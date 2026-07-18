import pyray as pr
import numpy as np


class Grid:
    def __init__(
        self,
        num_row: int,
        num_col: int,
        width: int,
        height: int,
        tile_size: int,
        grid_outline_color: pr.Color,
        block_probability: float,
        color_walkable_cell: pr.Color,
        color_obstacle_cell: pr.Color,
    ) -> None:
        self.num_row = num_row
        self.num_col = num_col
        self.game_width = width
        self.game_height = height
        self.tile_size = tile_size
        self.grid_outline_color = grid_outline_color
        self.block_probability = block_probability
        self.grid_cell_values: np.ndarray[tuple[int, int], np.dtype[np.int64]] = (
            np.where(
                np.random.rand(self.num_row, self.num_col) < self.block_probability,
                0,
                1,
            )
        )  # init with 1's as walkable tiles for the pathfinder algorithm
        self.grid_cell_clickable: np.ndarray[tuple[int, int], np.dtype[np.bool]] = (
            self.grid_cell_values.astype(bool)
        )
        self.grid_cell_colors: list[pr.Color] = [
            color_obstacle_cell,
            color_walkable_cell,
        ]

    def print(self) -> None:
        for row in self.grid_cell_values:
            for element in row:
                print(element, end=" ")
            print()

    def get_cell_clicked(self, pos: pr.Vector2) -> tuple[int, int]:
        i = int(pos.x / self.tile_size)
        j = int(pos.y / self.tile_size)
        if self.grid_cell_clickable[j][i]:
            pass
            # self.grid_cell_values[j][i] = not self.grid_cell_values[j][i]

    def draw_grid_outline(self) -> None:
        for i in range(self.num_row):
            pr.draw_line(
                0,
                i * self.tile_size,
                self.game_width,
                i * self.tile_size,
                self.grid_outline_color,
            )
        for j in range(self.num_col):
            pr.draw_line(
                j * self.tile_size,
                0,
                j * self.tile_size,
                self.game_height,
                self.grid_outline_color,
            )

    def draw(self) -> None:
        for i in range(self.num_row):
            for j in range(self.num_col):
                cell_value = self.grid_cell_values[i][j]
                pr.draw_rectangle(
                    j * self.tile_size,
                    i * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                    self.grid_cell_colors[cell_value],
                )
