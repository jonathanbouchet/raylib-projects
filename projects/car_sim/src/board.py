import copy
import pyray as pr
import numpy as np


class Board:
    def __init__(
        self,
        num_row: int,
        num_col: int,
        width: int,
        height: int,
        tile_size: int,
        board_outline_color: pr.Color,
        obstacle_probability: float,
        color_walkable_cell: pr.Color,
        color_obstacle_cell: pr.Color,
        color_path_cell: pr.Color,
        debug: bool,
    ) -> None:
        self.num_row = num_row
        self.num_col = num_col
        self.game_width = width
        self.game_height = height
        self.tile_size = tile_size
        self.board_outline_color = board_outline_color
        self.obstacle_probability = obstacle_probability
        self.debug = debug
        self.board_cell_values: np.ndarray[tuple[int, int], np.dtype[np.int64]] = (
            np.where(
                np.random.rand(self.num_row, self.num_col) < self.obstacle_probability,
                0,
                1,
            )
        )  # init with 1's as walkable tiles for the pathfinder algorithm
        self.board_cell_clickable: np.ndarray[tuple[int, int], np.dtype[np.bool]] = (
            self.board_cell_values.astype(bool)
        )
        self.board_cell_colors: list[pr.Color] = [
            color_obstacle_cell,
            color_walkable_cell,
            color_path_cell,
        ]
        self.initial_board: list[list[int]] = copy.deepcopy(
            self.board_cell_values.tolist()
        )  # convert to list to make it immutable

    def add_player(self) -> tuple[int, int]:
        # should be in walkable cell, i.e cell_values = 1
        rows, cols = np.nonzero(self.board_cell_values)
        print(f"{rows=}, {cols=}")
        # take randomly a couple with these values
        val = np.random.randint(0, len(rows))
        print(f"player position on the grid: {rows[val]}, {cols[val]}")
        return [rows[val], cols[val]]

    def update(self) -> None:
        self.get_cell_clicked()

    def update_board(self, path):
        for val in path:
            self.board_cell_values[val[0], val[1]] = 2

    def print(self) -> None:
        for row in self.board_cell_values:
            for element in row:
                print(element, end=" ")
            print()

    def get_cell_clicked(self, pos: pr.Vector2) -> tuple[int, int]:
        i = int(pos.x / self.tile_size)
        j = int(pos.y / self.tile_size)
        if self.board_cell_clickable[j][i]:
            return [i, j]
        else:
            return [None, None]

    def get_board(self) -> np.ndarray[tuple[int, int], np.dtype[np.int64]]:
        return self.board_cell_values

    def draw_board_outline(self) -> None:
        for i in range(self.num_row):
            pr.draw_line(
                0,
                i * self.tile_size,
                self.game_width,
                i * self.tile_size,
                self.board_outline_color,
            )
        for j in range(self.num_col):
            pr.draw_line(
                j * self.tile_size,
                0,
                j * self.tile_size,
                self.game_height,
                self.board_outline_color,
            )

    def draw(self) -> None:
        for i in range(self.num_row):
            for j in range(self.num_col):
                cell_value = self.board_cell_values[i][j]
                pr.draw_rectangle(
                    j * self.tile_size,
                    i * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                    self.board_cell_colors[cell_value],
                )

    def reset_board(self) -> None:
        print("resetting the board")
        print(f"original board: {self.initial_board}")
        self.board_cell_values = np.array(self.initial_board)
        print("done")
        self.print()
