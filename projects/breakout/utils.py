import math
import random
import pyray as pr
import raylib as rl
import settings as setting


def generate_random_unit_vector() -> tuple[float, float]:
    theta = random.uniform(0, 2 * math.pi)
    x = math.cos(theta)
    y = math.sin(theta)
    return [x, y]


def rect_to_bounding_box(rect: pr.Rectangle) -> pr.BoundingBox:
    min_vec = pr.Vector3(rect.x, rect.y, 0.0)
    max_vec = pr.Vector3(rect.x + rect.width, rect.y + rect.height, 0.0)
    return pr.BoundingBox(min_vec, max_vec)


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        color: list[pr.Color],
        disabled: bool,
    ) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.width: int = width
        self.height: int = height
        self.speed: int = speed
        self.color: list[pr.Color] = color
        self.disabled: bool = disabled


class Player(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        roundness: float,
        color: list[pr.Color],
        disabled: bool,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color[0],
            disabled=disabled,
        )
        self.player_roundness = roundness

    def move(self, dt: float) -> None:
        self.direction.x = int(pr.is_key_down(rl.KEY_RIGHT)) - int(
            pr.is_key_down(rl.KEY_LEFT)
        )
        if self.position.x < 0:
            self.position.x = 0
        if self.position.x + self.width > setting.window_width:
            self.position.x = setting.window_width - self.width
        dt = pr.get_frame_time()
        self.position.x += self.direction.x * self.speed * dt

    def draw(self) -> None:
        pr.draw_rectangle_rounded(
            pr.Rectangle(self.position.x, self.position.y, self.width, self.height),
            self.player_roundness,
            20,
            self.color,
        )

    def update(self, dt) -> None:
        self.move(dt=dt)


class Brick(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        roundness: float,
        color: list[pr.Color],
        disabled: bool,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color[0],
            disabled=disabled,
        )
        self.strength: int = 2  # hardcoded

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pr.draw_rectangle_v(
            pr.Vector2(self.position.x, self.position.y),
            pr.Vector2(self.width, self.height),
            self.color,
        )


class Bricks(Brick):
    def __init__(self, num_brick: int, brick_height: int, num_row: int):
        self.num_brick: int = num_brick
        self.brick_height: int = brick_height
        self.num_row: int = num_row
        self.brick_width: int = int(setting.window_width / self.num_brick) - 20
        self.bricks_list: list[Brick] = []

    def make_bricks(self):
        for i in range(10):
            for j in range(3):
                # print(i,j)
                pos_x = i * 60 + 10
                pos_y = j * 40 + 10
                brick = Brick(
                    pr.Vector2(pos_x, pos_y),
                    direction=pr.Vector2(0, 0),
                    width=50,
                    height=30,
                    speed=0,
                    roundness=0,
                    color=setting.brick_color,
                    disabled=False,
                )
                self.bricks_list.append(brick)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        _ = [brick.draw() for brick in self.bricks_list if not brick.disabled]


class Ball(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        color: list[pr.Color],
        disabled: bool,
        spawned: bool,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color[0],
            disabled=disabled,
        )
        self.spawned: bool = spawned

    def move(self, dt: float) -> None:
        if (
            self.position.x - self.width / 2 < 0
            or self.position.x + self.width / 2 > setting.window_width
        ):
            self.direction.x *= -1
        if self.position.y - self.width / 2 < 0:
            self.direction.y *= -1
        if self.position.y - self.width > setting.window_height:
            # disable the ball
            self.disabled = True
            self.spawned = False

        dt = pr.get_frame_time()
        if pr.vector2_length(self.direction) > 0:
            self.direction = pr.vector2_normalize(self.direction)
        self.direction = (
            pr.vector2_normalize(self.direction)
            if pr.vector2_length(self.direction) > 0
            else self.direction
        )
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def draw(self) -> None:
        if not self.disabled:
            pr.draw_circle_v(self.position, self.width, self.color)

    def spawn_ball(self, position: pr.Vector2) -> None:
        """spawn_ball: spawn the ball in the top-middle of the player with random direction

        :param position: the current location of the player
        :type position: pr.Vector2
        """
        self.position.x = position.x + setting.player_width / 2
        self.position.y = position.y - self.width
        self.speed = 0
        self.disabled = False

    def start(self) -> None:

        if pr.is_key_pressed(rl.KEY_SPACE):
            self.spawned = True
            self.direction = pr.Vector2(
                random.uniform(-0.25, 0.25), random.uniform(-1, 0)
            )
            self.speed = setting.ball_speed

    def update(self, dt) -> None:
        self.move(dt=dt)

    def check_collision_player(self, player: Player) -> None:
        player_bounding_box = rect_to_bounding_box(
            pr.Rectangle(
                player.position.x, player.position.y, player.width, player.height
            )
        )
        if pr.check_collision_box_sphere(
            player_bounding_box,
            pr.Vector3(self.position.x, self.position.y, 0),
            self.width,
        ):
            self.direction.y *= -1

    def check_collision_bricks(self, bricks: Bricks) -> None:
        for brick in bricks.bricks_list:
            brick_bounding_box = rect_to_bounding_box(
                pr.Rectangle(brick.position.x, brick.position.y, 100, 30)
            )
            if pr.check_collision_box_sphere(
                brick_bounding_box,
                pr.Vector3(self.position.x, self.position.y, 0),
                self.width,
            ):
                # brick.strength -= 1
                # brick.color = rl.PURPLE
                # if brick.strength == 0:
                brick.disabled = True
