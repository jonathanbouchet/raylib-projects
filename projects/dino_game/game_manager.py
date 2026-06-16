import random
from pathlib import Path
import pyray as pr
import raylib as rl

THIS_DIR = (Path(__file__).parent / "assets").resolve()

class Sprite:
    def __init__(self, position: pr.Vector2, texture: pr.Texture, color: pr.Color, debug_color: pr.Color):
        self.position = position
        self.texture = texture
        self.color = color
        self.debug_color = debug_color

    def get_rectangle(self) -> pr.Rectangle:
        return pr.Rectangle(self.position.x, self.position.y, self.texture.width, self.texture.height)
    
    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        pass
    
    def draw(self) -> None:
        pr.draw_texture_v(self.texture, self.position, self.color)
        pr.draw_rectangle_lines(int(self.position.x), int(self.position.y), int(self.texture.width), int(self.texture.height), self.debug_color)


class Player(Sprite):
    def __init__(self, position: pr.Vector2, texture: pr.Texture, color: pr.Color, debug_color: pr.Color):
        super().__init__(position=position, texture=texture, color=color, debug_color=debug_color)
        # Physics state
        self.vy: float = 0.0  # vertical velocity (px/s)
        self.gravity: float = 1500.0  # gravity (px/s^2) — tune to taste
        self.jump_speed: float = 500.0  # initial jump impulse (px/s)
        self.is_grounded: bool = False
        self.dead = False
    
    def update(self, dt: float, other: pr.Rectangle) -> None:
        self.move(dt=dt, other=other)

    def check_collision(self, other: pr.Rectangle) -> bool:
        return pr.check_collision_recs(self.get_rectangle(), other)

    def check_collisions_enemies(self, enemies: list[pr.Rectangle]):
        for enemy in enemies:
            # print(f"{enemy.width}, {enemy.height}, {enemy.x, enemy.y}")
            if pr.check_collision_recs(self.get_rectangle(), enemy):
                print(f"{enemy.width}, {enemy.height}, {type(enemy)}")
                print("COLLISION")
                dead_texture = pr.load_texture("assets/dino/dino_dead_64x64.png")
                self.texture = dead_texture
                self.dead = True

    def move(self, dt: float,  other: pr.Rectangle):
        if pr.is_key_pressed(rl.KEY_SPACE) and self.is_grounded:
            self.vy = -self.jump_speed
            self.is_grounded = False

        # Apply gravity
        self.vy += self.gravity * dt

        # Integrate vertical velocity
        self.position.y += self.vy * dt

        # Simple collision resolution (vertical only)
        if self.check_collision(other):
            # If we hit the platform from above, snap on top and stop vertical velocity
            if self.vy >= 0 and self.position.y + self.texture.height > other.y:
                self.position.y = other.y - self.texture.height
                self.vy = 0.0
                self.is_grounded = True
            else:
                # Basic fallback: prevent penetrating from below (optional improvement)
                self.position.y = other.y + other.tecture.height
                self.vy = 0.0
                self.is_grounded = False
        else:
            self.is_grounded = False


class Block:
    def __init__(self, position: pr.Vector2, size: pr.Vector2, speed: float) -> None:
        self.position = position
        self.speed = speed
        self.size = size
        self.direction = pr.Vector2(-1, 0)
        self.disable = False

    def update(self, dt: float) -> None:
        # update velocity
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        if self.position.x < 0:
            self.disable = True

    def draw(self):
        pr.draw_rectangle_v(self.position, self.size, pr.BLACK)


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
        # player_texture_path: str,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.show_fps = show_fps
        self.floor_y_pos: int = floor_y_pos
        self.show_metrics = show_metrics
        # self.player_texture_path = player_texture_path

        # game running time variable
        self.run_time: float = 0
        self.frame_counter: int = 0

        # player
        # self.player_texture  = pr.load_texture(player_texture_path)
        # self.player = Player(position=pr.Vector2(100, self.height - int(self.player_texture.height) - 20), texture=self.player_texture, color=pr.WHITE, debug_color=pr.BLUE)

        # game objects
        self.block_list: list[Block] = []

    def init(self) -> None:
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

    def load_ground(self):
        self.floor_rect = pr.Rectangle(0, self.height - self.floor_y_pos, self.width, self.height - self.floor_y_pos)

    def load_player(self, player_texture_path: str) -> None:
        # init_window() needs to be called BEFORE loading any texture
        # WARNING: GL: GPU is not ready to load data, trying to load before InitWindow()?
        self.player_texture  = pr.load_texture(player_texture_path)
        self.player = Player(position=pr.Vector2(100, self.height - int(self.player_texture.height) - 20), texture=self.player_texture, color=pr.WHITE, debug_color=pr.BLUE)

    def update(self) -> None:
        dt = pr.get_frame_time()
        self.frame_counter += 1
        self.run_time = pr.get_time()
        if self.frame_counter % 60 == 0:  # spawn a block every frame
            if random.random() < 0.95:  # and not block_y_spawn:
                s = pr.Vector2(10, random.randint(10, 40))
                print(f"{s.x}, {s.y}")
                self.block_list.append(
                    Block(
                        position=pr.Vector2(
                            self.width, random.randint(100, 200 - int(s.y) - 10)
                        ),
                        size=s,
                        speed=100,
                    )
                )

        # update player
        self.player.update(dt=dt, other=self.floor_rect)
        # self.player.check_collisions_enemies(enemies=[x.get_rectangle() for x in self.block_list])

        # updates all blocks
        _ = [block.update(dt=dt) for block in self.block_list]

        # clean list of blocks
        self.discard_blocks()

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)

        # draw player
        self.player.draw()

        # draw block
        _ = [block.draw() for block in self.block_list if not block.disable]

        # draw floor
        pr.draw_line_v(
            pr.Vector2(0, self.height - self.floor_y_pos),
            pr.Vector2(self.width, self.height - self.floor_y_pos),
            pr.WHITE,
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
            pr.draw_text(f"blocks:{(len(self.block_list))}", 0, 60, 20, pr.GREEN)

        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()

    def end(self) -> None:
        pr.close_window()

    def discard_blocks(self):
        self.block_list = [x for x in self.block_list if x.position.x > 0]


if __name__ == "__main__":
    game = Game(
        width=800,
        height=200,
        fps_target=60,
        name="app",
        background_color=pr.Color(211, 211, 211, 255), # LIGHT GRAY
        floor_y_pos=100,
        show_fps=True,
        show_metrics=True,
        # player_texture_path=f"{THIS_DIR}/dino_idle_64x64.png",
    )
    game.init()
    game.load_ground()
    game.load_player(player_texture_path=f"{THIS_DIR}/dino_idle_64x64.png")
    game.run()
    game.end()
