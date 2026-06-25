import pyray as pr


class BaseSprite:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: float,
        rotation_speed: float,
        scale: float,
        color: pr.Color,
        debug: bool,
        debug_color,
    ) -> None:
        self.position = position
        self.direction = direction
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.scale = scale
        self.color = color
        self.debug = debug
        self.debug_color = debug_color

    def update(self, dt: float) -> None:
        pass

    def move(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pass
