import random
from pathlib import Path
import pyray as pr

THIS_DIR = (Path(__file__).parent.parent).resolve()

class TileData:
    def __init__(
            self, 
            render_pos: pr.Vector2, 
            tile_name: str, 
            tile_id: int, 
            grid_pos: dict[str: int]) -> None:
        self.render_pos = render_pos
        self.tile_name = tile_name
        self.tile_id = tile_id
        self.grid_pos = grid_pos

    def get_render_pos(self) -> pr.Vector2:
        return self.render_pos

    def get_tile_name(self) -> str:
        return self.tile_name

    def get_grid_pos_x(self) -> int:
        return self.grid_pos.get("tile_x")

    def get_grid_pos_y(self) -> int:
            return self.grid_pos.get("tile_y")

class World:
    def __init__(self, grid_length_x: int, grid_length_y: int, width: int, height: int):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.TILE_SIZE = 32
        # self.ground_tiles: list[TileData] = []
        self.ground_tiles: list[dict[str, pr.Vector2 | str]] = [] # ground level = 1st layer of tiles: grass, sand water or road
        self.additional_tiles: list[dict[str, pr.Vector2 | str]] = [] # upper level = 2nd layer of tiles: building
        self.world = self.create_world()

    def create_world(self) -> None:
        """
        - create a map by placing randomly textures
        """
        world = []
        tile_count = 0
        for grid_x in range(0, self.grid_length_x):
            world.append([])
            for grid_y in range(0, self.grid_length_y):
                world_tile = self.grid_to_world(grid_x=grid_x, grid_y=grid_y)
                world[grid_x].append(world_tile)

                # store all the ground tile in order to make only 1 draw call later on
                render_pos = world_tile.get("render_pos")
                tile_name = world_tile.get("tile")
                # tmp = TileData(
                #     render_pos=pr.Vector2(
                #         render_pos[0] + self.width // 2,
                #         render_pos[1] + self.height // 4),
                #     tile_name=tile_name,
                #     tile_id=tile_count, 
                #     grid_pos={"tile_x": grid_x, "tile_y": grid_y}
                # )
                # self.ground_tiles.append(tmp)
                self.ground_tiles.append(
                    {
                        "render_pos": pr.Vector2(
                            render_pos[0] + self.width // 2,
                            render_pos[1] + self.height // 4,
                        ),
                        "tile_name": tile_name,
                        "tile_id": tile_count,
                        "grid_pos": {"tile_x": grid_x, "tile_y": grid_y},
                    }
                )
                tile_count += 1
        return world

    def add_to_world(self, ui_element_name: str, tile_x: int, tile_y: int) -> None:
        """add a selected entity to the world map"""
        world_tile = self.grid_to_world(grid_x=tile_x + 1, grid_y=tile_y + 1)
        # testing: for road tiles, directly replace the tiles from the ground_tiles data
        if ui_element_name in [
            "road_top_right",
            "road_bottom_round",
            "road_bottom_right_T",
        ]:
            print("replacing ground tile with road")
            self.replace_ground_tile(ui_element_name, tile_x, tile_y)
        else:

            render_pos = world_tile.get("render_pos")
            tile_name = ui_element_name

            # tmp = TileData(
            #     render_pos=render_pos, 
            #     tile_name=tile_name,
            #     tile_id=len(self.additional_tiles), 
            #     grid_pos={"tile_x": tile_x + 1, "tile_y": tile_y + 1}
            # )
            # self.additional_tiles.append(tmp)

            self.additional_tiles.append(
                {
                    "render_pos": pr.Vector2(
                        render_pos[0] + self.width // 2,
                        render_pos[1]
                        + self.height // 4
                        - self.textures.get(tile_name).height,
                    ),
                    "tile_name": tile_name,
                }
            )
            # reorder the additional list by y ascending
            self.additional_tiles = sorted(
                self.additional_tiles, key=lambda x: x["render_pos"].y
            )

    def replace_ground_tile(
        self, ui_element_name: str, tile_x: int, tile_y: int
    ) -> None:
        world_tile = self.grid_to_world(grid_x=tile_x + 1, grid_y=tile_y + 1)
        render_pos = world_tile.get("render_pos")
        tile_name = ui_element_name
        for tile in self.ground_tiles:
            if (
                tile.get("grid_pos")["tile_x"] == tile_x
                and tile.get("grid_pos")["tile_y"] == tile_y
                # tile.get_grid_pos_x == tile_x
                # and tile.get_grid_pos_y == tile_y
            ):
                print("found tile")
                id = tile["tile_id"]

                # tmp = TileData(
                #     render_pos=pr.Vector2(
                #         render_pos[0] + self.width // 2,
                #         render_pos[1]
                #         + self.height // 4
                #         - self.textures.get(tile_name).height // 4
                #         - self.TILE_SIZE // 2,
                #     ),
                #     tile_name=tile_name,
                #     tile_id=id, 
                #     grid_pos={"tile_x": tile_x, "tile_y": tile_y},
                # )
                # self.ground_tiles[id] = tmp
                self.ground_tiles[id] = {
                    "render_pos": pr.Vector2(
                        render_pos[0] + self.width // 2,
                        render_pos[1]
                        + self.height // 4
                        - self.textures.get(tile_name).height // 4
                        - self.TILE_SIZE // 2,
                    ),
                    "tile_name": tile_name,
                    "tile_id": id,
                    "grid_pos": {"tile_x": tile_x, "tile_y": tile_y},
                }
        print(self.ground_tiles[0:5], len(self.ground_tiles))

    def draw(self, scroll: pr.Vector2):
        """draw all the floor tile in 1 draw call per frame"""
        if len(self.ground_tiles) == 0:
            return
        for tile in self.ground_tiles:
            tile_name = tile.get("tile_name")
            render_pos = tile.get("render_pos")
            # tile_name = tile.get_tile_name()
            # render_pos = tile.get_render_pos()
            if tile_name in ["sand", "grass"]:
                pr.draw_texture_v(
                    self.textures.get(tile_name),
                    pr.vector2_add(render_pos, scroll),
                    pr.WHITE,
                )
            else:
                # toggle this block to draw the water tile under ground level
                # need to decide
                pr.draw_texture_v(
                    self.textures.get(tile_name),
                    pr.vector2_add(
                        pr.Vector2(
                            render_pos.x,
                            render_pos.y
                            + -(
                                self.textures.get(tile_name).height // 2  ## 64x62 -> 31
                                - self.TILE_SIZE // 2
                                - 10  # fixed me later
                            ),
                        ),
                        scroll,
                    ),
                    pr.WHITE,
                )
        if len(self.additional_tiles) == 0:
            return
        for tile in self.additional_tiles:
            tile_name = tile.get("tile_name")
            render_pos = tile.get("render_pos")
            # if tile_name in ["sand2", "grass2", "water2", "sand", "grass"]:
            pr.draw_texture_v(
                self.textures.get(tile_name),
                pr.vector2_add(render_pos, scroll),
                pr.WHITE,
            )
            # else:
            #     pr.draw_texture_v(
            #         self.textures.get(tile_name),
            #         pr.vector2_add(
            #             pr.Vector2(
            #                 render_pos.x,
            #                 render_pos.y
            #                 + -(
            #                     self.textures.get(tile_name).height // 2  ## 64x62 -> 31
            #                     - self.TILE_SIZE // 2
            #                     - 10  # fixed me later
            #                 ),
            #             ),
            #             scroll,
            #         ),
            #         pr.WHITE,
            #     )

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
            (grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE),  # top left
            (
                grid_x * self.TILE_SIZE + self.TILE_SIZE,
                grid_y * self.TILE_SIZE,
            ),  # top right
            (
                grid_x * self.TILE_SIZE + self.TILE_SIZE,
                grid_y * self.TILE_SIZE + self.TILE_SIZE,
            ),  # bottom right
            (
                grid_x * self.TILE_SIZE,
                grid_y * self.TILE_SIZE + self.TILE_SIZE,
            ),  # bottom left
        ]

        # get the isometric coordinates of the tile
        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
        min_x = min([x for x, y in iso_poly])
        min_y = min([y for x, y in iso_poly])

        # associate a texture to this tile
        r = random.randint(1, 100)
        if r <= 5:
            tile = "water"
        elif r <= 10:
            tile = "sand"
        else:
            tile = "grass"

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
        kenney_sand = pr.load_texture(f"{THIS_DIR}/assets/landscapeTiles_059_64x64.png")
        kenney_water = pr.load_texture(
            f"{THIS_DIR}/assets/landscapeTiles_066_64x64.png"
        )
        kenney_grass = pr.load_texture(
            f"{THIS_DIR}/assets/landscapeTiles_067_64x64.png"
        )
        kenney_house = pr.load_texture(f"{THIS_DIR}/assets/buildingTiles_018_64x64.png")
        kenney_tree = pr.load_texture(f"{THIS_DIR}/assets/cityDetails_010.png")
        sand = pr.load_texture(f"{THIS_DIR}/assets/maroon_tile_no_border_64x64.png")
        water = pr.load_texture(f"{THIS_DIR}/assets/blue_tile_no_border_64x64.png")
        grass = pr.load_texture(f"{THIS_DIR}/assets/green_tile_no_border_64x64.png")
        building01 = pr.load_texture(f"{THIS_DIR}/assets/building01.png")
        building02 = pr.load_texture(f"{THIS_DIR}/assets/building02.png")
        road_top_right = pr.load_texture(f"{THIS_DIR}/assets/landscapeTiles_082.png")
        road_bottom_round = pr.load_texture(f"{THIS_DIR}/assets/landscapeTiles_127.png")
        road_bottom_right_T = pr.load_texture(
            f"{THIS_DIR}/assets/landscapeTiles_104.png"
        )
        self.textures = {
            "sand": kenney_sand,
            "water": kenney_water,
            "grass": kenney_grass,
            # "house": kenney_house,
            "building01": building01,
            "building02": building02,
            # "tree": kenney_tree,
            # "sand2": sand,
            # "water2": water,
            # "grass2": grass,
            "road_top_right": road_top_right,
            "road_bottom_round": road_bottom_round,
            "road_bottom_right_T": road_bottom_right_T,
        }

    def unload_textures(self) -> None:
        for k, v in self.textures.items():
            pr.unload_texture(v)
