from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.dijkstra import DijkstraFinder
from pathfinding.finder.breadth_first import BreadthFirstFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from simple_board import BaseBoard


class PathFinder(BaseBoard):
    def __init__(
        self,
        num_rows: int,
        num_cols: int,
        cell_size: int,
        pathfinder_name: str,
        obstacle: str,
    ):
        super().__init__(num_rows=num_rows, num_cols=num_cols, cell_size=cell_size)
        self.pathfinder_name: str = pathfinder_name
        self.pathfinder_obstacle: str = obstacle
        self.pathfinder = None
        self.setpathfinder()

    def setpathfinder(self):
        obstacles = self.set_obstacle()
        if self.pathfinder_name == "a_star":
            self.pathfinder = AStarFinder(diagonal_movement=obstacles)
        elif self.pathfinder_name == "breadth_first":
            self.pathfinder = BreadthFirstFinder(diagonal_movement=obstacles)
        elif self.pathfinder_name == "dijkstra":
            self.pathfinder = DijkstraFinder(diagonal_movement=obstacles)

    def set_obstacle(self):
        if self.pathfinder_obstacle == "always":
            return DiagonalMovement.always
        elif self.pathfinder_obstacle == "if_at_most_one_obstacleays":
            return DiagonalMovement.if_at_most_one_obstacle
        elif self.pathfinder_obstacle == "mro":
            return DiagonalMovement.mro
        elif self.pathfinder_obstacle == "never":
            return DiagonalMovement.never
        elif self.pathfinder_obstacle == "only_when_no_obstacle  ":
            return DiagonalMovement.only_when_no_obstacle

    def __str__(self) -> str:
        return f"{self.pathfinder}"
