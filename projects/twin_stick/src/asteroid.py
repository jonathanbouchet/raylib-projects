import math
import pyray as pr
from .sprite import BaseSprite


class Asteroid(BaseSprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        size: pr.Vector2,
        speed: float,
        angular_speed: float,
        scale: float,
        color: pr.Color,
        debug: bool,
        debug_color,
    ) -> None:
        super().__init__(
            position=position,
            speed=speed,
            angular_speed=angular_speed,
            scale=scale,
            color=color,
            debug=debug,
            debug_color=debug_color,
        )
        self.direction=direction
        self.size = size
        self.rotation = 0

    def get_rectangle(self) -> pr.Rectangle:
        return pr.Rectangle(self.position.x, self.position.y, self.size.x, self.size.y)

    def get_origin(self) -> pr.Vector2:
        return pr.Vector2(self.size.x // 2, self.size.y // 2)

    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        self.rotation += self.angular_speed * dt
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def rotated_point(
        self, p: pr.Vector2, origin: pr.Vector2, angle_deg: float
    ) -> pr.Vector2:
        ang = math.radians(angle_deg)
        s, c = math.sin(ang), math.cos(ang)
        x, y = p.x - origin.x, p.y - origin.y
        return pr.Vector2(origin.x + x * c - y * s, origin.y + x * s + y * c)

    def draw(self, dt: float) -> None:
        origin = self.get_origin()
        rect = self.get_rectangle()
        pr.draw_rectangle_pro(rect, origin, self.rotation, self.color)
        # debug: rotated outline
        if self.debug:
            center_world = pr.Vector2(rect.x + origin.x, rect.y + origin.y)

            x0, y0 = rect.x, rect.y
            x1, y1 = rect.x + rect.width, rect.y + rect.height

            tl = self.rotated_point(pr.Vector2(x0, y0), center_world, self.rotation)
            tr = self.rotated_point(pr.Vector2(x1, y0), center_world, self.rotation)
            br = self.rotated_point(pr.Vector2(x1, y1), center_world, self.rotation)
            bl = self.rotated_point(pr.Vector2(x0, y1), center_world, self.rotation)
            tl.x -= int(self.size.x / 2)
            tl.y -= int(self.size.y / 2)
            tr.x -= int(self.size.x / 2)
            tr.y -= int(self.size.y / 2)
            br.x -= int(self.size.x / 2)
            br.y -= int(self.size.y / 2)
            bl.x -= int(self.size.x / 2)
            bl.y -= int(self.size.y / 2)

            pr.draw_line_ex(
                pr.Vector2(int(tl.x), int(tl.y)),
                pr.Vector2(int(tr.x), int(tr.y)),
                2.0,
                self.debug_color,
            )
            pr.draw_line_ex(
                pr.Vector2(int(tr.x), int(tr.y)),
                pr.Vector2(int(br.x), int(br.y)),
                2.0,
                self.debug_color,
            )
            pr.draw_line_ex(
                pr.Vector2(int(br.x), int(br.y)),
                pr.Vector2(int(bl.x), int(bl.y)),
                2.0,
                self.debug_color,
            )
            pr.draw_line_ex(
                pr.Vector2(int(bl.x), int(bl.y)),
                pr.Vector2(int(tl.x), int(tl.y)),
                2.0,
                self.debug_color,
            )
