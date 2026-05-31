import copy
import numpy as np
import pyray as pr
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.dijkstra import DijkstraFinder
from pathfinding.finder.breadth_first import BreadthFirstFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
import settings as settings


class Board:
    def __init__(self, num_rows, num_cols: int, cell_size: int):
        self.grid_rows: int = num_rows
        self.grid_cols: int = num_cols
        self.cell_size: int = cell_size
        # self.grid = np.ones(
        #     (self.grid_rows, self.grid_cols), dtype=int
        # )  # init with 1's as walkable tiles for the pathfinder algorithm
        self.colors: list[pr.Color] = [
            pr.BLACK,
            pr.DARKGRAY,
            pr.YELLOW,
            pr.GREEN,
            pr.PINK,
        ]
        self.start_cell: list[int] = []  # to be updated when the user clicks a cell
        self.end_cell: list[int] = [self.grid_rows - 1, self.grid_rows - 1]  # end cell
        self.block_probability = 0.15  # 15% of chance for any element to be zeros
        self.grid = np.where(
            np.random.rand(self.grid_rows, self.grid_cols) < self.block_probability,
            0,
            1,
        )  # init with 1's as walkable tiles for the pathfinder algorithm
        self.has_been_processed: bool = False
        self.initial_grid = None

    def prepare_grid(self):
        self.end_cell: list[int] = [
            self.grid_rows - 1,
            self.grid_rows - 1,
        ]  # 3 = end cell
        self.grid[self.end_cell[0]][self.end_cell[1]] = 3
        self.initial_grid = copy.deepcopy(self.grid)  # self.grid.copy()

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
        self.grid[j][i] = 2  # not self.grid[j][i]
        self.start_cell = [i, j]
        return [i, j]

    def find_path(self) -> None:
        # 1. instantiate the grid object
        grid = Grid(matrix=self.grid)

        # 2. define the start and end nodes (X, Y format)
        start = grid.node(self.start_cell[0], self.start_cell[1])
        end = grid.node(self.end_cell[0], self.end_cell[1])  # Bottom-right corner

        # 3. create the finder instance
        # finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

        # 4. find the path
        # Warning: This operation mutates the grid object internally
        path, runs = finder.find_path(start, end, grid)

        # optional: output the results
        print(f"Algorithm finished in {runs} iterations.")
        print("Path found:")

        # 5. convert node objects into readable (X, Y) coordinates
        clean_path = [(node.x, node.y) for node in path]
        print(clean_path)

        # optional: Visualize the grid map with the path drawn on it
        print("\nVisualized Grid Map:")
        print(grid.grid_str(path=path, start=start, end=end))

        # 6. visualize path:
        for i in range(1, len(clean_path) - 1):
            x = clean_path[i][1]
            y = clean_path[i][0]
            self.grid[x][y] = 4

        self.has_been_processed = True

    def reset_board(self) -> None:
        print("resetting the board")
        self.grid = self.initial_grid
        self.prepare_grid()
        print("done")
        self.print()
