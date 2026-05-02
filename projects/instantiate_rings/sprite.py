import pyray as pr
import settings as setting


class Sprite:
    def __init__(
        self,
        pos: pr.Vector2,
        direction: pr.Vector2,
        speed: float,
        inner_radius: int,
        outer_radius: int,
        color: pr.Color,
    ) -> None:
        self.pos = pos
        self.direction = direction
        self.speed = speed
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.color = color

    def move(self, dt: float) -> None:
        """
        - check for collisions with the top, bottom, left and right border of the screen in order to make the ring bouncing back
        """

        if (
            self.pos.x >= (setting.WINDOW_WIDTH - self.outer_radius)
            or self.pos.x <= self.outer_radius
        ):
            self.direction.x *= -1
        if (
            self.pos.y >= (setting.WINDOW_HEIGHT - self.outer_radius)
            or self.pos.y <= self.outer_radius
        ):
            self.direction.y *= -1

        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt

    def update(self, dt):
        self.move(dt)

    def draw(self):
        pr.draw_ring(
            self.pos, self.inner_radius, self.outer_radius, 0, 360, 50, self.color
        )
        pr.draw_line_ex(
            self.pos,
            pr.Vector2(
                self.pos.x + self.direction.x * 100, self.pos.y + self.direction.y * 100
            ),
            10,
            pr.RED,
        )

    def __str__(self) -> str:
        return f"speed: {self.speed}, inner radius:{self.inner_radius}, outer radius: {self.outer_radius}, color: {self.color}"
