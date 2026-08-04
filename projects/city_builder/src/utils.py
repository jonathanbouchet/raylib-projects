import json
import xmltodict
from .tiles import TileData
import pyray as pr

TILE_SIZE = 32


def parse_map(map_name: str):
    print(map_name)
    with open(map_name, "r") as f:
        map_dict = json.load(f)
    return map_dict


def parse_tileset(tileset_name: str):
    with open(tileset_name, "r", encoding="utf-8") as f:
        data_dict = xmltodict.parse(f.read())
    return data_dict


def cart_to_iso(x, y):
    """convert from cartesian to isometric coordinates"""
    iso_x = x - y
    iso_y = (x + y) // 2
    return iso_x, iso_y


def grid_to_world(
    grid_x: int, grid_y: int
) -> dict[str, list[int, int] | list[tuple[int, int]]]:
    """
    - return for each tile its data / info:
        1. cartesian coords
        2. isometric coords
    """
    # get the cartesian coordinates of the tile
    rect = [
        (grid_x * TILE_SIZE, grid_y * TILE_SIZE),  # top left
        (
            grid_x * TILE_SIZE + TILE_SIZE,
            grid_y * TILE_SIZE,
        ),  # top right
        (
            grid_x * TILE_SIZE + TILE_SIZE,
            grid_y * TILE_SIZE + TILE_SIZE,
        ),  # bottom right
        (
            grid_x * TILE_SIZE,
            grid_y * TILE_SIZE + TILE_SIZE,
        ),  # bottom left
    ]

    # get the isometric coordinates of the tile
    iso_poly = [cart_to_iso(x, y) for x, y in rect]
    min_x = min([x for x, y in iso_poly])
    min_y = min([y for x, y in iso_poly])

    out = {
        "grid": [grid_x, grid_y],
        "cart_rect": rect,
        "iso_rect": iso_poly,
        "render_pos": [min_x, min_y],
    }
    return out


def process_layer(
    data: list[int],
    grid_len_x: int,
    grid_len_y: int,
    tileset: dict,
    map_textures_dict: dict[str, str],
) -> dict:
    WIDTH = 1080
    HEIGHT = 720
    print(f"{map_textures_dict=}")
    print(f"{tileset=}")
    ground_tiles: list[TileData] = []
    tile_cnt = 0
    for grid_x in range(0, grid_len_x):
        for grid_y in range(0, grid_len_y):
            if data[tile_cnt]>0:
                texture_id = data[tile_cnt] - 1  # reminder: subtract 1 to reference tileset
                tile = grid_to_world(grid_x=grid_x, grid_y=grid_y)
                tile["tile"] = tileset[texture_id].get("source")

                # get the tiles indexes to isometric/cartesian data
                render_pos = tile.get("render_pos")
                tile_name = tile.get("tile")
                iso_rect = tile.get("iso_rect")
                cart_rect = tile.get("cart_rect")

                if tile.get("tile") in map_textures_dict.keys():
                    tile_name = map_textures_dict.get(tile.get("tile"))
            # else:
            #     # default tile
            #     print(f"tile not found: {tile.get('tile')}")
            #     tile_name = "grass"

                # instantiate a TileData class
                tmp = TileData(
                    render_pos=pr.Vector2(
                        render_pos[0] + WIDTH // 2, 
                        render_pos[1] + HEIGHT // 4,
                    ),
                    tile_name=tile_name,
                    tile_id=tile_cnt,
                    grid_pos={"tile_x": grid_x, "tile_y": grid_y},
                    iso_rect=iso_rect,
                    cart_rect=cart_rect,
                )
                ground_tiles.append(tmp)
            tile_cnt += 1

    return ground_tiles
