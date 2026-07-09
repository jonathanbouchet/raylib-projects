import pyray as pr


class ChoiceContainer:
    def __init__(
        self, position: pr.Vector2, red_value: int, green_value: int, blue_value: int
    ) -> None:
        self.position = position
        self.red_value = red_value
        self.green_value = green_value
        self.blue_value = blue_value
        self.colors: list[pr.Color] = [
            pr.Color(self.red_value, 0, 0, 255),
            pr.Color(0, self.green_value, 0, 255),
            pr.Color(0, 0, self.blue_value, 255),
        ]

    def set_red_value(self, red_val: int) -> None:
        self.red_value = red_val

    def set_green_value(self, green_val: int) -> None:
        self.green_value = green_val

    def set_blue_value(self, blue_val: int) -> None:
        self.blue_value = blue_val

    def set_colors(self) -> list[pr.Color]:
        self.colors = [
            pr.Color(self.red_value, 0, 0, 255),
            pr.Color(0, self.green_value, 0, 255),
            pr.Color(0, 0, self.blue_value, 255),
        ]

    def update(self, r: int, g: int, b: int) -> None:
        self.set_red_value(red_val=r)
        self.set_green_value(green_val=g)
        self.set_blue_value(blue_val=b)
        self.set_colors()

    def draw(self) -> None:
        # outline
        rect = pr.Rectangle(self.position.x, self.position.y, 360, 120)
        pr.draw_rectangle_lines_ex(rect, 4, pr.WHITE)

        start = self.position.x

        for i in range(3):
            current_rect = pr.Rectangle(
                start + (i + 1) * 15 + 100 * (i), self.position.y + 10, 100, 100
            )
            pr.draw_rectangle_rec(current_rect, self.colors[i])
