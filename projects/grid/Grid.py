import numpy as np
import pyray as pr
import settings as settings


class Grid:
    def __init__(self, num_rows, num_cols: int, cell_size: int):
        self.grid_rows: int = num_rows
        self.grid_cols: int = num_cols
        self.cell_size: int = cell_size
        self.grid = np.zeros(
            (self.grid_rows, self.grid_cols), dtype=int
        )  # init with 0's
        self.colors: list[pr.Color] = [pr.DARKGRAY, pr.YELLOW]

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
                    self.colors[cell_value],
                )

    def get_cell_clicked(self, pos: pr.Vector2) -> tuple[int, int]:
        i = int(pos.x / self.cell_size)
        j = int(pos.y / self.cell_size)
        self.grid[j][i] = not self.grid[j][i]
        return [i, j]
