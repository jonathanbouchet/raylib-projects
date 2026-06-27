import math
import pyray as pr
import raylib as rl
from .laser import Laser
from .utils import wrap_borders


class Player:
    def __init__(
        self,
        position: pr.Vector2,
        window_borders: pr.Vector2,
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
        self.position = position
        self.speed = speed
        self.angular_speed = angular_speed
        self.scale = scale
        self.color = color
        self.debug = debug
        self.debug_color = debug_color
        self.window_borders = window_borders
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
        self.position = wrap_borders(
            position=self.position,
            width=self.window_borders.x,
            height=self.window_borders.y,
        )

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
            laser = Laser(
                position=tip_world,
                direction=forward,
                size=pr.Vector2(30, 5.0),
                speed=200,
            )
            self.lasers.append(laser)

    def draw(self, dt: float) -> None:
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
        # world_3d = [pr.Vector3(w.x, w.y, 0) for w in world]
        pr.draw_triangle_lines(world[0], world[1], world[2], self.color)

    def get_lasers(self) -> list[Laser]:
        """return a list of all lasers instantiated"""
        return self.lasers
