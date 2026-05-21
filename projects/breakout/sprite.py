import pyray as pr


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        color: list[pr.Color],
        disabled: bool,
    ) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.width: int = width
        self.height: int = height
        self.speed: int = speed
        self.color: list[pr.Color] = color
        self.disabled: bool = disabled
