import pyray as pr
from sprite import Sprite


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
            color=color,
            disabled=disabled,
        )
        self.current_color: pr.Color = color[0]
        self.strength: int = 2  # hardcoded

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pr.draw_rectangle_v(
            pr.Vector2(self.position.x, self.position.y),
            pr.Vector2(self.width, self.height),
            self.current_color,
        )
