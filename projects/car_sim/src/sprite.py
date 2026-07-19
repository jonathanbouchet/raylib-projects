import pyray as pr


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        position_board: pr.Vector2,
        radius: int,
        color: pr.Color,
        debug: bool,
    ) -> None:
        self.position = position
        self.position_board = position_board
        self.radius = radius
        self.color = color
        self.debug = debug

    def update(self) -> None:
        pass

    def move(self) -> None:
        pass

    def set_position(self, target: pr.Vector2) -> None:
        self.position_board = target

    def get_board_position(self) -> tuple[int, int]:
        return [int(self.position_board.x), int(self.position_board.y)]

    def draw(self) -> None:
        # pr.draw_circle_v(
        #     pr.Vector2(
        #         self.position.x - self.radius,
        #         self.position.y - self.radius
        #     ),
        #     self.radius,
        #     self.color
        # )
        pr.draw_circle_v(
            pr.Vector2(
                (self.position_board.x + 1) * 64 - self.radius,  # testing
                (self.position_board.y + 1) * 64 - self.radius,
            ),
            self.radius,
            self.color,
        )
