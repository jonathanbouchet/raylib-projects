import math
import pyray as pr
import raylib as rl
from .sprite import BaseSprite
from .laser import Laser


class Player(BaseSprite):
    def __init__(
        self,
        position: pr.Vector2,
        window_size: pr.Vector2,
        v1: pr.Vector3,
        v2: pr.Vector3,
        v3: pr.Vector3,
        speed: float,
        angular_speed: float,
        scale: float,
        color: pr.Color,
        debug: bool,
        debug_color,
    ) -> None:
        super().__init__(
            position=position,
            speed=speed,
            angular_speed=angular_speed,
            scale=scale,
            color=color,
            debug=debug,
            debug_color=debug_color,
        )
        self.window_size = window_size
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        # compute centroid and store local verts (never modify)
        cx = (v1.x + v2.x + v3.x) / 3.0
        cy = (v1.y + v2.y + v3.y) / 3.0
        self.local = [pr.Vector2(v.x - cx, v.y - cy) for v in (v1, v2, v3)]
        self.global_pos: list[pr.Vector3] = [v1, v2, v3]
        self.rotation = 0
        self.angle = 0.0  # degrees
        self.velocity = pr.Vector2(0, 0)
        self.thrust = 400
        self.drag = 0.5  # damping
        self.lasers: list[Laser] = []

    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        # simple rotation control: left/right change angle
        self.angle += (
            (int(pr.is_key_down(rl.KEY_RIGHT)) - int(pr.is_key_down(rl.KEY_LEFT)))
            * self.angular_speed
            * dt
        )
        ang_rad = math.radians(self.angle)
        forward = pr.Vector2(
            math.cos(ang_rad - math.pi / 2), math.sin(ang_rad - math.pi / 2)
        )
        if pr.is_key_down(rl.KEY_UP):
            self.velocity.x += forward.x * self.thrust * dt
            self.velocity.y += forward.y * self.thrust * dt

        # clamping velocity
        # self.velocity.x *= max(0, 1 - self.drag * dt)
        # self.velocity.y *= max(0, 1 - self.drag * dt)
        self.velocity.x *= 1 - self.drag * dt
        self.velocity.y *= 1 - self.drag * dt

        # integrate
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

        # check borders to re-appear on the other side of the screen
        if self.position.x > self.window_size.x:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = self.window_size.x
        if self.position.y > self.window_size.y:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = self.window_size.y

        # check if laser is shoot
        if pr.is_key_pressed(rl.KEY_SPACE):
            ang_rad = math.radians(self.angle)
            # forward = pr.Vector2(math.cos(ang_rad - math.pi/2), math.sin(ang_rad - math.pi/2))
            c, s = math.cos(ang_rad), math.sin(ang_rad)

            world = [
                pr.Vector2(
                    self.position.x + (lv.x * c - lv.y * s),
                    self.position.y + (lv.x * s + lv.y * c),
                )
                for lv in self.local
            ]

            tip_world = world[2]  # top vertex (same order as local)
            laser = Laser(position=tip_world, direction=forward, speed=50)
            self.lasers.append(laser)

        # for global_pos in self.global_pos:
        #     global_pos.x += int(pr.is_key_down(rl.KEY_RIGHT) * self.speed) - int(
        #         pr.is_key_down(rl.KEY_LEFT) * self.speed
        #     )
        #     global_pos.y += int(pr.is_key_down(rl.KEY_DOWN) * self.speed) - int(
        #         pr.is_key_down(rl.KEY_UP) * self.speed
        #     )

    def draw(self, dt: float):
        a = math.radians(self.angle)
        c, s = math.cos(a), math.sin(a)
        # rotate local -> world and draw
        world = [
            pr.Vector2(
                self.position.x + (lv.x * c - lv.y * s),
                self.position.y + (lv.x * s + lv.y * c),
            )
            for lv in self.local
        ]
        world_3d = [pr.Vector3(w.x, w.y, 0) for w in world]
        pr.draw_triangle_lines(world[0], world[1], world[2] , self.color)
        # pr.draw_triangle_3d(world_3d[0], world_3d[1], world_3d[2], self.color)
        # pr.draw_triangle_3d(self.v1, self.v2, self.v3, self.color)
        # world = [pr.Vector2(self.position.x, self.position.y ) for vect in self.local]
        # pr.draw_triangle_lines(world[0], world[1], world[2], self.color)
        # add a 3rd dimension for this method, z=0
        # world_3d = [pr.Vector3(w.x, w.y ,0) for w in world]
        # print(f"{world_3d[0].x},{world_3d[0].y},{world_3d[1].x},{world_3d[1].y}, {world_3d[2].x},{world_3d[2].y}")
        # pr.draw_triangle_3d(world_3d[0], world_3d[1], world_3d[2], self.color)

        # pr.draw_triangle_3d(
        #     self.global_pos[0], self.global_pos[1], self.global_pos[2], self.color
        # )
