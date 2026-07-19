import pyray as pr

class Sprite:
    def __init__(self, position: pr.Vector2, position_board: pr.Vector2, radius: int, color: pr.Color, debug: bool) -> None:
        self.position = position
        self.position_board = position_board
        self.radius = radius
        self.color = color
        self.debug = debug

    def update(self) -> None:
        pass

    def move(self) -> None:
        pass

    def set_position(seff) -> None:
        pass

    def draw(self) -> None:
        pr.draw_circle_v(
            pr.Vector2(
                self.position.x - self.radius, 
                self.position.y - self.radius
            ), 
            self.radius, 
            self.color
        )