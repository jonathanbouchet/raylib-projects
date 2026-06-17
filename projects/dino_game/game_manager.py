import random
from pathlib import Path
import pyray as pr
from entities import Player, Enemy

THIS_DIR = (Path(__file__).parent / "assets").resolve()


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target,
        name: str,
        background_color: pr.Color,
        floor_y_pos: int,
        show_fps: bool,
        show_metrics: bool,
        player_textures_data: dict[str, str],
        enemy_texture_path: str,
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
        self.enemy_texture_path = enemy_texture_path

        # game running time variable
        self.run_time: float = 0
        self.frame_counter: int = 0

        # game objects
        self.enemy_list: list[Enemy] = []

    def init(self) -> None:
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

    def load_ground(self):
        self.floor_rect = pr.Rectangle(
            0,
            self.height - self.floor_y_pos,
            self.width,
            self.height - self.floor_y_pos,
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
        self.enemy_texture = pr.load_texture(self.enemy_texture_path)

    def update(self) -> None:
        dt = pr.get_frame_time()
        self.frame_counter += 1
        self.run_time = pr.get_time()
        if self.frame_counter % 60 == 0:  # spawn a block every frame
            if random.random() < 0.95:
                s = pr.Vector2(10, random.randint(10, 40))
                print(f"{s.x}, {s.y}")
                self.enemy_list.append(
                    Enemy(
                        texture=self.enemy_texture,
                        position=pr.Vector2(
                            self.width,
                            self.height - int(self.enemy_texture.height) - 20,
                        ),
                        speed=200,
                        color=pr.WHITE,
                        scale=random.uniform(0.8, 1.4),
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

        # clean list of blocks
        self.discard_blocks()

    def draw(self) -> None:
        dt = pr.get_frame_time()
        pr.begin_drawing()
        pr.clear_background(self.background_color)

        # draw player
        self.player.draw(dt=dt)

        # draw block
        _ = [block.draw() for block in self.enemy_list if not block.disable]

        # draw floor
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
        if self.show_fps:
            pr.draw_fps(0, 0)

        if self.show_metrics:
            pr.draw_text(f"time ellapsed:{int(self.run_time)}", 0, 20, 20, pr.GREEN)
            pr.draw_text(
                f"frame count:{(int(self.frame_counter))}", 0, 40, 20, pr.GREEN
            )
            pr.draw_text(f"blocks:{(len(self.enemy_list))}", 0, 60, 20, pr.GREEN)

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
        enemy_texture_path=f"{THIS_DIR}/cactus_12x32.png",
    )
    game.init()
    game.load_ground()
    game.load_player()
    game.load_enemy_texture()
    game.run()
    game.end()
