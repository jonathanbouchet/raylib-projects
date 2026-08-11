import asyncio
import pyray as pr


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
        tile_x: int,
        tile_y: int,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.tile_x = tile_x
        self.tile_y = tile_y

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

    def update(self) -> None:
        dt = pr.get_frame_time()

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            pr.begin_drawing()
            self.draw()
            self.debug()
            pr.end_drawing()
            await asyncio.sleep(0)

    def debug(self) -> None:
        # debug
        pr.clear_background(self.background_color)
        if pr.get_frame_time():
            pr.draw_text(f"FPS: {int(1.0 / pr.get_frame_time())}", 0, 0, 20, pr.RED)

    def draw(self) -> None:
        pass

    def end(self) -> None:
        pr.close_window()
