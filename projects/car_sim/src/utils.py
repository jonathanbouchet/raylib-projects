from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.dijkstra import DijkstraFinder
from pathfinding.finder.breadth_first import BreadthFirstFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

def find_path(board, player_pos, target) -> tuple[int, int]:
        # 1. instantiate the grid object
        grid = Grid(matrix=board)

        # 2. define the start and end nodes (X, Y format)
        start = grid.node(player_pos[0], player_pos[1])
        end = grid.node(target[0], target[1])

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

        # 6. save path
        path_vals = []
        for i in range(1, len(clean_path) - 1):
            x = clean_path[i][1]
            y = clean_path[i][0]
            path_vals.append([x, y])
        
        return path_vals


