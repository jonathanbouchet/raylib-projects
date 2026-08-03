import pyray as pr


class TextureData:
    def __init__(self, name: str, texture: pr.Texture, is_buildable: bool) -> None:
        self.name = name
        self.texture = texture
        self.is_buildable = is_buildable

    def get_name(self) -> str:
        return self.name

    def get_texture(self) -> pr.Texture:
        return self.texture

    def get_buildable(self) -> bool:
        return self.is_buildable


class TileData:
    def __init__(
        self,
        render_pos: pr.Vector2,
        tile_name: str,
        tile_id: int,
        grid_pos: dict[str: int], # indexes of tile from 0 to grid_length, eg: 0 .. 14
        iso_rect: pr.Vector2,
        cart_rect: pr.Vector2,
    ) -> None:
        self.render_pos = render_pos
        self.tile_name = tile_name
        self.tile_id = tile_id
        self.grid_pos = grid_pos
        self.iso_rect = iso_rect
        self.cart_rect = cart_rect

    def get_render_pos(self) -> pr.Vector2:
        return self.render_pos

    def get_tile_name(self) -> str:
        return self.tile_name

    def get_grid_pos_x(self) -> int:
        return self.grid_pos.get("tile_x")

    def get_grid_pos_y(self) -> int:
        return self.grid_pos.get("tile_y")

    def get_tile_id(self) -> int:
        return self.tile_id

    def get_iso_rect(self) -> pr.Vector2:
        return self.iso_rect

    def get_cart_rect(self) -> pr.Vector2:
        return self.cart_rect

    def __str__(self) -> str:
        return f"""
        Tile ID: {self.get_tile_id()},
        name: {self.get_tile_name()}, 
        X: {self.get_grid_pos_x()},
        Y: {self.get_grid_pos_y()}"""