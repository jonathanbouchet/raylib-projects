import pyray as pr
import raylib as rl


def multiply_vector2(v, scalar):
    return pr.Vector2(v.x * scalar, v.y * scalar)


class Player:
    def __init__(self, position: pr.Vector2, direction: pr.Vector2, speed: int) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.speed: int = speed

    def move(self, dt: float) -> None:
        self.direction.x = int(pr.is_key_down(rl.KEY_RIGHT)) - int(
            pr.is_key_down(rl.KEY_LEFT)
        )
        self.direction.y = int(pr.is_key_down(rl.KEY_DOWN)) - int(
            pr.is_key_down(rl.KEY_UP)
        )
        self.position = pr.vector2_add(
            self.position,
            pr.vector2_scale(pr.vector2_scale(self.direction, self.speed), dt),
        )
        # self.position.x += self.direction.x * self.speed * dt
        # self.position.y += self.direction.y * self.speed * dt

    def animate(self, dt: float):
        pass

    def update(self, dt: float) -> None:
        self.move(dt=dt)
        self.animate(dt=dt)

    def draw(self) -> None:
        pr.draw_rectangle_v(self.position, pr.Vector2(20, 40), pr.YELLOW)
