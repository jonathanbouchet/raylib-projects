import pyray as pr
import math


class Body:
    def __init__(self, position: pr.Vector3, radius: int, color: pr.Color):
        self.position: pr.Vector3 = position
        self.radius: int = radius
        self.color: pr.Color = color

    def draw(self) -> None:
        pr.draw_sphere(self.position, self.radius, self.color)


class Star(Body):
    def __init__(self, position: pr.Vector3, radius: int, color: pr.Color):
        super().__init__(position=position, radius=radius, color=color)


class Planetoid(Body):
    def __init__(
        self,
        position: pr.Vector3,
        radius: int,
        color: pr.Color,
        speed_revolution: int,
        distance_to_center: int,
    ):
        super().__init__(position=position, radius=radius, color=color)
        self.speed_revolution: int = speed_revolution
        self.distance_to_center: int = distance_to_center

    def draw_trajectory(self):
        pr.draw_circle_3d(
            pr.Vector3(0, 0, 0),  # center
            self.distance_to_center,
            pr.Vector3(1, 0, 0),
            90,
            self.color,
        )

    def update(self, dl: float, x_offset: float, z_offset: float):
        self.position.x = x_offset + self.distance_to_center * math.cos(
            dl * self.speed_revolution * 2 * math.pi
        )
        self.position.z = z_offset + self.distance_to_center * math.sin(
            dl * self.speed_revolution * 2 * math.pi
        )
        self.position.y = self.position.y
        # self.move()

    def move(self):
        self.draw()
