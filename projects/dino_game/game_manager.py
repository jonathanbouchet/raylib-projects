import random
from pathlib import Path
from enum import Enum
import pyray as pr
from entities import Player, Enemy, Cloud, PlayerStates

THIS_DIR = (Path(__file__).parent / "assets").resolve()

class GameStates(Enum):
    INIT = 0
    RUN = 1
    PAUSE = 2

class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
        floor_y_pos: int,
        show_fps: bool,
        show_metrics: bool,
        player_textures_data: dict[str, list[str]],
        enemy_textures_data: list[str, str],
        cloud_texture_path: str,
        level: int,
        number_avoided: int,
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
        self.cloud_texture_path = cloud_texture_path
        self.level = level
        self.number_avoided = number_avoided
        self.state = GameStates.INIT

        # game running time variable
        self.run_time: float = 0
        self.frame_counter: int = 0

        # game objects
        self.enemy_list: list[Enemy] = []

        # props
        self.cloud_list: list[Cloud] = []

    def init(self) -> None:
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

    def load_props(self) -> None:
        # ground
        self.floor_rect = pr.Rectangle(
            0,
            self.height - self.floor_y_pos,
            self.width,
            self.height - self.floor_y_pos,
        )

        # cloud
        self.cloud_texture = pr.load_texture(self.cloud_texture_path)
        self.cloud = Cloud(
            position=pr.Vector2(self.width, 20),
            texture=self.cloud_texture,
            color=pr.DARKGRAY,
            debug_color=pr.YELLOW,
            speed=20,
            screen_width=self.width
        )

    def load_player(self) -> None:
        # init_window() needs to be called BEFORE loading any texture
        # WARNING: GL: GPU is not ready to load data, trying to load before InitWindow()?

        self.player_texture = pr.load_texture(self.player_textures_data.get('idle')[0])
        player_running_textures = self.player_textures_data.get('run')
        player_dead_texture = self.player_textures_data.get('dead')[0]
        self.player = Player(
            position=pr.Vector2(
                100, self.height - int(self.player_texture.height) - 20
            ),
            texture=self.player_texture,
            running_textures_path=player_running_textures,
            dead_texture_path=player_dead_texture,
            color=pr.WHITE,
            debug_color=pr.BLUE,
        )

    def load_enemy_texture(self) -> None:
        self.enemy_textures = [pr.load_texture(x) for x in self.enemy_textures_data]

    def update(self) -> None:
        # check Player State
        if self.player.get_state() != PlayerStates.DEAD:
            self.state = GameStates.RUN
            dt = pr.get_frame_time()
            self.frame_counter += 1
            self.run_time = pr.get_time()
            if self.frame_counter % 60 == 0:  # spawn a block every frame
                if random.random() < 0.9:
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
                            speed=200,
                            color=pr.WHITE,
                            scale=random.uniform(1.0, 2.0),
                            debug_color=pr.PINK,
                        )
                    )


            # update player
            self.player.update(dt=dt, other=self.floor_rect)
            self.player.check_collisions_enemies(
                enemies=[x.get_rectangle() for x in self.enemy_list]
            )

            # updates all blocks
            _ = [block.update(dt=dt) for block in self.enemy_list]

            # update cloud
            self.cloud.update(dt=dt)

            self.number_avoided = len([enemy for enemy in self.enemy_list if (enemy.position.x + enemy.texture.width) < self.player.position.x])
            self.level = int(self.number_avoided / 5) + 1

            # clean list of blocks
            # self.discard_blocks()
        else:
            self.state = GameStates.PAUSE

    def draw(self) -> None:
        dt = pr.get_frame_time()
        pr.begin_drawing()
        pr.clear_background(self.background_color)

        # draw player
        self.player.draw(dt=dt)

        # draw block
        _ = [block.draw() for block in self.enemy_list if not block.disable]

        # draw floor
        pr.draw_rectangle_rec(self.floor_rect, pr.YELLOW)
        pr.draw_line_v(
            pr.Vector2(0, self.height - self.floor_y_pos),
            pr.Vector2(self.width, self.height - self.floor_y_pos),
            pr.BLUE,
        )
        pr.draw_line_v(
            pr.Vector2(0, int(self.height / 2)),
            pr.Vector2(self.width, int(self.height / 2)),
            pr.RED,
        )
        # update cloud
        self.cloud.draw()

        # draw score
        pr.draw_text(f"LEVEL: {self.level}", self.width - 100, 0, 10, pr.DARKGRAY)
        pr.draw_text(f"SCORE: {int(self.frame_counter/10)}", self.width - 100, 10, 10, pr.DARKGRAY)
        pr.draw_text(f"AVOIDED: {int(self.number_avoided)}", self.width - 100, 20, 10, pr.DARKGRAY)
        
        if self.show_fps:
            pr.draw_fps(0, 0)

        if self.show_metrics:
            pr.draw_text(f"time ellapsed:{int(self.run_time)}", 0, 20, 20, pr.DARKGREEN)
            pr.draw_text(
                f"frame count:{(int(self.frame_counter))}", 0, 40, 20, pr.DARKGREEN
            )
            pr.draw_text(f"blocks:{(len(self.enemy_list))}", 0, 60, 20, pr.DARKGREEN)
            pr.draw_text(f"{self.state}", 0, 80, 20, pr.DARKGREEN)

        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()

    def end(self) -> None:
        pr.close_window()

    def discard_blocks(self):
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
                f"{THIS_DIR}/dino_right_leg_64x64.png"
                ],
            "dead": [f"{THIS_DIR}/dino_dead_64x64.png"]
        },
        enemy_textures_data=[
            f"{THIS_DIR}/cactus_2_16x32.png",
            f"{THIS_DIR}/cactus_12x32.png"
        ],
        cloud_texture_path=f"{THIS_DIR}/cloud_64x64.png",
        level=1,
        number_avoided=0
    )
    game.init()
    game.load_props()
    game.load_player()
    game.load_enemy_texture()
    game.state = GameStates.RUN
    game.run()
    game.end()
