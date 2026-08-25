import pymunk
import pyray as pr

"""
this class defines a pymunk STATIC body based on a raylib definition:
- position as pr.Vector2
- size: width x height as pr.Vector2

Because of the inconsistency of coordinates definition between the 2 frameworks:
- pymunk defines object based on their center of gravity and size
- raylib defines object based on top-left position and size

- example:
floor = Static(
    position=pr.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 
    body_size=pr.Vector2(200, FLOOR_THICKNESS), 
    elasticity=0.9, 
    friction=1.0
)
"""


class Static:
    def __init__(
        self,
        position: pr.Vector2,
        body_size: pr.Vector2,
        elasticity: float,
        friction: float,
        color: pr.Color,
    ) -> None:
        self.static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.static_body.position = (position.x, position.y)
        self.static_body_size = (body_size.x, body_size.y)
        self.shape = pymunk.Poly.create_box(self.static_body, self.static_body_size)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.color = color
        self.debug = False

    def draw(self) -> None:
        pr.draw_rectangle_v(
            pr.Vector2(
                self.static_body.position.x - self.static_body_size[0] / 2,
                self.static_body.position.y - self.static_body_size[1] / 2,
            ),
            self.static_body_size,
            self.color,
        )
        if self.debug:
            pr.draw_line(
                int(self.static_body.position.x - self.static_body_size[0] / 2),
                int(self.static_body.position.y),
                int(self.static_body.position.x + self.static_body_size[0] / 2),
                int(self.static_body.position.y),
                pr.GREEN,
            )


class Dynamic:
    def __init__(
        self,
        position: pr.Vector2,
        radius: int,
        velocity: pr.Vector2,
        elasticity: float,
        friction: float,
        color: pr.Color,
    ) -> None:
        self.body = pymunk.Body(1.0, 100)
        self.body.position = (position.x, position.y)
        self.body.velocity = (velocity.x, velocity.y)
        self.radius = radius
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.color = color

    def draw(self) -> None:
        pr.draw_circle_v(
            pr.Vector2(self.body.position.x, self.body.position.y),
            self.radius,
            self.color,
        )

class DynamicMouse:
    def __init__(
    self,
    position: pr.Vector2,
    body_size: pr.Vector2,
    elasticity: float,
    friction: float,
    color: pr.Color,
) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = (position.x, position.y)
        self.body_size = (body_size.x, body_size.y)
        self.shape = pymunk.Poly.create_box(self.body, self.body_size)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.color = color
        self.debug = False

    def update(self):
        pos = pr.get_mouse_position()
        self.body.position = (pos.x, pos.y)

    def draw(self) -> None:
        pr.draw_rectangle_v(
            pr.Vector2(
                self.body.position.x - self.body_size[0] / 2,
                self.body.position.y - self.body_size[1] / 2,
            ),
            self.body_size,
            self.color,
        )
        if self.debug:
            pr.draw_line(
                int(self.body.position.x - self.body_size[0] / 2),
                int(self.body.position.y),
                int(self.body.position.x + self.body_size[0] / 2),
                int(self.body.position.y),
                pr.GREEN,
            )