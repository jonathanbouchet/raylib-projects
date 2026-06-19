import random
from pathlib import Path
from enum import Enum
import pyray as pr
from entities import StaticSprite, Player, Enemy, Cloud, PlayerStates

THIS_DIR = (Path(__file__).parent / "assets").resolve()


class GameStates(Enum):
    INIT = 0  # start of the app
    RUN = 1  # game is running
    PAUSE = 2  # game is paused after a collision player <-> enemy


class Game:
    def __init__(
        self,
        width: int,  # screen width
        height: int,  # screen height
        fps_target: int,  # target FPS
        name: str,  # name of app
        background_color: pr.Color,  # background color
        floor_y_pos: int,  # offset from height to locate the 'floor'
        show_fps: bool,  # flag for showing FPS counter
        show_metrics: bool,  # flag to show in-game metrics
        player_textures_data: dict[str, list[str]],  # player textures: idle, run, dead
        enemy_textures_data: list[str, str],  # enemy texture: single and double cactus
        cloud_texture_data: str,  # cloud texture: only 1
        level_up_sound_path: str,
        level: int,  # game level
        number_per_level: int,  # the number of objects to avoid to increment the level
        number_avoided: int,  # number of cactus avoided
        enemy_speed: int,  # speed of cactus when spawned
        enemy_spawn_probability: float,  # probability of an enemy to spawn at every second
        cloud_speed: int,  # speed of the cloud
        player_debug: bool,  # flag to show Rectangle outline of the player and its state
        enemy_debug: bool,  # flag to show Rectangle outline of the enemy
        cloud_debug: bool,  # flag to show Rectangle outline of the cloud
        floor_debug: bool,  # flag to show Rectangle outline and filled area of the floor
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.show_fps = show_fps
        self.floor_y_pos: int = floor_y_pos
        self.show_metrics = show_metrics
        self.player_textures_data = player_textures_data
        self.enemy_textures_data = enemy_textures_data
        self.cloud_texture_data = cloud_texture_data
        self.level_up_sound_path = level_up_sound_path
        self.level = level
        self.number_per_level = number_per_level
        self.number_avoided = number_avoided
        self.state = GameStates.INIT
        self.enemy_speed = enemy_speed
        self.enemy_spawn_probability = enemy_spawn_probability
        self.cloud_speed = cloud_speed
        self.player_debug = player_debug
        self.enemy_debug = enemy_debug
        self.cloud_debug = cloud_debug
        self.floor_debug = floor_debug

        # game running time variable
        self.run_time: float = 0  # time in second since the app has started
        self.frame_counter: int = 0  # frame counter, ie every time self.run() is done

        # game objects
        self.enemy_list: list[Enemy] = []  # list to hold every time an enemy is spawned

    def init(self) -> None:
        """create raylib window"""
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        pr.init_audio_device()

    def load_props(self) -> None:
        """load_props such as the floor needed for collision and cloud (no collision)"""
        # ground
        self.ground = StaticSprite(
            window_width=self.width,
            window_height=self.height,
            floor_y_pos=self.floor_y_pos,
            show_debug=self.floor_debug,
        )

        # cloud
        self.cloud_texture = pr.load_texture(self.cloud_texture_data)
        self.cloud = Cloud(
            position=pr.Vector2(self.width, 20),
            texture=self.cloud_texture,
            color=pr.DARKGRAY,
            debug_color=pr.YELLOW,
            speed=self.cloud_speed,
            screen_width=self.width,
            show_debug=self.cloud_debug,
        )

        # sound
        self.level_up_sound: pr.Sound = pr.load_sound(self.level_up_sound_path)

    def load_player(self) -> None:
        """load_player:
            init_window() needs to be called BEFORE loading any texture
            WARNING: GL: GPU is not ready to load data, trying to load before InitWindow()?
        - player is spawned at 100 pixels from left (hardcoded) with the idle texture
        - other textures are extracted for later used
        """
        self.player_texture = pr.load_texture(self.player_textures_data.get("idle")[0])
        player_running_textures = self.player_textures_data.get("run")
        player_dead_texture = self.player_textures_data.get("dead")[0]
        self.player = Player(
            position=pr.Vector2(
                100, self.height - int(self.player_texture.height) - 20
            ),
            texture=self.player_texture,
            running_textures_path=player_running_textures,
            dead_texture_path=player_dead_texture,
            color=pr.WHITE,
            debug_color=pr.BLUE,
            show_debug=self.player_debug,
        )

    def load_enemy_texture(self) -> None:
        """load_enemy_textures: single and double cactus"""
        self.enemy_textures = [pr.load_texture(x) for x in self.enemy_textures_data]

    def spawn_enemy(self) -> None:
        """spawn_enemy / cactus:
        - spawned every 60 frames = 1 second with a probability of 75%
        """
        if self.frame_counter % self.fps_target == 0:  # spawn a block every frame
            if random.random() < self.enemy_spawn_probability:
                # randomly select one of the 2 enemy textures
                current_texture = random.choices(self.enemy_textures)[0]
                print(f"{current_texture=}")
                self.enemy_list.append(
                    Enemy(
                        texture=current_texture,
                        position=pr.Vector2(
                            self.width,
                            self.height - int(current_texture.height) - 20,
                        ),
                        speed=self.enemy_speed,
                        color=pr.WHITE,
                        scale=random.uniform(1.0, 1.5),
                        debug_color=pr.PINK,
                        show_debug=self.enemy_debug,
                    )
                )

    def calculate_level(self) -> None:
        self.number_avoided = len(
            [
                enemy
                for enemy in self.enemy_list
                if (enemy.position.x + enemy.texture.width) < self.player.position.x
            ]
        )
        if int(self.number_avoided / self.number_per_level) + 1 > self.level:
            self.level += 1
            pr.play_sound(self.level_up_sound)

    def update(self) -> None:
        """game update
        - if player is not dead and games is running -> update all objects (this take care of the INIT state):
            - we spawn enemy if frame counter condition is met
            - player is updated
             - movement and floor detection
             - then collision of player with enemies
            - enemies are updated
            - cloud is updated
        - if player is dead, switch to PAUSE mode
        - otherwise it means the game just start -> INIT
        """
        # check Player State
        if (
            self.player.get_state() != PlayerStates.DEAD
            and self.state == GameStates.RUN
        ):
            # self.state = GameStates.RUN
            dt = pr.get_frame_time()
            self.frame_counter += 1
            self.run_time = pr.get_time()

            self.spawn_enemy()

            # update player
            self.player.update(dt=dt, other=self.ground.floor_rect)
            self.player.check_collisions_enemies(
                enemies=[x.get_rectangle() for x in self.enemy_list]
            )

            # updates all blocks
            _ = [enemy.update(dt=dt) for enemy in self.enemy_list]

            # update cloud
            self.cloud.update(dt=dt)
            self.calculate_level()

            # clean list of blocks
            # self.discard_blocks()
        elif self.player.get_state() == PlayerStates.DEAD:
            self.state = GameStates.PAUSE
        else:
            self.state = GameStates.INIT

    def draw(self) -> None:
        """draw game objects
        - first is background then player, then enemies and floor and cloud
        - draw UI next
        - when the game paused (collision), update is not called so that's how the textures stay frozen
        - if the game state is either in INIT or PAUSE, repsective UI button are shown
        - once clicked, the game state switched back to RUN and the game resumes

        """
        dt = pr.get_frame_time()
        pr.begin_drawing()
        pr.clear_background(self.background_color)

        # draw player
        self.player.draw(dt=dt)

        # draw block
        _ = [enemy.draw() for enemy in self.enemy_list if not enemy.disable]

        # draw floor
        self.ground.draw()

        # update cloud
        self.cloud.draw()

        # draw UI
        pr.draw_text(f"LEVEL: {self.level}", self.width - 100, 0, 10, pr.DARKGRAY)
        pr.draw_text(
            f"SCORE: {int(self.frame_counter / 10)}",
            self.width - 100,
            10,
            10,
            pr.DARKGRAY,
        )
        pr.draw_text(
            f"AVOIDED: {int(self.number_avoided)}",
            self.width - 100,
            20,
            10,
            pr.DARKGRAY,
        )

        if self.show_fps:
            pr.draw_fps(0, 0)

        if self.show_metrics:
            pr.draw_text(f"time ellapsed:{int(self.run_time)}", 0, 20, 20, pr.DARKGREEN)
            pr.draw_text(
                f"frame count:{(int(self.frame_counter))}", 0, 40, 20, pr.DARKGREEN
            )
            pr.draw_text(f"blocks:{(len(self.enemy_list))}", 0, 60, 20, pr.DARKGREEN)
            pr.draw_text(f"{self.state}", 0, 80, 20, pr.DARKGREEN)

        if self.state == GameStates.PAUSE:
            if pr.gui_button(
                pr.Rectangle(self.width / 2 - 75, self.height / 2 - 20, 150, 40),
                "Click to Restart",
            ):
                # keep track of current score
                self.high_score = int(self.frame_counter / 10)

                # reset all variables
                self.run_time = 0
                self.frame_counter = 0
                self.enemy_list = []
                self.level = 1
                self.number_avoided = 0

                # re-instantiate player, enemy, cloud
                self.load_player()
                self.load_enemy_texture()
                self.state = GameStates.RUN
                self.update()

        if self.state == GameStates.INIT:
            if pr.gui_button(
                pr.Rectangle(self.width / 2 - 75, self.height / 2 - 20, 150, 40),
                "Space to start",
            ):
                self.state = GameStates.RUN

        pr.end_drawing()

    def run(self) -> None:
        """main game loop
        1. update all game objects
        2. draw updated game objects
        """
        while not pr.window_should_close():
            self.update()
            self.draw()

    def end(self) -> None:
        """end / close game window"""
        pr.close_audio_device()
        pr.close_window()

    def discard_blocks(self):
        """discard blocks: not used
        - goal is not accumulate all enemies in the list after they disappear from the game screen
        """
        self.enemy_list = [x for x in self.enemy_list if x.position.x > 0]


if __name__ == "__main__":
    game = Game(
        width=800,
        height=200,
        fps_target=60,
        name="app",
        background_color=pr.Color(211, 211, 211, 255),  # LIGHT GRAY
        floor_y_pos=20,
        show_fps=True,
        show_metrics=True,
        player_textures_data={
            "idle": [f"{THIS_DIR}/dino_idle_64x64.png"],
            "run": [
                f"{THIS_DIR}/dino_left_leg_64x64.png",
                f"{THIS_DIR}/dino_right_leg_64x64.png",
            ],
            "dead": [f"{THIS_DIR}/dino_dead_64x64.png"],
        },
        enemy_textures_data=[
            f"{THIS_DIR}/cactus_2_16x32.png",
            f"{THIS_DIR}/cactus_12x32.png",
        ],
        cloud_texture_data=f"{THIS_DIR}/cloud_64x64.png",
        level_up_sound_path=f"{THIS_DIR}/Coin_7.wav",
        level=1,
        number_per_level=5,
        number_avoided=0,
        enemy_speed=200,
        enemy_spawn_probability=0.75,
        cloud_speed=20,
        player_debug=True,
        enemy_debug=True,
        cloud_debug=True,
        floor_debug=True,
    )
    game.init()
    game.load_props()
    game.load_player()
    game.load_enemy_texture()

    # game.state = GameStates.RUN
    game.run()
    game.end()
