import pyray as pr
import raylib as rl
from .sprite import BaseSprite


class Player(BaseSprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        v1: pr.Vector3,
        v2: pr.Vector3,
        v3: pr.Vector3,
        speed: float,
        rotation_speed: float,
        scale: float,
        color: pr.Color,
        debug: bool,
        debug_color,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            speed=speed,
            rotation_speed=rotation_speed,
            scale=scale,
            color=color,
            debug=debug,
            debug_color=debug_color,
        )
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        # compute centroid and store local verts (never modify)
        cx = (v1.x + v2.x + v3.x) / 3.0
        cy = (v1.y + v2.y + v3.y) / 3.0
        self.local = [pr.Vector2(v.x - cx, v.y - cy) for v in (v1, v2, v3)]
        self.global_pos: list[pr.Vector3] = [v1, v2, v3]
        self.rotation = 0

    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        for global_pos in self.global_pos:
            global_pos.x += int(pr.is_key_down(rl.KEY_RIGHT) * self.speed) - int(
                pr.is_key_down(rl.KEY_LEFT) * self.speed
            )
            global_pos.y += int(pr.is_key_down(rl.KEY_DOWN) * self.speed) - int(
                pr.is_key_down(rl.KEY_UP) * self.speed
            )

    def draw(self, dt: float):
        # pr.draw_triangle_3d(self.v1, self.v2, self.v3, self.color)
        # world = [pr.Vector2(self.position.x, self.position.y ) for vect in self.local]
        # pr.draw_triangle_lines(world[0], world[1], world[2], self.color)
        # add a 3rd dimension for this method, z=0
        # world_3d = [pr.Vector3(w.x, w.y ,0) for w in world]
        # print(f"{world_3d[0].x},{world_3d[0].y},{world_3d[1].x},{world_3d[1].y}, {world_3d[2].x},{world_3d[2].y}")
        # pr.draw_triangle_3d(world_3d[0], world_3d[1], world_3d[2], self.color)
        pr.draw_triangle_3d(
            self.global_pos[0], self.global_pos[1], self.global_pos[2], self.color
        )
