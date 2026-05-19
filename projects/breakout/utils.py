import pyray as pr
import raylib as rl
import settings as setting


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        color: pr.Color,
    ) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.width: int = width
        self.height: int = height
        self.speed: int = speed
        self.color: pr.Color = color


class Player(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        roundness: float,
        color: pr.Color,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color,
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
        color: pr.Color,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color,
        )

    def update(self) -> None:
        pass


class Bricks(Brick):
    def __init__(self, num_brick: int, brick_height: int, num_row: int):
        self.num_brick: int = num_brick
        self.brick_height: int = brick_height
        self.num_row: int = num_row
        self.brick_width: int = int(setting.window_width / self.num_brick)

    def make_bricks(self):
        for i in range(self.num_row):
            for j in range(self.num_brick):
                pass
                # pr.draw_rectangle_rounded(
                #     pr.Rectangle(self.position.x, self.position.y, self.width, self.height),
                #     self.player_roundness,
                #     20,
                #     self.color,
                # )


class Ball(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        color: pr.Color,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color,
        )

    def move(self, dt: float) -> None:
        if (
            self.position.x - self.width / 2 < 0
            or self.position.x + self.width / 2 > setting.window_width
        ):
            self.direction.x *= -1
        if (
            self.position.y - self.width / 2 < 0
            or self.position.y + self.width / 2 > setting.window_height
        ):
            self.direction.y *= -1

        dt = pr.get_frame_time()
        self.direction = pr.vector2_normalize(self.direction)
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def draw(self) -> None:
        pr.draw_circle_v(self.position, self.width, self.color)

    def update(self, dt) -> None:
        self.move(dt=dt)
