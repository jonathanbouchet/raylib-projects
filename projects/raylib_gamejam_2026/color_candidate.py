import pyray as pr


class ColorContainer:
    def __init__(
        self,
        position: pr.Vector2,
        value: int,
        outline_color: pr.Color,
        base_color: pr.Color,
    ) -> None:
        self.position = position
        self.value = value
        self.outline_color = outline_color
        self.base_color = base_color

    def draw(self) -> None:
        # outline
        rect = pr.Rectangle(self.position.x, self.position.y, 200, 200)
        pr.draw_rectangle_lines_ex(rect, 4, self.outline_color)

        # choices: 1 is the correct value, the other are fake colors
        tl_rect = pr.Rectangle(self.position.x + 20, self.position.y + 20, 80, 80)
        pr.draw_rectangle_rec(tl_rect, self.base_color)

        tr_rect = pr.Rectangle(self.position.x + 20 + 80, self.position.y + 20, 80, 80)
        pr.draw_rectangle_rec(tr_rect, pr.GRAY)

        bl_rect = pr.Rectangle(self.position.x + 20, self.position.y + 20 + 80, 80, 80)
        pr.draw_rectangle_rec(bl_rect, pr.DARKGRAY)

        br_rect = pr.Rectangle(
            self.position.x + 20 + 80, self.position.y + 20 + 80, 80, 80
        )
        pr.draw_rectangle_rec(br_rect, pr.WHITE)
