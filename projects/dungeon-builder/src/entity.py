import pyray as pr
from .world import World


class Entity:
    def __init__(
        self,
        id: int,
        name: str,
        width: int,
        height: int,
        tile_x: int,
        tile_y: int,
        texture: pr.Texture,
        world: World,
    ) -> None:
        self.id = id
        self.name = name
        self.width = width
        self.height = height
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.texture = texture
        self.world = world

    def update(self) -> None:
        pass

    def draw(self, tile_x: int, tile_y: int, scroll: pr.Vector2) -> None:
        entity_tile = self.world.grid_to_world(grid_x=tile_x, grid_y=tile_y)
        render_pos = entity_tile.get("render_pos")
        tmp_pos = pr.Vector2(
            render_pos[0] + self.width // 2, render_pos[1] + self.height // 4
        )
        pr.draw_texture_v(
            self.texture,
            pr.vector2_add(tmp_pos, scroll),
            pr.WHITE,
        )