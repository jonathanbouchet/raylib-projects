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
    ):
        self.static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.static_body.position = (position.x, position.y)
        self.static_body_size = (body_size.x, body_size.y)
        self.shape = pymunk.Poly.create_box(self.static_body, self.static_body_size)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.debug: bool = False

    def draw(self) -> None:
        pr.draw_rectangle_v(
            pr.Vector2(
                self.static_body.position.x - self.static_body_size[0] / 2,
                self.static_body.position.y - self.static_body_size[1] / 2,
            ),
            self.static_body_size,
            pr.DARKGRAY,
        )
        if self.debug:
            pr.draw_line(
                int(self.static_body.position.x - self.static_body_size[0] / 2),
                int(self.static_body.position.y),
                int(self.static_body.position.x + self.static_body_size[0] / 2),
                int(self.static_body.position.y),
                pr.GREEN,
            )
