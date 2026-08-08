import asyncio
import pyray as pr
import raylib as rl
from .utils import load_tilesets
from src.tileset import TextureAnim


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
        self.fps_value = pr.ffi.new("float *", 1.0)
        # self.fps_value_selected = pr.ffi.new("bool *", False)

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        self.textures = load_tilesets()
        self.animations = TextureAnim(textures=self.textures, position=pr.Vector2(self.width//2, self.height//2), scale=2)
        print(self.animations)
        print(f"{self.animations.current_animation_name}")

    def update(self) -> None:
        anims = self.animations.get_animation_names()
        if pr.gui_dropdown_box(
            pr.Rectangle(0, 60, 120, 20),
                ";".join(anims),
                self.active_index_ptr,
                self.ui_dropdown_edit_mode,
            ):
                self.ui_dropdown_edit_mode = not self.ui_dropdown_edit_mode
                self.ui_selected_value = self.active_index_ptr[0]
        pr.gui_slider(pr.Rectangle(0, 40, 120, 20), "0", "2", self.fps_value, 0.0, 2.0)

        self.animations.update(selected_value=self.ui_selected_value, fps_target_mult=self.fps_value[0])

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
            await asyncio.sleep(0)

    def draw(self) -> None:
        dt = pr.get_frame_time()
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        self.animations.draw(dt=dt, fps=self.fps_target*2)
        pr.end_drawing()
        pr.draw_fps(0,0)
        pr.draw_text(f"{self.animations.current_animation_name}", 0, 20, 20, pr.GREEN)

    def end(self) -> None:
        pr.close_window()
