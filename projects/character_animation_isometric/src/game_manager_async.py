import asyncio
import pyray as pr
import raylib as rl
from .utils import load_textures
from src.character import Character, States


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.textures = {}
        self.active_index_ptr:int = pr.ffi.new("int *", 0)
        self.ui_dropdown_edit_mode = False
        self.ui_selected_value: int = None

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        self.textures = load_textures()
        for k,v in self.textures.items():
            print(f"animation: {k}: {len(v)} animations")
        self.character = Character(position=pr.Vector2(0, 0), textures=self.textures)

    def update(self) -> None:
        if pr.gui_dropdown_box(
            pr.Rectangle(0, 40, 120, 20),
                "IDLE;RUN;PICKUP",
                self.active_index_ptr,
                self.ui_dropdown_edit_mode,
            ):
                self.ui_dropdown_edit_mode = not self.ui_dropdown_edit_mode
                self.ui_selected_value = self.active_index_ptr[0]

        self.character.update(selected_value=self.ui_selected_value)

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
            await asyncio.sleep(0)

    def draw(self) -> None:
        dt = pr.get_frame_time()
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        self.character.draw(dt=dt)
        pr.end_drawing()
        pr.draw_fps(0,0)
        pr.draw_text(f"{self.character.state}", 0, 20, 20, pr.GREEN)

    def end(self) -> None:
        pr.close_window()
