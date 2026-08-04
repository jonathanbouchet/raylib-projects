import random
import numpy as np
from pathlib import Path
import pyray as pr
from .tiles import TextureData, TileData
from .utils import parse_map, parse_tileset, process_layer

THIS_DIR = (Path(__file__).parent.parent).resolve()


class World:
    def __init__(
        self,
        grid_length_x: int,
        grid_length_y: int,
        width: int,
        height: int,
        map_data: dict[str, dict[str, str]],
        map_textures_dict: dict[str, str],
    ):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.map_textures_dict = map_textures_dict
        self.TILE_SIZE = 32
        self.ground_tiles: list[
            TileData
        ] = []  # ground level = 1st layer of tiles: grass, sand water or road
        self.additional_tiles: list[
            TileData
        ] = []  # upper level = 2nd layer of tiles: building
        # self.load_world(map_data=map_data)
        self.create_world()

    def load_world(self, map_data: dict[str, dict[str, str]]):
        # tileset
        tileset_name = f"{THIS_DIR}/{map_data.get('tileset')}"
        print(f"{tileset_name=}")
        tileset = parse_tileset(tileset_name=tileset_name)
        textures_data = tileset.get("tileset")["tile"]
        textures_list = []
        for texture in textures_data:
            texture_dict = {
                "id": int(texture.get("@id")),
                "source": texture.get("image")["@source"].split("city_builder/")[-1],
                "width": texture.get("image")["@width"],
                "height": texture.get("image")["@height"],
            }
            textures_list.append(texture_dict)

        print(f"{textures_list=}")

        # map
        # a. building layer:
        #   - if index is 0 -> no tile
        #   - otherwise, index needs to be subtracted by 1 when referencing the textures_list
        # b. ground layer:
        #   - index needs to be subtracted by 1 when referencing the textures_list

        map_name = f"{THIS_DIR}/{map_data.get('map')}"
        print(f"{map_name=}")
        map = parse_map(map_name=map_name)
        layers = map.get("layers")
        print(f"number of layers: {len(layers)}")
        layers_data = []
        for layer in layers:
            layer_name = layer.get("name")
            width, height = layer.get("width"), layer.get("width")
            data = layer.get("data")
            # transpose y->x data
            data_1 = np.array(data).reshape(width, height)
            data_2 = data_1.transpose()
            data_3 = data_2.reshape(-1)
            data_4 = data_3.tolist()
            layers_data.append(
                {"name": layer_name, "width": width, "height": height, "data": data_4}
            )

        for layer in layers_data:
            print(layer.get("name"), layer.get("width"), layer.get("height"))
            if layer.get("name") == "ground_tiles":
                res = process_layer(
                    data=layer.get("data"),
                    grid_len_x=width,
                    grid_len_y=height,
                    tileset=textures_list,
                    map_textures_dict=self.map_textures_dict,
                )
                self.ground_tiles = res
            if layer.get("name") == "road_tiles":
                res = process_layer(
                    data=layer.get("data"),
                    grid_len_x=width,
                    grid_len_y=height,
                    tileset=textures_list,
                    map_textures_dict=self.map_textures_dict,
                )
                self.additional_tiles = res

    def create_world(self) -> None:
        """
        - create a map by placing randomly textures
        - loop is y descending then x ascending
        """
        tile_count = 0
        for grid_x in range(0, self.grid_length_x):
            for grid_y in range(0, self.grid_length_y):
                # get the tiles indexes to isometric/cartesian data
                world_tile = self.grid_to_world(grid_x=grid_x, grid_y=grid_y)
                render_pos = world_tile.get("render_pos")
                tile_name = world_tile.get("tile")
                iso_rect = world_tile.get("iso_rect")
                cart_rect = world_tile.get("cart_rect")

                # instantiate a TileData class
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

    def add_to_world(self, ui_element_name: str, tile_x: int, tile_y: int) -> None:
        """
        - add a selected UI element to the world map
        - retrieve texture data by its name: ui_element_name and grid_position: tile_x, tile_y
        - how it works:
            - if tile is one of the road segments, the original tile is simply replaced
            - if the tile is one of the buildings, the original tile is kept and the new tile is added to another grid ("additional_tiles")
        """
        if ui_element_name in [
            "road_top_right",
            "road_bottom_round",
            "road_bottom_right_T",
            "road_bottom_right",
            "road_crossing",
            "road_top_left_T",
            "road_bottom_left_T",
            "road_top_right_T",
            "road_top_T_shape",
            "road_bottom_T_shape",
            "road_left_T_shape",
            "road_right_T_shape",
        ]:
            print("replacing ground tile with road")
            self.replace_ground_tile(ui_element_name, tile_x, tile_y)
        else:
            print(f"adding ground tile with building: {ui_element_name}")
            new_tile_x = tile_x + 1
            new_tile_y = tile_y + 1
            world_tile = self.grid_to_world(grid_x=new_tile_x, grid_y=new_tile_y)
            render_pos = world_tile.get("render_pos")
            tile_name = ui_element_name

            tmp = TileData(
                render_pos=pr.Vector2(
                    render_pos[0] + self.width // 2,
                    render_pos[1]
                    + self.height // 4
                    - self.textures.get(tile_name).get_texture().height,
                ),
                tile_name=tile_name,
                tile_id=len(self.additional_tiles),
                grid_pos={"tile_x": tile_x, "tile_y": tile_y},
                iso_rect=world_tile.get("iso_rect"),
                cart_rect=world_tile.get("cart_rect"),
            )
            print(tmp)
            self.additional_tiles.append(tmp)
            # self.additional_tiles.insert(tile_x*self.grid_length_x + tile_y, tmp)
            # sort tiles by y ascending
            self.additional_tiles = sorted(
                self.additional_tiles, key=lambda x: x.get_render_pos().y
            )

    def replace_ground_tile(
        self, ui_element_name: str, tile_x: int, tile_y: int
    ) -> None:
        world_tile = self.grid_to_world(grid_x=tile_x, grid_y=tile_y)
        render_pos = world_tile.get("render_pos")
        tile_name = ui_element_name
        for tile in self.ground_tiles:
            if tile.get_grid_pos_x() == tile_x and tile.get_grid_pos_y() == tile_y:
                print("found tile")
                id = tile.get_tile_id()

                tmp = TileData(
                    render_pos=pr.Vector2(
                        render_pos[0] + self.width // 2,
                        render_pos[1] + self.height // 4,
                        # - self.textures.get(tile_name).height // 4
                        # - self.textures.get(tile_name).get_texture().height //4
                        # - self.TILE_SIZE // 2,
                    ),
                    tile_name=tile_name,
                    tile_id=id,
                    grid_pos={"tile_x": tile_x, "tile_y": tile_y},
                    iso_rect=world_tile.get("iso_rect"),
                    cart_rect=world_tile.get("cart_rect"),
                )
                self.ground_tiles[id] = tmp
        print(self.ground_tiles[0:5], len(self.ground_tiles))

    def draw(self, scroll: pr.Vector2):
        """
        - draw world tiles
        - how it works:
            - first the ground_tiles(grass, sand, water or road segments) are drawn ; using ground_tiles list
                - there is a special case for the water tile because the original texture has a different height
            - then the buildings are drawn using additional_tiles list
        - Take ito account the camera scrolling effect
        """
        if len(self.ground_tiles) == 0:
            return
        for tile in self.ground_tiles:
            tile_name = tile.get_tile_name()
            render_pos = tile.get_render_pos()
            if tile_name in ["sand", "grass"]:
                pr.draw_texture_v(
                    self.textures.get(tile_name).get_texture(),
                    pr.vector2_add(render_pos, scroll),
                    pr.WHITE,
                )
            else:
                # toggle this block to offset the water tile under ground level
                # need to decide
                pr.draw_texture_v(
                    self.textures.get(tile_name).get_texture(),
                    pr.vector2_add(
                        pr.Vector2(
                            render_pos.x,
                            render_pos.y
                            + -(
                                self.textures.get(tile_name).get_texture().height
                                // 2  ## 64x62 -> 31
                                - self.TILE_SIZE // 2
                                - 12  # fixed me later
                            ),
                        ),
                        scroll,
                    ),
                    pr.WHITE,
                )
        if len(self.additional_tiles) == 0:
            return
        for tile in self.additional_tiles:
            if tile is not None:
                tile_name = tile.get_tile_name()
                render_pos = tile.get_render_pos()
                pr.draw_texture_v(
                    self.textures.get(tile_name).get_texture(),
                    pr.vector2_add(render_pos, scroll),
                    pr.WHITE,
                )

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

    def get_ground_tile_status(self, x: int, y) -> TileData:
        pass

    def cart_to_iso(self, x, y):
        """convert from cartesian to isometric coordinates"""
        iso_x = x - y
        iso_y = (x + y) // 2
        return iso_x, iso_y

    def load_textures(self, textures_data_path: dict[str, str]):
        """load textures used throughout the game"""
        textures = {}
        for texture_name, texture_path in textures_data_path.items():
            textures[texture_name] = TextureData(
                name=texture_name,
                texture=pr.load_texture(f"{THIS_DIR}/{texture_path.get('path')}"),
                is_buildable=texture_path.get("is_buildable"),
            )
        self.textures: dict[str:TextureData] = textures

    def unload_textures(self) -> None:
        for k, v in self.textures.items():
            pr.unload_texture(v.get_texture())
