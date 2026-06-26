import math
import pyray as pr
from .sprite import BaseSprite
from .utils import draw_rotated_rect_lines


class Asteroid:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        size: pr.Vector2,
        color: pr.Color,
    ):
        self.position = position
        self.direction = direction
        self.size = size
        self.color = color
        self.lineThick = 2
        self.angle = 0.0

        self.speed = 10.0  # pixels/sec
        self._rotating = False  # set with SPACE

    def update(self, dt: float) -> None:
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt
        self.angle += 180.0 * dt  # degrees/sec

    def draw(self, dt: float):
        center = pr.Vector2(
            self.position.x + self.size.x / 2, self.position.y + self.size.y / 2
        )
        draw_rotated_rect_lines(
            center, self.size, self.angle, self.lineThick, self.color
        )
