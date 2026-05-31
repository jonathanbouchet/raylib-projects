import numpy as np
import pyray as pr
import settings as settings


class BaseBoard:
    def __init__(self, num_rows, num_cols: int, cell_size: int):
        self.grid_rows: int = num_rows
        self.grid_cols: int = num_cols
        self.cell_size: int = cell_size
        self.grid = np.ones(
            (self.grid_rows, self.grid_cols), dtype=int
        )  # init with 1's as walkable tiles for the pathfinder algorithm
        self.colors: list[pr.Color] = [
            pr.BLACK,
            pr.DARKGRAY,
            pr.YELLOW,
            pr.GREEN,
            pr.PINK,
        ]

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
        if self.grid[j][i] == 1:
            self.grid[j][i] = 2
        elif self.grid[j][i] == 2:
            self.grid[j][i] = 1
        return [i, j]

   