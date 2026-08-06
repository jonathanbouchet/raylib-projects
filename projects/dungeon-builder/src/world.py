import random
from pathlib import Path
import pyray as pr
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from .tiles import TileData, LayerTile

THIS_DIR = (Path(__file__).parent.parent).resolve()

class World:
    def __init__(self, grid_length_x: int, grid_length_y: int, width: int, height: int, origin: pr.Vector2):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.origin: pr.Vector2 = origin
        self.TILE_SIZE = 64 # should be real TILE_SIZE_WIDTH / 2
        self.ground_tiles: list[TileData] = []
        self.props_tiles: list[TileData] = []
        self.entity_tiles: list[TileData] = []
        self.create_world()
        self.add_props_world()
        self.print_props_grid()

    def create_world(self) -> None:
        """
        - the grid is now filled accordingly pathfinder algo, ie, the values for grid_x are filled first 
        - then the loop is done by the grid_y:
        - [
            [0,1,2], # y=0
            [3,4,5], # y=1
            ...    , 
          ]
        """
        tile_count: int = 0
        for grid_y in range(0, self.grid_length_y):
            for grid_x in range(0, self.grid_length_x):
                world_tile = self.grid_to_world(tile_type=LayerTile.ground,grid_x=grid_x, grid_y=grid_y)
                render_pos = world_tile.get("render_pos")
                tile_name = world_tile.get("tile")
                iso_rect = world_tile.get("iso_rect")
                cart_rect = world_tile.get("cart_rect")

                # instantiate a TileData class
                # note: the global transformation screen.width//2, screen.height//4 to recenter the tiles is applied here
                tmp = TileData(
                    render_pos=pr.Vector2(
                        render_pos[0] + self.width // 2,
                        render_pos[1] + self.height // 4,
                    ),
                    tile_name=tile_name,
                    tile_id=tile_count,
                    grid_pos={"tile_x": grid_x, "tile_y": grid_y},
                    iso_rect=iso_rect,
                    cart_rect=cart_rect,
                )
                self.ground_tiles.append(tmp)
                tile_count += 1

    def add_props_world(self)-> None:
        tile_count: int = 0
        for grid_y in range(0, self.grid_length_y):
            for grid_x in range(0, self.grid_length_x):
                world_tile = self.grid_to_world(tile_type=LayerTile.props, grid_x=grid_x, grid_y=grid_y)
                render_pos = world_tile.get("render_pos")
                tile_name = world_tile.get("tile")
                iso_rect = world_tile.get("iso_rect")
                cart_rect = world_tile.get("cart_rect")

                # instantiate a TileData class
                # note: the global transformation screen.width//2, screen.height//4 to recenter the tiles is applied here
                tmp = TileData(
                    render_pos=pr.Vector2(
                        render_pos[0] + self.width // 2,
                        render_pos[1] + self.height // 4,
                    ),
                    tile_name=tile_name,
                    tile_id=tile_count,
                    grid_pos={"tile_x": grid_x, "tile_y": grid_y},
                    iso_rect=iso_rect,
                    cart_rect=cart_rect,
                )
                self.props_tiles.append(tmp)
                tile_count += 1

    def find_path(self, grid_x: int, grid_y: int) -> None:
        # 1. instantiate the grid object: 1's are walkable tiles, 0's are non walkable
        # in our case, these values come from the props_tiles
        data = np.array([0 if t.tile_name is not None else 1 for t in self.props_tiles]).reshape(self.grid_length_x, self.grid_length_y)
        print(f"{data=}")
        grid = Grid(matrix=data)
        print(f"{grid=}")

        # 2. define the start and end nodes (X, Y format)
        start = grid.node(grid_x, grid_y)
        end = grid.node(self.grid_length_x - 1, self.grid_length_y - 1)  # Bottom-right corner

        # 3. create the finder instance
        # finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

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
        

    def draw_floor(self, scroll: pr.Vector2):
        """draw all the floor tile in 1 draw call per frame"""
        for tile in self.ground_tiles:
            tile_name = tile.get_tile_name()
            render_pos = tile.get_render_pos()
            
            pr.draw_texture_v(
                self.textures.get(tile_name), 
                pr.Vector2(
                    render_pos.x + self.origin.x + scroll.x,
                    render_pos.y - (128 + self.TILE_SIZE - 10) 
                    + self.origin.y + scroll.y 
                    ), 
                pr.WHITE
            )

    def draw_props(self, scroll: pr.Vector2):
        """draw all the floor tile in 1 draw call per frame"""
        for tile in self.props_tiles:
            tile_name = tile.get_tile_name()
            render_pos = tile.get_render_pos()

            if tile_name is not None:
                pr.draw_texture_v(
                    self.textures.get(tile_name), 
                    pr.Vector2(
                        render_pos.x + self.origin.x + scroll.x,
                        render_pos.y - (128 + self.TILE_SIZE)
                        + self.origin.y + scroll.y 
                        ), 
                    pr.WHITE
                )

    def grid_to_world(
        self, tile_type: LayerTile, grid_x: int, grid_y: int
    ) -> dict[str, list[int, int] | list[tuple[int, int]]]:
        """
        - return for each tile its data / info:
            1. cartesian coords
            2. isometric coords
            3. associated texture
        """
        # get the cartesian coordinates of the tile
        rect = [
            (grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE), # top left
            (grid_x * self.TILE_SIZE + self.TILE_SIZE, grid_y * self.TILE_SIZE), # top right
            (
                grid_x * self.TILE_SIZE + self.TILE_SIZE,
                grid_y * self.TILE_SIZE + self.TILE_SIZE,
            ), # bottom right
            (grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE + self.TILE_SIZE), # bottom left
        ]

        # get the isometric coordinates of the tile
        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
        min_x = min([x for x, y in iso_poly])
        min_y = min([y for x, y in iso_poly])

        if tile_type == LayerTile.ground:
            r = random.randint(1, 100)
            if r <= 10:
                tile = "dirt_W"
            elif r <= 50:
                tile = "stone_E"
            else:
                tile = "stone_W"
            out = {
                "grid": [grid_x, grid_y],
                "cart_rect": rect,
                "iso_rect": iso_poly,
                "render_pos": [min_x, min_y],
                "tile": tile,
            }
        elif tile_type == LayerTile.props:
            if grid_x == self.grid_length_x - 1 and grid_y == self.grid_length_y - 1:
                tile = None # reserve the last tile of the grid empty
            else:
                r = random.randint(1, 100)
                if r <= 5:
                    tile = "stoneWallCorner_E"
                elif r <= 10:
                    tile = "stoneWallArchway_N"
                elif r <= 15:
                    tile = "stoneColumn_N"
                else:
                    tile = None
        else:
            print(f"tile_type not found: {tile_type}")
            tile = None

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_rect": iso_poly,
            "render_pos": [min_x, min_y],
            "tile": tile,
        }
        return out

    def cart_to_iso(self, x, y):
        """convert from cartesian to isometric coordinates"""
        iso_x = x - y
        iso_y = (x + y) // 2
        return iso_x, iso_y

    def load_textures(self):
        """load textures used throughout the game"""
        stone_E = pr.load_texture(f"{THIS_DIR}/assets/stone_E.png")
        stone_W = pr.load_texture(f"{THIS_DIR}/assets/stone_W.png")
        stone_N = pr.load_texture(f"{THIS_DIR}/assets/stone_N.png")
        stone_S = pr.load_texture(f"{THIS_DIR}/assets/stone_S.png")
        dirt_W = pr.load_texture(f"{THIS_DIR}/assets/dirt_W.png")
        stoneWallArchway_N = pr.load_texture(f"{THIS_DIR}/assets/stoneWallArchway_N.png")
        stoneColumn_N = pr.load_texture(f"{THIS_DIR}/assets/stoneColumn_N.png")
        Male_4_Idle0 = pr.load_texture(f"{THIS_DIR}/assets/Male_4_Idle0.png")
        stoneWallCorner_E = pr.load_texture(f"{THIS_DIR}/assets/stoneWallCorner_E.png")
        
        self.textures = {
            "stone_E": stone_E,
            "stone_W": stone_W,
            "stone_N": stone_N,
            "stone_S": stone_S,
            "dirt_W": dirt_W,
            "stoneWallArchway_N": stoneWallArchway_N,
            "stoneColumn_N": stoneColumn_N,
            "Male_4_Idle0": Male_4_Idle0,
            "stoneWallCorner_E": stoneWallCorner_E
            }

    def unload_textures(self) -> None:
        for k,v in self.textures.items():
            pr.unload_texture(v)

    def print_props_grid(self) -> None:
        data_0 = np.array(['x' if t.tile_name is not None else 'o' for t in self.props_tiles])
        data = data_0.reshape(self.grid_length_x, self.grid_length_y)
        data_grid_fl = data.reshape(-1)
        data_grid_fl_2 = data_grid_fl.tolist()

        cols = self.grid_length_x
        for i in range(0, len(data_grid_fl_2), cols):
            row = data_grid_fl_2[i : i + cols]
            print("".join(f"{str(item):<2}" for item in row))

    def clear_world(self) -> None:
        self.ground_tiles.clear()
        self.props_tiles.clear()
