import pyray as pr
from enum import Enum


class LayerTile(Enum):
    ground = 0
    props = 1
    entity = 2


class TileData:
    def __init__(
        self,
        texture_id: int,
        render_pos: pr.Vector2,
        tile_name: str,
        tile_id: int,
        grid_pos: dict[str:int],  # indexes of tile from 0 to grid_length, eg: 0 .. 14
        cart_rect: pr.Vector2,
        path: list[pr.Vector2],
    ) -> None:
        self.texture_id = texture_id
        self.render_pos = render_pos
        self.tile_name = tile_name
        self.tile_id = tile_id
        self.grid_pos = grid_pos
        self.cart_rect = cart_rect
        self.path = path

    def get_render_pos(self) -> pr.Vector2:
        return self.render_pos

    def get_tile_name(self) -> str:
        return self.tile_name

    def get_grid_tile_x(self) -> int:
        return self.grid_pos.get("tile_x")

    def get_grid_tile_y(self) -> int:
        return self.grid_pos.get("tile_y")

    def get_tile_id(self) -> int:
        return self.tile_id

    def get_cart_rect(self) -> pr.Vector2:
        return self.cart_rect

    def get_path(self) -> list[pr.Vector2]:
        return self.path

    def __str__(self) -> str:
        return f"""
        Tile ID: {self.get_tile_id()},
        name: {self.get_tile_name()}, 
        X: {self.get_grid_tile_x()},
        Y: {self.get_grid_tile_y()}
        path:{self.get_path()}"""
