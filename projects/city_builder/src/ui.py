import pyray as pr
import raylib as rl


class UIElement:
    def __init__(
        self,
        position: pr.Vector2,
        name: str,
        width: int,
        height: int,
        texture: pr.Texture,
        scale_factor: float,
    ) -> None:
        self.position = position
        self.name = name
        self.width = width
        self.height = height
        self.texture = texture
        self.scale_factor = scale_factor
        self.rect = pr.Rectangle(
            position.x,
            position.y,
            self.scale_factor * self.width,
            self.scale_factor * self.height,
        )
        self.is_selected: bool = False
        self.is_disabled = False

    def update(self) -> None:
        if pr.is_mouse_button_pressed(0):
            if (
                pr.check_collision_point_rec(pr.get_mouse_position(), self.rect)
                and not self.is_disabled
            ):
                self.is_selected = not self.is_selected
                print(f"selected tile: {self.name}, {self.is_selected}")

    def get_texture(self) -> pr.Texture:
        return self.texture

    def draw(self) -> None:
        pr.draw_texture_ex(self.texture, self.position, 0, self.scale_factor, pr.WHITE)
        if self.is_selected:
            pr.draw_rectangle_lines(
                int(self.position.x),
                int(self.position.y),
                int(self.width // 2),  # for visualization purposes only
                int(self.height // 2),  # for visualization purposes only
                pr.SKYBLUE,
            )
        else:
            pr.draw_rectangle_lines(
                int(self.position.x),
                int(self.position.y),
                int(self.width // 2),  # for visualization purposes only
                int(self.height // 2),  # for visualization purposes only
                pr.RED,
            )

    def set_status(self, status: bool) -> None:
        self.is_selected = status

    def get_status(self) -> bool:
        return self.is_selected


class UIContainer:
    def __init__(self, position: pr.Vector2, el: list[UIElement]) -> None:
        self.position = position
        self.ui_elements = el

    def update_status(self) -> int | None:
        statuses = [x.get_status() for x in self.ui_elements]
        if any(statuses):
            index = [i for i, val in enumerate(statuses) if val]
            # disable the non selected UI elements
            for cnt, el in enumerate(self.ui_elements):
                if cnt != index[0]:
                    el.is_disabled = True
            return index[0]
        else:
            # in that case no UI element has been selected so all should be enable
            for cnt, el in enumerate(self.ui_elements):
                el.is_disabled = False
        return None

    def get_selected(self) -> str:
        statuses = [x.get_status() for x in self.ui_elements]
        if any(statuses):
            index = [i for i, val in enumerate(statuses) if val]
            return self.ui_elements[index[0]].name

    def get_selected_tile_index(self) -> int:
        statuses = [x.get_status() for x in self.ui_elements]
        if any(statuses):
            index = [i for i, val in enumerate(statuses) if val]
            return index[0]

    def update(self) -> int | None:
        for el in self.ui_elements:
            el.update()
        return self.update_status()

    def draw(self) -> None:
        _ = [el.draw() for el in self.ui_elements]

    def get_names(self) -> None:
        return [x.name for x in self.ui_elements]
