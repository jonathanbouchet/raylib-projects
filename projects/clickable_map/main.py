import asyncio
from pathlib import Path
import pyray as pr
from grid import Grid

THIS_DIR = (Path(__file__).parent / "assets").resolve()


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
        texture_walkable_path: str,
        texture_obstacle_path: str,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.texture_walkable_path = texture_walkable_path
        self.texture_obstacle_path = texture_obstacle_path

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        self.grid = Grid(
            num_row=10,
            num_col=10,
            width=self.width,
            height=self.height,
            tile_size=64,
            grid_outline_color=pr.RED,
            block_probability=0.1,
            texture_walkable=pr.load_texture(self.texture_walkable_path),
            texture_obstacle=pr.load_texture(self.texture_obstacle_path),
        )

    def update(self) -> None:
        if pr.is_mouse_button_pressed(0):
            self.grid.get_cell_clicked(pr.get_mouse_position())

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        self.grid.draw()
        self.grid.draw_grid_outline()
        pr.draw_fps(0, 0)
        pr.end_drawing()

    def end(self) -> None:
        self.grid.unload_textures()
        pr.close_window()


async def main() -> None:

    game = Game(
        width=640, 
        height=640, 
        fps_target=60, 
        name="app", 
        background_color=pr.BLACK, 
        texture_obstacle_path=f"{THIS_DIR}/rock_64x64.png",
        texture_walkable_path=f"{THIS_DIR}/grass_64x64.png",
    )
    game.init()
    game.grid.print()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
