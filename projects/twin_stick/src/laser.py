import math
import pyray as pr
from .utils import rotate_point


class Laser:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        size: pr.Vector2,
        speed: float,
        color: pr.Color
    ):
        self.position = position
        self.direction = direction
        self.size = size
        self.speed = speed
        self.discard = False
        self.color = color

    def update(self, dt) -> None:
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def get_rectangle(self) -> list[pr.Vector2]:
        center = pr.Vector2(
            self.position.x + self.size.x / 2, self.position.y + self.size.y / 2
        )
        half = pr.Vector2(self.size.x / 2, self.size.y / 2)
        tl = pr.Vector2(center.x - half.x, center.y - half.y)
        tr = pr.Vector2(center.x + half.x, center.y - half.y)
        br = pr.Vector2(center.x + half.x, center.y + half.y)
        bl = pr.Vector2(center.x - half.x, center.y + half.y)

        angle = math.degrees(math.atan2(self.direction.y, self.direction.x))

        tl = rotate_point(tl, center, angle)
        tr = rotate_point(tr, center, angle)
        br = rotate_point(br, center, angle)
        bl = rotate_point(bl, center, angle)

        return [tl, tr, br, bl]

    def draw(self) -> None:
        # print(f"{self.direction.x}, {self.direction.y}")
        laser_rect = pr.Rectangle(
            self.position.x, self.position.y, self.size.x, self.size.y
        )
        pr.draw_rectangle_pro(
            laser_rect,
            pr.Vector2(self.size.x // 2, self.size.y // 2),
            math.degrees(math.atan2(self.direction.y, self.direction.x)),
            self.color,
        )
