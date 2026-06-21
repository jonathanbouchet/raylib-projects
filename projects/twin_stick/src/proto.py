import math
import random
import pyray as pr
import raylib as rl

width, height = 600, 600


class Enemy:
    def __init__(
        self,
        position: pr.Vector2,
        size: pr.Vector2,
        direction: pr.Vector2,
        speed: float,
        color: pr.Color,
    ) -> None:
        self.position = position
        self.size = size
        self.direction = direction
        self.speed = speed
        self.color = color

    def update(self, dt):
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        if self.position.x > width:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = width
        if self.position.y > height:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = height

    def draw(self) -> None:
        pr.draw_rectangle_v(self.position, self.size, self.color)


class Laser:
    def __init__(self, position: pr.Vector2, direction: pr.Vector2, speed: float):
        self.position = position
        self.direction = direction
        self.speed = speed

    def update(self, dt):
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def draw(self) -> None:
        L = 30
        end = pr.Vector2(
            self.position.x + self.direction.x * L,
            self.position.y + self.direction.y * L,
        )
        pr.draw_line_v(self.position, end, pr.WHITE)


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        v1: pr.Vector2,
        v2: pr.Vector2,
        v3: pr.Vector2,
        color: pr.Color,
        scale_factor: float = 1.0,
    ) -> None:
        self.position = position
        # compute centroid and store local verts (never modify)
        cx = (v1.x + v2.x + v3.x) / 3.0
        cy = (v1.y + v2.y + v3.y) / 3.0
        self.local = [pr.Vector2(v.x - cx, v.y - cy) for v in (v1, v2, v3)]
        self.angle = 0.0  # degrees
        self.color = color
        self.velocity = pr.Vector2(0, 0)
        self.thrust = 400
        self.drag = 0.5  # damping
        self.angular_speed = 150
        self.scale_factor = scale_factor
        self.lasers: list[Laser] = []

    def update(self, dt):
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
        # forward = pr.Vector2(math.cos(self.angle), math.sin(self.angle))
        # forward = pr.Vector2(math.cos(self.angle - math.pi/2), math.sin(self.angle - math.pi/2))
        # if pr.is_key_down(rl.KEY_SPACE):
        if pr.is_mouse_button_down(0):
            self.velocity.x += forward.x * self.thrust * dt
            self.velocity.y += forward.y * self.thrust * dt
        # gravity + drag
        # self.vel.x += self.gravity.x * dt
        # self.vel.y += self.gravity.y * dt

        # clamping velocity
        # self.velocity.x *= max(0, 1 - self.drag * dt)
        # self.velocity.y *= max(0, 1 - self.drag * dt)
        self.velocity.x *= 1 - self.drag * dt
        self.velocity.y *= 1 - self.drag * dt

        # integrate
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

        # check borders to re-appear on the other side of the screen
        if self.position.x > width:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = width
        if self.position.y > height:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = height

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
            laser = Laser(position=tip_world, direction=forward, speed=100)
            # laser = Laser(position=pr.Vector2(tip_world.x, tip_world.y), direction=forward, speed=300)
            self.lasers.append(laser)

    def draw(self):
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
        # pr.draw_triangle_lines(world[0], world[1], world[2], self.color)
        # add a 3rd dimension for this method, z=0
        world_3d = [pr.Vector3(w.x, w.y, 0) for w in world]
        pr.draw_triangle_3d(world_3d[0], world_3d[1], world_3d[2], self.color)


pr.init_window(width, height, "app")
pr.set_target_fps(60)

arrow = Sprite(
    position=pr.Vector2(width / 2, height / 2),
    v1=pr.Vector2(width / 2 - 10, height / 2),  # bottom left
    v2=pr.Vector2(width / 2 + 10, height / 2),  # bottom right
    v3=pr.Vector2(width / 2, height / 2 - 25),  # top center
    color=pr.WHITE,
    scale_factor=1.0,
)
# enemies
enemies = [
    Enemy(
        position=pr.Vector2(random.randint(0, width), random.randint(0, height)),
        size=pr.Vector2(10, 10),
        direction=pr.Vector2(random.randint(-100, 100), random.randint(-100, 100)),
        speed=3,
        color=random.choice([pr.YELLOW, pr.GREEN, pr.BLUE, pr.PINK]),
    )
    for i in range(2)
]

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    arrow.update(dt=dt)
    _ = [x.update(dt=dt) for x in enemies]
    if len(arrow.lasers) > 0:
        _ = [l.update(dt=dt) for l in arrow.lasers]

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    arrow.draw()
    _ = [x.draw() for x in enemies]

    if len(arrow.lasers) > 0:
        _ = [l.draw() for l in arrow.lasers]
    pr.draw_fps(0, 0)
    pr.end_drawing()
pr.close_window()
