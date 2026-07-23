import random
from pathlib import Path
import pyray as pr

THIS_DIR = (Path(__file__).parent.parent).resolve()

class World:
    def __init__(self, grid_length_x: int, grid_length_y: int, width: int, height: int):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.TILE_SIZE = 32
        self.world = self.create_world()

    def create_world(self) -> None:
        """
        - create a map by placing randomly tree and rock textures
        - grass (`block`) are placed for evry tile automatically as the `floor`
        """
        world = []
        for grid_x in range(0, self.grid_length_x):
            world.append([])
            for grid_y in range(0, self.grid_length_y):
                world_tile = self.grid_to_world(grid_x=grid_x, grid_y=grid_y)
                world[grid_x].append(world_tile)
        return world

    def grid_to_world(
        self, grid_x: int, grid_y: int
    ) -> dict[str, list[int, int] | list[tuple[int, int]]]:
        """
        - return for each tile its data / info:
            1. cartesian coords
            2. isometric coords
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

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_rect": iso_poly,
            "render_pos": [min_x, min_y],
        }
        return out

    def cart_to_iso(self, x, y):
        """convert from cartesian to isometric coordinates"""
        iso_x = x - y
        iso_y = (x + y) // 2
        return iso_x, iso_y

    def load_textures(self):
        """load textures used throughout the game"""
        kenney_sand = pr.load_texture(f"{THIS_DIR}/assets/landscapeTiles_059_64x64.png")
        kenney_house = pr.load_texture(f"{THIS_DIR}/assets/buildingTiles_018_64x64.png")
        kenney_tree = pr.load_texture(f"{THIS_DIR}/assets/cityDetails_010.png")
        self.textures = {
            "sand": kenney_sand,
            "house": kenney_house,
            "tree": kenney_tree
            }

    def unload_textures(self) -> None:
        for k,v in self.textures.items():
            pr.unload_texture(v)

