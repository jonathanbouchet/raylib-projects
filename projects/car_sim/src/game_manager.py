import pyray as pr
from .resource_manager import ResourceManager
from .board import Board
from .sprite import Sprite
from .timer import Timer
from .utils import find_path


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

        # board
        self.board = Board(
            num_row=self.resources_manager.board_data().get("num_row"),
            num_col=self.resources_manager.board_data().get("num_col"),
            width=self.width,
            height=self.height,
            tile_size=self.resources_manager.board_data().get("cell_size"),
            board_outline_color=self.resources_manager.board_data().get(
                "outline_color"
            ),
            obstacle_probability=self.resources_manager.board_data().get(
                "obstacle_probability"
            ),
            color_walkable_cell=self.resources_manager.board_data().get(
                "color_walkable_cell"
            ),
            color_obstacle_cell=self.resources_manager.board_data().get(
                "color_obstable_cell"
            ),
            debug=self.resources_manager.board_data().get("debug"),
        )

        # player
        player_position_board = self.board.add_player()
        # player_position_board = [0,0]
        player_position_world = pr.Vector2(
            (player_position_board[0] + 1) * self.board.tile_size,
            (player_position_board[1] + 1) * self.board.tile_size,
        )  # board indexes start at 0
        self.player = Sprite(
            position=player_position_world,
            position_board=pr.Vector2(
                player_position_board[0], player_position_board[1]
            ),
            radius=self.resources_manager.player_sprite().get("radius"),
            color=self.resources_manager.player_sprite().get("color"),
            debug=self.resources_manager.player_sprite().get("debug"),
        )
        self.player_timer = Timer(
            duration=1, repeat=True, autostart=False, func=self.player.draw
        )

    def init(self) -> None:
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        # self.grid = Grid(
        #     num_row=self.grid.num_row,
        #     num_col=self.grid.num_col,
        #     width=self.width,
        #     height=self.height,
        #     tile_size=self.grid.cell_size,
        #     grid_outline_color=self.grid.grid_outline_color,
        #     block_probability=0.1,
        #     color_walkable_cell=self.grid.color_walkable_cell,
        #     color_obstacle_cell=self.grid.color_obstacle_cell,
        # )

    def update(self) -> None:
        # update timer that delays the player drawing
        self.player_timer.update()
        if pr.is_mouse_button_pressed(0):
            self.board.reset_board()
            mouse_pos = self.board.get_cell_clicked(pr.get_mouse_position())
            print(f"{mouse_pos=}")
            if mouse_pos[0] is not None and mouse_pos[1] is not None:
                # walkable tile
                current_player_position = self.player.get_board_position()
                print(f"{current_player_position=}")
                path = find_path(
                    board=self.board.get_board(),
                    player_pos=current_player_position,
                    target=mouse_pos,
                )
                print(f"{path=}")
                self.board.update_board(path=path)
                self.player.set_position(pr.Vector2(mouse_pos[0], mouse_pos[1]))

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        self.board.draw()
        self.board.draw_board_outline()
        self.player.draw()
        if self.debug:
            pr.draw_fps(0, 0)
            pr.draw_text(
                f"PLAYER:[{int(self.player.position_board.x)},{int(self.player.position_board.y)}]",
                0,
                20,
                20,
                pr.GREEN,
            )
            self.board.draw_board_outline()
        pr.end_drawing()
