import pyray as pr
import raylib as rl
from sprite import Sprite
import settings as setting


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
