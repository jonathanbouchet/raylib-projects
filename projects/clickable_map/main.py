import asyncio
import pyray as pr
from grid import Grid


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        self.grid = Grid(
            num_row=10,
            num_col=10,
            width=self.width,
            height=self.height,
            tile_width=60,
            tile_height=60,
            grid_outline_color=pr.RED,
        )

    def update(self) -> None:
        pass

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        self.grid.draw()
        pr.draw_fps(0, 0)
        pr.end_drawing()

    def end(self) -> None:
        pr.close_window()


async def main() -> None:
    game = Game(
        width=600, height=600, fps_target=60, name="app", background_color=pr.BLACK
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
