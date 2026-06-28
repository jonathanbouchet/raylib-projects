import pyray as pr
from .utils import rotate_point, wrap_borders


class Asteroid:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        window_borders: pr.Vector2,
        size: pr.Vector2,
        color: pr.Color,
    ) -> None:
        self.position = position
        self.direction = direction
        self.window_borders = window_borders
        self.size = size
        self.color = color
        self.lineThick = 2
        self.angle = 0.0
        self.speed = 0.0  # pixels/sec
        self._rotating = False  # set with SPACE
        self.discard: bool = False

    def update(self, dt: float) -> None:
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt
        self.angle += 90.0 * dt  # degrees/sec

        self.position = wrap_borders(
            position=self.position,
            width=self.window_borders.x,
            height=self.window_borders.y,
        )

    def get_rectangle(self) -> list[pr.Vector2]:
        center = pr.Vector2(
            self.position.x + self.size.x / 2, self.position.y + self.size.y / 2
        )
        half = pr.Vector2(self.size.x / 2, self.size.y / 2)
        tl = pr.Vector2(center.x - half.x, center.y - half.y)
        tr = pr.Vector2(center.x + half.x, center.y - half.y)
        br = pr.Vector2(center.x + half.x, center.y + half.y)
        bl = pr.Vector2(center.x - half.x, center.y + half.y)

        tl = rotate_point(tl, center, self.angle)
        tr = rotate_point(tr, center, self.angle)
        br = rotate_point(br, center, self.angle)
        bl = rotate_point(bl, center, self.angle)

        return [tl, tr, br, bl]

    def draw(self, dt: float) -> None:
        center = pr.Vector2(
            self.position.x + self.size.x / 2, self.position.y + self.size.y / 2
        )
        half = pr.Vector2(self.size.x / 2, self.size.y / 2)
        tl = pr.Vector2(center.x - half.x, center.y - half.y)
        tr = pr.Vector2(center.x + half.x, center.y - half.y)
        br = pr.Vector2(center.x + half.x, center.y + half.y)
        bl = pr.Vector2(center.x - half.x, center.y + half.y)

        tl = rotate_point(tl, center, self.angle)
        tr = rotate_point(tr, center, self.angle)
        br = rotate_point(br, center, self.angle)
        bl = rotate_point(bl, center, self.angle)

        pr.draw_line_ex(tl, tr, self.lineThick, self.color)
        pr.draw_line_ex(tr, br, self.lineThick, self.color)
        pr.draw_line_ex(br, bl, self.lineThick, self.color)
        pr.draw_line_ex(bl, tl, self.lineThick, self.color)
