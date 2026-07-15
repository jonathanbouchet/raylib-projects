import pyray as pr


class BaseButton:
    def __init__(self, position: pr.Vector2, size: pr.Vector2) -> None:
        self.position = position
        self.size = size
        self.state_changed = False

    def update(self) -> None:
        # print(f"{pr.check_collision_point_rec(pr.get_mouse_position(), self.rect)}, {pr.is_mouse_button_pressed(0)}")
        if pr.check_collision_point_rec(
            pr.get_mouse_position(), self.rect
        ) and pr.is_mouse_button_pressed(0):
            self.state_changed = not self.state_changed


class Button(BaseButton):
    def __init__(
        self,
        position: pr.Vector2,
        size: pr.Vector2,
        roundness: int,
        segments: int,
        base_color: pr.Color,
        changed_color: pr.Color,
    ) -> None:
        super().__init__(position=position, size=size)
        self.roundness = roundness
        self.segments = segments
        self.base_color = base_color
        self.changed_color = changed_color
        self.rect = pr.Rectangle(
            self.position.x, self.position.y, self.size.x, self.size.y
        )

    def draw(self) -> None:
        pr.draw_rectangle_rounded(
            self.rect, self.roundness, self.segments, self.base_color
        ) if not self.state_changed else pr.draw_rectangle_rounded(
            self.rect, self.roundness, self.segments, self.changed_color
        )
