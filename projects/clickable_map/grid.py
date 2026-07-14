import pyray as pr


class Grid:
    def __init__(
        self,
        num_row: int,
        num_col: int,
        width: int,
        height: int,
        tile_width: int,
        tile_height: int,
        grid_outline_color: pr.Color,
    ) -> None:
        self.num_row = num_row
        self.num_col = num_col
        self.game_width = width
        self.game_height = height
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.grid_outline_color = grid_outline_color

    def draw(self) -> None:
        for i in range(self.num_row):
            for j in range(self.num_col):
                if j == 0:
                    pr.draw_line(
                        0,
                        i * self.tile_height,
                        self.game_width,
                        i * self.tile_height,
                        self.grid_outline_color,
                    )
