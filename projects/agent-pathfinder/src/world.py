import random
from pathlib import Path
import pyray as pr
from .tiles import TileData, LayerTile
from .utils import parse_map, parse_tileset, dict_texture_name_to_game

THIS_DIR = (Path(__file__).parent.parent).resolve()


class World:
    def __init__(
        self,
        grid_length_x: int,
        grid_length_y: int,
        width: int,
        height: int,
        textures,
    ):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.textures = textures
        self.TILE_SIZE = 64
        self.ground_tiles: list[TileData] = []
        # self.create_world()

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
                world_tile = self.grid_to_world(
                    tile_type=LayerTile.ground, grid_x=grid_x, grid_y=grid_y
                )
                render_pos = world_tile.get("render_pos")
                tile_name = world_tile.get("tile")
                cart_rect = world_tile.get("cart_rect")
                texture_id = world_tile.get("texture_id")
                path = world_tile.get("path")

                # instantiate a TileData class
                tmp = TileData(
                    render_pos=render_pos,
                    tile_name=tile_name,
                    tile_id=tile_count,
                    grid_pos={"tile_x": grid_x, "tile_y": grid_y},
                    cart_rect=cart_rect,
                    texture_id=texture_id,
                    path=path,
                )
                self.ground_tiles.append(tmp)
                tile_count += 1

    def draw_grid(self) -> None:
        for x in range(0, self.grid_length_x + 1):
            pr.draw_line_ex(
                pr.Vector2(x * self.TILE_SIZE, 0),
                pr.Vector2(x * self.TILE_SIZE, self.grid_length_y * self.TILE_SIZE),
                2,
                pr.BLUE,
            )
        for y in range(0, self.grid_length_y + 1):
            pr.draw_line_ex(
                pr.Vector2(0, y * self.TILE_SIZE, 0),
                pr.Vector2(self.grid_length_x * self.TILE_SIZE, y * self.TILE_SIZE),
                2,
                pr.BLUE,
            )

    def draw_ground(self):
        """draw all the floor tile in 1 draw call per frame"""
        for tile in self.ground_tiles:
            tile_name = tile.get_tile_name()
            pr.draw_texture_v(
                self.textures.get(tile_name)["texture"], tile.get_render_pos(), pr.WHITE
            )

    def grid_to_world(
        self, tile_type: LayerTile, grid_x: int, grid_y: int, name_from_map: str = None
    ) -> dict[str, list[int, int] | list[tuple[int, int]]]:
        """
        - return for each tile its data / info:
            1. cartesian coords
            2. associated texture
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

        if tile_type == LayerTile.ground:
            tile = self.map1(grid_x=grid_x, grid_y=grid_y)
        elif tile_type == LayerTile.prebuilt:
            tile = dict_texture_name_to_game.get(name_from_map)
            print(f"{name_from_map=}, {tile=}")

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "render_pos": pr.Vector2(grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE),
            "tile": tile,
            "texture_id": self.textures.get(tile)["id"],
            "path": self.textures.get(tile)["path"],
        }
        return out

    def map1(self, grid_x, grid_y) -> str:
        tilename: str = ""
        if (grid_x > 1 and grid_x < 6) and (grid_y == 1 or grid_y == 6):
            tilename = "straight_L_R"
        elif (grid_y > 1 and grid_y < 6) and (grid_x == 1 or grid_x == 6):
            tilename = "straight_T_B"
        elif grid_x == 1 and grid_y == 1:
            tilename = "curve_B_R"
        elif grid_x == 6 and grid_y == 1:
            tilename = "curve_L_B"
        elif grid_x == 1 and grid_y == 6:
            tilename = "curve_T_R"
        elif grid_x == 6 and grid_y == 6:
            tilename = "curve_L_T"
        else:
            tilename = random.choice(["grass", "dirt"])
        return tilename

    def make_path(self) -> list[pr.Vector2]:
        """
        - a path is build by adding all the paths data for each tile in the map
        - example: "path": [pr.Vector2(0, 32), pr.Vector2(20, 40), pr.Vector2(32, 64)]
        - because some are common to multiple tile, the initial list: 'markers' needd to be deduped to return only the single values
        - finally each marker is converted to a Vector2
        """
        markers = []
        for tile in self.ground_tiles:
            if tile.get_tile_name() in [
                "curve_L_B",
                "curve_L_T",
                "curve_B_R",
                "curve_T_R",
                "straight_L_R",
                "straight_T_B",
            ]:
                grid_x, grid_y = tile.get_grid_tile_x(), tile.get_grid_tile_y()
                paths = tile.get_path()
                for p in paths:
                    point = pr.vector2_add(
                        p,
                        pr.Vector2(
                            int(grid_x * self.TILE_SIZE), int(grid_y * self.TILE_SIZE)
                        ),
                    )
                    markers.append([int(point.x), int(point.y)])
        markers = [list(x) for x in set(tuple(inner) for inner in markers)]
        return [pr.Vector2(d[0], d[1]) for d in markers]

    def draw_path(self) -> None:
        """
        - this method is to draw the path of a single tile
        - for the straight road segments, there are only 2 markers
        - for the curve segments, there are 3 markers
        """
        for tile in self.ground_tiles:
            if tile.get_tile_name() in [
                "curve_L_B",
                "curve_L_T",
                "curve_B_R",
                "curve_T_R",
                "straight_L_R",
                "straight_T_B",
            ]:
                grid_x, grid_y = tile.get_grid_tile_x(), tile.get_grid_tile_y()
                paths = tile.get_path()
                for i in range(0, 2):
                    start = pr.vector2_add(
                        tile.get_path()[i],
                        pr.Vector2(grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE),
                    )
                    end = pr.vector2_add(
                        tile.get_path()[i + 1],
                        pr.Vector2(grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE),
                    )
                    pr.draw_line_ex(start, end, 1, pr.RED)
                for p in paths:
                    point = pr.vector2_add(
                        p,
                        pr.Vector2(grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE),
                    )
                    pr.draw_rectangle_v(point, pr.Vector2(5, 5), pr.RED)

    def load_map(self, map_data: str, tileset: str):
        # tileset
        tileset_name = f"{THIS_DIR}/assets/maps/{tileset}"
        print(f"{tileset_name=}")
        tileset = parse_tileset(tileset_name=tileset_name)
        textures_data = tileset.get("tileset")["tile"]
        textures_list = []
        for texture in textures_data:
            texture_dict = {
                "id": int(texture.get("@id")),
                "source": texture.get("image")["@source"]
                .split("agent-pathfinder/")[-1]
                .split("assets/")[-1],
                "width": texture.get("image")["@width"],
                "height": texture.get("image")["@height"],
            }
            textures_list.append(texture_dict)
        print(f"{textures_list=}")

        map_name = f"{THIS_DIR}/assets/maps/{map_data}"
        print(f"{map_name=}")
        map = parse_map(map_name=map_name)
        layers = map.get("layers")
        print(f"number of layers: {len(layers)}")
        layers_data = []
        for layer in layers:
            layer_name = layer.get("name")
            width, height = layer.get("width"), layer.get("width")
            data = layer.get("data")
            layers_data.append(
                {"name": layer_name, "width": width, "height": height, "data": data}
            )
            # transpose y->x data
            # data_1 = np.array(data).reshape(width, height)
            # data_2 = data_1.transpose()
            # data_3 = data_2.reshape(-1)
            # data_4 = data_3.tolist()
            # layers_data.append(
            #     {"name": layer_name, "width": width, "height": height, "data": data_4}
            # )
            # data = layer.get("data")

            tile_count = 0
            tileset = textures_list
            for grid_y in range(0, self.grid_length_y):
                for grid_x in range(0, self.grid_length_x):
                    if data[tile_count] > 0:
                        texture_id = (
                            data[tile_count] - 1
                        )  # reminder: subtract 1 to reference tileset
                        print(f"{texture_id=}")
                        # temporary overwrite the name of the tile
                        tmp = tileset[texture_id].get("source")
                        world_tile = self.grid_to_world(
                            tile_type=LayerTile.prebuilt,
                            grid_x=grid_x,
                            grid_y=grid_y,
                            name_from_map=tmp,
                        )

                        render_pos = world_tile.get("render_pos")
                        tile_name = world_tile.get("tile")
                        cart_rect = world_tile.get("cart_rect")
                        texture_id = world_tile.get("texture_id")
                        path = world_tile.get("path")
                        # instantiate a TileData class
                        tmp_tile = TileData(
                            render_pos=render_pos,
                            tile_name=tile_name,
                            tile_id=tile_count,
                            grid_pos={"tile_x": grid_x, "tile_y": grid_y},
                            cart_rect=cart_rect,
                            texture_id=texture_id,
                            path=path,
                        )
                        self.ground_tiles.append(tmp_tile)
                        tile_count += 1

    def unload_textures(self) -> None:
        for k, v in self.textures.items():
            pr.unload_texture(v.get("texture"))
