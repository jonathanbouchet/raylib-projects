import pyray as pr
from .resource_manager import ResourceManager
from .grid import Grid


class Game:
    def __init__(self, resource_manager) -> None:
        self.resources_manager: ResourceManager = resource_manager
        # generalities
        self.width: int = self.resources_manager.game_data().get("width")
        self.height: int = self.resources_manager.game_data().get("height")
        self.fps_target: int = self.resources_manager.game_data().get("fps")
        self.background_color: pr.Color = tuple(
            self.resources_manager.game_data().get("background_color")
        )
        self.name: str = self.resources_manager.game_data().get("name")
        self.debug: bool = self.resources_manager.game_data().get("debug")

        # grid
        self.color_walkable_cell = self.resources_manager.grid_data().get(
            "color_walkable_cell"
        )
        self.color_obstacle_cell = self.resources_manager.grid_data().get(
            "color_obstable_cell"
        )

    def init(self) -> None:
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
            color_walkable_cell=self.color_walkable_cell,
            color_obstacle_cell=self.color_obstacle_cell,
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
