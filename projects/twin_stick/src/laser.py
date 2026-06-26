import pyray as pr


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
        pr.draw_line_ex(self.position, end, 2, pr.WHITE)
