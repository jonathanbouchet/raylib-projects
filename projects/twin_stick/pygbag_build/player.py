import math
import pyray as pr
import raylib as rl
from laser import Laser
from utils import wrap_borders


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
        debug_color: pr.Color,
        laser_data: dict[str, str | int],
        shoot_cooldown: float,
        shoot_timer: float,
    ) -> None:
        self.position = position
        self.speed = speed
        self.angular_speed = angular_speed
        self.scale = scale
        self.color = color
        self.debug = debug
        self.debug_color = debug_color
        self.window_borders = window_borders
        self.laser_data = laser_data
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
        # testing
        self.shoot_cooldown = shoot_cooldown
        self.shoot_timer = shoot_timer

    def load_laser_sound(self, sound: pr.Sound) -> None:
        self.laser_sound: pr.Sound = sound

    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        # 1) apply rotation from current input
        self.angle += (
            (int(pr.is_key_down(rl.KEY_RIGHT)) - int(pr.is_key_down(rl.KEY_LEFT)))
            * self.angular_speed
            * dt
        )

        # 1.5 testing
        # mouse = pr.get_mouse_position()  # pr.Vector2 (screen/world coords in raylib)
        # dx = mouse.x - self.position.x
        # dy = mouse.y - self.position.y

        # angle where your "forward" is (cos(a - pi/2), sin(a - pi/2))
        # so use atan2(dy, dx) + 90deg
        # self.angle = math.degrees(math.atan2(dy, dx)) + 90.0

        # 2) compute forward ONCE from the updated angle
        ang_rad = math.radians(self.angle)
        forward = pr.Vector2(
            math.cos(ang_rad - math.pi / 2), math.sin(ang_rad - math.pi / 2)
        )

        # 3) thrust uses the same forward
        if pr.is_key_down(rl.KEY_UP):
            self.velocity.x += forward.x * self.thrust * dt
            self.velocity.y += forward.y * self.thrust * dt

        self.velocity.x *= 1 - self.drag * dt
        self.velocity.y *= 1 - self.drag * dt

        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

        self.position = wrap_borders(
            position=self.position,
            width=self.window_borders.x,
            height=self.window_borders.y,
        )

        # 4) shooting uses the exact same forward
        self.shoot_timer = max(0.0, self.shoot_timer - dt)
        if pr.is_key_down(rl.KEY_SPACE) and self.shoot_timer == 0.0:
            self.shoot_timer = self.shoot_cooldown
            # if pr.is_key_pressed(rl.KEY_SPACE):
            a = ang_rad
            c, s = math.cos(a), math.sin(a)
            world = [
                pr.Vector2(
                    self.position.x + (lv.x * c - lv.y * s),
                    self.position.y + (lv.x * s + lv.y * c),
                )
                for lv in self.local
            ]
            tip_world = world[2]

            dir_vec = pr.Vector2(
                tip_world.x - self.position.x, tip_world.y - self.position.y
            )
            mag = math.hypot(dir_vec.x, dir_vec.y) or 1.0
            dir_vec.x /= mag
            dir_vec.y /= mag

            laser = Laser(
                position=tip_world,
                direction=dir_vec,
                # direction=forward,   # <-- guaranteed synced with this frame’s angle
                size=pr.Vector2(
                    self.laser_data.get("size")[0], self.laser_data.get("size")[1]
                ),
                speed=self.laser_data.get("speed"),
                color=tuple(self.laser_data.get("color")),
            )
            self.lasers.append(laser)
            pr.play_sound(self.laser_sound)

    # def move(self, dt: float) -> None:
    #     # 1) update angle first
    #     self.angle += (
    #         (int(pr.is_key_down(rl.KEY_RIGHT)) - int(pr.is_key_down(rl.KEY_LEFT)))
    #         * self.angular_speed * dt
    #     )

    #     # 2) now compute forward from the updated angle
    #     ang_rad = math.radians(self.angle)
    #     forward = pr.Vector2(
    #         math.cos(ang_rad - math.pi / 2),
    #         math.sin(ang_rad - math.pi / 2)
    #     )

    #     # 3) use forward for thrust
    #     if pr.is_key_down(rl.KEY_UP):
    #         self.velocity.x += forward.x * self.thrust * dt
    #         self.velocity.y += forward.y * self.thrust * dt

    #     self.velocity.x *= 1 - self.drag * dt
    #     self.velocity.y *= 1 - self.drag * dt

    #     self.position.x += self.velocity.x * dt
    #     self.position.y += self.velocity.y * dt

    #     self.position = wrap_borders(
    #         position=self.position,
    #         width=self.window_borders.x,
    #         height=self.window_borders.y,
    #     )

    #     # 4) now shoot using the same forward computed above
    #     if pr.is_key_pressed(rl.KEY_SPACE):
    #         # tip_world computed from world verts
    #         a = ang_rad
    #         c, s = math.cos(a), math.sin(a)
    #         world = [
    #             pr.Vector2(
    #                 self.position.x + (lv.x * c - lv.y * s),
    #                 self.position.y + (lv.x * s + lv.y * c),
    #             )
    #             for lv in self.local
    #         ]
    #         tip_world = world[2]

    #         laser = Laser(
    #             position=tip_world,
    #             direction=forward,   # <-- use forward from updated angle
    #             size=pr.Vector2(
    #                 self.laser_data.get("size")[0],
    #                 self.laser_data.get("size")[1]
    #             ),
    #             speed=self.laser_data.get("speed"),
    #             color=tuple(self.laser_data.get("color"))
    #         )
    #         self.lasers.append(laser)

    # def move(self, dt: float) -> None:
    #     # simple rotation control: left/right change angle
    #     self.angle += (
    #         (int(pr.is_key_down(rl.KEY_RIGHT)) - int(pr.is_key_down(rl.KEY_LEFT)))
    #         * self.angular_speed
    #         * dt
    #     )
    #     ang_rad = math.radians(self.angle)
    #     forward = pr.Vector2(
    #         math.cos(ang_rad - math.pi / 2), math.sin(ang_rad - math.pi / 2)
    #     )
    #     if pr.is_key_down(rl.KEY_UP):
    #         self.velocity.x += forward.x * self.thrust * dt
    #         self.velocity.y += forward.y * self.thrust * dt

    #     # clamping velocity
    #     # self.velocity.x *= max(0, 1 - self.drag * dt)
    #     # self.velocity.y *= max(0, 1 - self.drag * dt)
    #     self.velocity.x *= 1 - self.drag * dt
    #     self.velocity.y *= 1 - self.drag * dt

    #     # integrate
    #     self.position.x += self.velocity.x * dt
    #     self.position.y += self.velocity.y * dt

    #     # check borders to re-appear on the other side of the screen
    #     self.position = wrap_borders(
    #         position=self.position,
    #         width=self.window_borders.x,
    #         height=self.window_borders.y,
    #     )

    #     # check if laser is shot
    #     if pr.is_key_pressed(rl.KEY_SPACE):
    #         ang_rad = math.radians(self.angle)
    #         # forward = pr.Vector2(math.cos(ang_rad - math.pi/2), math.sin(ang_rad - math.pi/2))
    #         c, s = math.cos(ang_rad), math.sin(ang_rad)

    #         world = [
    #             pr.Vector2(
    #                 self.position.x + (lv.x * c - lv.y * s),
    #                 self.position.y + (lv.x * s + lv.y * c),
    #             )
    #             for lv in self.local
    #         ]

    #         tip_world = world[2]  # top vertex (same order as local)
    #         laser = Laser(
    #             position=tip_world,
    #             direction=forward,
    #             size=pr.Vector2(
    #                 self.laser_data.get("size")[0],
    #                 self.laser_data.get("size")[1]
    #             ),
    #             speed=self.laser_data.get("speed"),
    #             color=tuple(self.laser_data.get("color"))
    #         )
    #         self.lasers.append(laser)

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

        # draw a line in the forward direction to help the user
        ang_rad = math.radians(self.angle)
        forward = pr.Vector2(
            math.cos(ang_rad - math.pi / 2), math.sin(ang_rad - math.pi / 2)
        )
        # print(f"{forward.x=}, {forward.y=}")
        start = world[2]
        end = pr.Vector2(start.x + forward.x * 1000, start.y + forward.y * 1000)
        pr.draw_line_ex(start, end, 1, pr.SKYBLUE)

    def get_lasers(self) -> list[Laser]:
        """return a list of all lasers instantiated"""
        return self.lasers
