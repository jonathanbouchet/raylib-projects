import pyray as pr


class Cell:
    def __init__(
        self,
        position: pr.Vector2,
        size: pr.Vector2,
        offset_x: int,
        offset_y: int,
        color: pr.Color,
    ) -> None:
        self.position = position
        self.size = size
        self.color = color
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.state_changed: bool = False
        self.clicked: bool = False
        self.rect = pr.Rectangle(
            self.position.x + self.offset_x,
            self.position.y + self.offset_y,
            self.size.x,
            self.size.y,
        )

    def update(self) -> None:
        # print(f"{pr.check_collision_point_rec(pr.get_mouse_position(), self.rect)}, {pr.is_mouse_button_pressed(0)}")
        if pr.check_collision_point_rec(
            pr.get_mouse_position(), self.rect
        ) and pr.is_mouse_button_pressed(0):
            self.state_changed = not self.state_changed
            self.clicked = True

    def draw(self):
        pr.draw_rectangle_rec(self.rect, self.color)
        if self.state_changed:
            pr.draw_rectangle_lines_ex(self.rect, 2, pr.RAYWHITE)
            pr.draw_text(
                f"{self.color}", int(self.rect.x), int(self.rect.y), 10, pr.BLACK
            )


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
        self.interactive_area: list[Cell] = [
            Cell(
                position=pr.Vector2(self.position.x, self.position.y),
                size=pr.Vector2(80, 80),
                offset_x=20,
                offset_y=20,
                color=self.base_color,
            ),
            Cell(
                position=pr.Vector2(self.position.x, self.position.y),
                size=pr.Vector2(80, 80),
                offset_x=20 + 80,
                offset_y=20,
                color=pr.DARKGRAY,
            ),
            Cell(
                position=pr.Vector2(self.position.x, self.position.y),
                size=pr.Vector2(80, 80),
                offset_x=20,
                offset_y=20 + 80,
                color=pr.GRAY,
            ),
            Cell(
                position=pr.Vector2(self.position.x, self.position.y),
                size=pr.Vector2(80, 80),
                offset_x=20 + 80,
                offset_y=20 + 80,
                color=pr.BEIGE,
            ),
        ]

    def update(self) -> None:
        _ = [c.update() for c in self.interactive_area]

    def draw(self) -> None:
        # outline
        rect = pr.Rectangle(self.position.x, self.position.y, 200, 200)
        pr.draw_rectangle_lines_ex(rect, 1, self.outline_color)
        _ = [c.draw() for c in self.interactive_area]

        # this works -> do not delete
        # choices: 1 is the correct value, the other are fake colors
        # tl_rect = pr.Rectangle(self.position.x + 20, self.position.y + 20, 80, 80)
        # pr.draw_rectangle_rec(tl_rect, self.base_color)

        # tr_rect = pr.Rectangle(self.position.x + 20 + 80, self.position.y + 20, 80, 80)
        # pr.draw_rectangle_rec(tr_rect, pr.GRAY)

        # bl_rect = pr.Rectangle(self.position.x + 20, self.position.y + 20 + 80, 80, 80)
        # pr.draw_rectangle_rec(bl_rect, pr.DARKGRAY)

        # br_rect = pr.Rectangle(
        #     self.position.x + 20 + 80, self.position.y + 20 + 80, 80, 80
        # )
        # pr.draw_rectangle_rec(br_rect, pr.WHITE)
