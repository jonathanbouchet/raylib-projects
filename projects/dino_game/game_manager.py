import random
import pyray as pr


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
        pr.draw_rectangle_v(self.position, self.size, pr.WHITE)


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
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.show_fps = show_fps
        self.floor_y_pos: int = floor_y_pos
        self.show_metrics = show_metrics

        # game running time variable
        self.run_time: float = 0
        self.frame_counter: int = 0

        # game objects
        self.block_list: list[Block] = []

    def init(self) -> None:
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

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

        # updates all blocks
        _ = [block.update(dt=dt) for block in self.block_list]

        # clean list of blocks
        self.discard_blocks()

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)

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
        background_color=pr.BLACK,
        floor_y_pos=100,
        show_fps=True,
        show_metrics=True,
    )
    game.init()
    game.run()
    game.end()
