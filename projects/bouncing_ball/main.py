import pyray as pr

width, height = 800, 600
gravity = pr.Vector2(0, 1000)  # gravity only on y


class Wall:
    def __init__(
        self,
        position: pr.Vector2,
        origin: pr.Vector2,
        rotation: float,
        size: pr.Vector2,
        color: pr.Color,
        id: int,
    ):
        self.id: int = id
        self.position: pr.Vector2 = position
        self.origin: pr.Vector2 = origin
        self.rotation: float = rotation
        self.size: pr.Vector2 = size
        self.color: pr.Color = color
        self.rectangle: pr.Rectangle = pr.Rectangle(
            self.position.x, self.position.y, self.size.x, self.size.y
        )

    def draw(self):
        tmp_rect = pr.Rectangle(
            self.position.x, self.position.y, self.size.x, self.size.y
        )
        pr.draw_rectangle_pro(tmp_rect, self.origin, self.rotation, self.color)


class Player:
    def __init__(
        self,
        position: pr.Vector2,
        velocity: pr.Vector2,
        radius: int,
        restitution: float = 0.8,
    ):
        self.position: pr.Vector2 = position
        self.velocity: pr.Vector2 = velocity
        self.radius: int = radius
        self.restitution: float = restitution
        self.initial_position: pr.Vector2 = position

    def set_velocity(self, velocity: pr.Vector2) -> None:
        self.velocity = velocity

    def reset(self) -> None:
        print(f"{self.initial_position.x=}, {self.initial_position.y=}")
        self.position = self.initial_position
        self.set_velocity(velocity=pr.Vector2(0, 0))
        # self.velocity = pr.Vector2(0,0)

    def update(self, dt: float, walls: list[Wall]) -> None:
        self.apply_gravity(dt)
        self.move(dt)
        for wall in walls:
            if self.check_collision(wall):
                self.resolve_collision(wall)

    def apply_gravity(self, dt: float) -> None:
        self.velocity.y += gravity.y * dt

    def move(self, dt: float) -> None:
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

    def check_collision(self, other: Wall) -> bool:
        return pr.check_collision_circle_rec(
            self.position, self.radius, other.rectangle
        )

    def resolve_collision(self, other: Wall) -> None:
        # Find closest point on rect to circle center
        rx, ry = other.rectangle.x, other.rectangle.y
        rw, rh = other.rectangle.width, other.rectangle.height

        # Clamp circle center to rect bounds to get closest point
        closest_x = max(rx, min(self.position.x, rx + rw))
        closest_y = max(ry, min(self.position.y, ry + rh))

        # Vector from closest point to circle center
        dx = self.position.x - closest_x
        dy = self.position.y - closest_y
        dist_sq = dx * dx + dy * dy

        if dist_sq == 0:
            # circle center exactly at closest point (corner/inside) — nudge upward
            # choose a fallback normal (up)
            nx, ny = 0.0, -1.0
            penetration = self.radius
        else:
            dist = dist_sq**0.5
            nx, ny = dx / dist, dy / dist  # contact normal (points from rect -> circle)
            penetration = self.radius - dist

        if penetration > 0:
            # push circle out along normal
            self.position.x += nx * penetration
            self.position.y += ny * penetration

            # decompose velocity into normal and tangential components
            v_dot_n = self.velocity.x * nx + self.velocity.y * ny
            v_nx = v_dot_n * nx
            v_ny = v_dot_n * ny
            v_tx = self.velocity.x - v_nx
            v_ty = self.velocity.y - v_ny

            # reflect/scale normal component by restitution, keep tangential (optionally apply friction)
            self.velocity.x = v_tx - v_nx * self.restitution
            self.velocity.y = v_ty - v_ny * self.restitution

            # small threshold to avoid jitter
            if abs(self.velocity.x) < 1:
                self.velocity.x = 0
            if abs(self.velocity.y) < 1:
                self.velocity.y = 0

    def draw(self):
        pr.draw_circle_v(self.position, self.radius, pr.YELLOW)


# Initialization
pr.init_window(width, height, "bouncing ball")
pr.set_target_fps(60)

player = Player(
    position=pr.Vector2(width / 3, 200),
    velocity=None,
    radius=20,
    restitution=0.8,
)
ground = Wall(
    id=0,
    position=pr.Vector2(0, height - 50),
    origin=pr.Vector2(0, 0),
    rotation=0,
    size=pr.Vector2(width, 50),
    color=pr.BLACK,
)

right = Wall(
    id=1,
    position=pr.Vector2(width - 50, 0),
    origin=pr.Vector2(0, 0),
    rotation=0,
    size=pr.Vector2(50, height),
    color=pr.DARKGREEN,
)

obstacle_down = Wall(
    id=3,
    position=pr.Vector2(width - 300, 300),
    origin=pr.Vector2(0, 0),
    rotation=0,
    size=pr.Vector2(50, height - 50 - 300),
    color=pr.DARKPURPLE,
)

diag = Wall(
    id=4,
    position=pr.Vector2(width - 300, 0),
    origin=pr.Vector2(0, 0),
    rotation=-45,
    size=pr.Vector2(50, 200),
    color=pr.DARKBLUE,
)

walls = [ground, right, obstacle_down]
is_fired: bool = False
is_input: bool = False
is_reset: bool = False

velocity_x = pr.ffi.new("float *", 500)  # Initial value
velocity_y = pr.ffi.new("float *", 0)  # Initial value

# Main loop
while not pr.window_should_close():
    dt = pr.get_frame_time()

    sliderOption_x = pr.gui_slider(
        pr.Rectangle(20, 20, 100, 20), "0", "1000", velocity_x, 0, 1000
    )
    sliderOption_y = pr.gui_slider(
        pr.Rectangle(20, 40, 100, 20), "0", "1000", velocity_y, -500, 500
    )

    if pr.gui_button(pr.Rectangle(20, 60, 100, 20), "Fire"):
        is_fired = True
        print(f"{velocity_x[0]=}, {velocity_y[0]=}")
        player.set_velocity(velocity=pr.Vector2(int(velocity_x[0]), int(velocity_y[0])))

    if pr.gui_button(pr.Rectangle(20, 80, 100, 20), "reset"):
        del player
        is_reset = True
        is_input = False
        is_fired = False

    if is_reset:
        player = Player(
            position=pr.Vector2(width / 3, 200),
            velocity=None,
            radius=20,
            restitution=0.8,
        )
        player.set_velocity(velocity=pr.Vector2(500, 0))
        is_reset = False

    # logic
    if is_fired:
        player.update(dt=dt, walls=walls)

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.DARKGRAY)
    player.draw()
    _ = [w.draw() for w in walls]
    pr.draw_fps(20, 0)
    pr.end_drawing()

pr.close_window()
