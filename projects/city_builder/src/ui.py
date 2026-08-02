import pyray as pr
from .world import World


class UIElement:
    def __init__(
        self,
        id: int, # unique id
        position: pr.Vector2, # position of the element RELATIVe to the top left corner of the container
        name: str, # texture name, e.g: building01
        width: int, # texture width in pixels
        height: int, # texture height in pixels
        texture: pr.Texture, # texture itself
        scale_factor: float, # scaling factor ; used to display a smaller version of the original texture
    ) -> None:
        self.id = id
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
        if self.is_selected:
            # pr.draw_rectangle_rounded(self.rect, 0.75, 20, pr.GREEN)
            pr.draw_rectangle_lines(
                int(self.position.x),
                int(self.position.y),
                int(self.width // 2),  # for visualization purposes only
                int(self.height // 2),  # for visualization purposes only
                pr.YELLOW,
            )
        pr.draw_texture_ex(self.texture, self.position, 0, self.scale_factor, pr.WHITE)

    def set_status(self, status: bool) -> None:
        self.is_selected = status

    def get_status(self) -> bool:
        return self.is_selected


class UIContainer:
    def __init__(
            self, 
            position: pr.Vector2, # position in game coordinates (pixels) of the top left corner
            el: list[str], world: World # list of texture names used by the UI
        ) -> None:
        self.position = position
        self.ui_element_names: list[str] = el
        self.ui_elements: list[UIElement] = [] # list of UI Element
        self.add_ui_elements(world=world)

    def add_ui_elements(self, world: World) -> None:
        for cnt, element_name in enumerate(self.ui_element_names):
            ui_element = UIElement(
                id=cnt,
                position=pr.Vector2(self.position.x, self.position.y + cnt * 30),
                name=element_name,
                width=world.textures.get(element_name).get_texture().width,
                height=world.textures.get(element_name).get_texture().height,
                texture=world.textures.get(element_name).get_texture(),
                scale_factor=0.5,
            )
            self.ui_elements.append(ui_element)

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

    def update(self, current_selection: int) -> int | None:
        if pr.is_mouse_button_pressed(0):
            # reset all UI elements statuses
            for el in self.ui_elements:
                el.is_selected = False
            for el in self.ui_elements:
                if pr.check_collision_point_rec(pr.get_mouse_position(), el.rect):
                    print(f"CLICKED: {el.name}")
                    el.is_selected = True
                    return el.id
        return current_selection



        # for el in self.ui_elements:
        #     el.update()
        # statuses = [x.get_status() for x in self.ui_elements]
        # print(f"{statuses=}")

        # return self.update_status()

    def draw(self) -> None:
        _ = [el.draw() for el in self.ui_elements]

    def get_names(self) -> None:
        return [x.name for x in self.ui_elements]
