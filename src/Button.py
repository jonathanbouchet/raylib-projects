import pyray as pr

""" 
this class is to provide a template for a toggle button 
- Button1 is using raylib primitive: you provide thw 2 colors to switch everytime the button is clicked
    -  roundness: int, segments: int are parameters to draw rounded edges
- Button2 is using textures provided to switch everytime the button is clicked

- instances:
button = Button(
    position=pr.Vector2(50, 100),
    size=pr.Vector2(150, 50),
    roundness=40,
    segments=50,
    base_color=pr.DARKGREEN,
    changed_color=pr.RED,
)

button2 = Button2(
    position=pr.Vector2(300, 100),
    size=pr.Vector2(0, 0),
    text1="assets/Button_Blue.png",
    text2="assets/Button_Blue_Pressed.png",
)
"""


class BaseButton:
    def __init__(self, position: pr.Vector2, size: pr.Vector2) -> None:
        self.position: pr.Vector2 = position
        self.size: pr.Vector2 = size
        self.state_changed: bool = False

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
        self.roundness: int = roundness
        self.segments: int = segments
        self.base_color: pr.Color = base_color
        self.changed_color: pr.Color = changed_color
        self.rect: pr.Rectangle = pr.Rectangle(
            self.position.x, self.position.y, self.size.x, self.size.y
        )

    def draw(self) -> None:
        pr.draw_rectangle_rounded(
            self.rect, self.roundness, self.segments, self.base_color
        ) if not self.state_changed else pr.draw_rectangle_rounded(
            self.rect, self.roundness, self.segments, self.changed_color
        )


class Button2(BaseButton):
    def __init__(
        self, position: pr.Vector2, size: pr.Vector2, text1: str, text2: str
    ) -> None:
        super().__init__(position=position, size=size)
        self.texture1: pr.Texture = pr.load_texture(text1)
        self.texture2: pr.Texture = pr.load_texture(text2)
        self.rect = pr.Rectangle(
            self.position.x, self.position.y, self.texture1.width, self.texture1.height
        )

    def draw(self):
        pr.draw_texture(
            self.texture1, int(self.position.x), int(self.position.y), pr.WHITE
        ) if not self.state_changed else pr.draw_texture(
            self.texture2, int(self.position.x), int(self.position.y), pr.WHITE
        )
