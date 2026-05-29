import numpy as np
import pyray as pr


class Grid:
    def __init__(self, num_rows, num_cols: int, cell_size: int):
        self.grid_rows: int = num_rows
        self.grid_cols: int = num_cols
        self.cell_size: int = cell_size
        self.grid = np.zeros((self.grid_rows, self.grid_cols), dtype=int)
        self.color_cell_value: pr.Color = pr.Color(
            26, 31, 40, 255
        )  # backgroud = darkgrey

    def update(self) -> None:
        pass

    def print(self) -> None:
        for row in self.grid:
            for element in row:
                print(element, end=" ")
            print()

    def draw(self) -> None:
        for i in range(self.grid_rows):
            for j in range(self.grid_cols):
                cell_value = self.grid[i][j]
                pr.draw_rectangle(
                    j * self.cell_size + 1,
                    i * self.cell_size + 1,
                    self.cell_size - 1,
                    self.cell_size - 1,
                    # pr.BEIGE
                    # self.colors[cell_value],
                    self.color_cell_value,
                )
