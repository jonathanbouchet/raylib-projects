import math
import pyray as pr


class Laser:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        size: pr.Vector2,
        speed: float,
    ):
        self.position = position
        self.direction = direction
        self.size = size
        self.speed = speed
        self.discard = False

    def update(self, dt) -> None:
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def draw(self) -> None:
        # print(f"{self.direction.x}, {self.direction.y}")
        laser_rect = pr.Rectangle(
            self.position.x, self.position.y, self.size.x, self.size.y
        )
        pr.draw_rectangle_pro(
            laser_rect,
            pr.Vector2(self.size.x // 2, self.size.y // 2),
            math.degrees(math.atan(self.direction.y / self.direction.x)),
            pr.WHITE,
        )
