import pyray as pr
from color_candidate import ColorContainer


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
        self.red_value_picked: pr.Color = None
        self.green_value_picked: pr.Color = None
        self.blue_value_picked: pr.Color = None

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

    def get_color_picked(self, color_container: ColorContainer) -> pr.Color:
        return color_container.colored_picked

    def update(
        self,
        r: int,
        g: int,
        b: int,
        red_container: ColorContainer,
        green_container: ColorContainer,
        blue_container: ColorContainer,
    ) -> None:
        self.set_red_value(red_val=r)
        self.set_green_value(green_val=g)
        self.set_blue_value(blue_val=b)
        self.set_colors()
        self.red_value_picked = self.get_color_picked(color_container=red_container)
        self.green_value_picked = self.get_color_picked(color_container=green_container)
        self.blue_value_picked = self.get_color_picked(color_container=blue_container)
        # if self.red_value_picked:
        #     print(f"red colored picked: {self.red_value_picked}")

    def draw(self, is_generated: bool) -> None:
        # outline
        if is_generated:
            rect = pr.Rectangle(self.position.x, self.position.y, 360, 120)
            pr.draw_rectangle_lines_ex(rect, 1, pr.WHITE)

        if self.red_value_picked:
            red_rect = pr.Rectangle(
                self.position.x + 15, self.position.y + 10, 100, 100
            )
            pr.draw_rectangle_rec(red_rect, self.red_value_picked)

        if self.green_value_picked:
            green_rect = pr.Rectangle(
                self.position.x + 15 + 100 + 15, self.position.y + 10, 100, 100
            )
            pr.draw_rectangle_rec(green_rect, self.green_value_picked)

        if self.blue_value_picked:
            blue_rect = pr.Rectangle(
                self.position.x + 15 + 100 + 15 + 100 + 15,
                self.position.y + 10,
                100,
                100,
            )
            pr.draw_rectangle_rec(blue_rect, self.blue_value_picked)

        # placeholder for testing
        # start = self.position.x
        # for i in range(3):
        #     current_rect = pr.Rectangle(
        #         start + (i + 1) * 15 + 100 * (i), self.position.y + 10, 100, 100
        #     )
        #     pr.draw_rectangle_rec(current_rect, self.colors[i])
