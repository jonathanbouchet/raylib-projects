import asyncio
from enum import Enum
import pyray as pr
from Button import Button


class GameState(Enum):
    INIT = 0
    RUN = 1
    SETTINGS = 2
    END = 3


class ScreenState(Enum):
    TITLE = 0
    MAIN = 1
    SETTINGS = 2


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        title_background_color: pr.Color,
        main_background_color: pr.Color,
        settings_background_color: pr.Color,
        title_screen_button_1: Button,
        title_screen_button_2: Button,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.title_background_color = title_background_color
        self.main_background_color = main_background_color
        self.settings_background_color = settings_background_color
        self.game_state = GameState.INIT
        self.screen_state = ScreenState.TITLE
        self.title_screen_button_1 = title_screen_button_1
        self.title_screen_button_2 = title_screen_button_2
        self.buttons: list[Button] = [
            self.title_screen_button_1,
            self.title_screen_button_2,
        ]

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

    def update(self) -> None:
        _ = [button.update() for button in self.buttons]
        if self.game_state == GameState.INIT:
            self.draw_title()
        if self.game_state == GameState.RUN:
            self.draw()
        if self.game_state == GameState.SETTINGS:
            self.draw_setting()

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()

    def draw(self) -> None:
        """main game loop"""
        pr.begin_drawing()
        pr.clear_background(self.main_background_color)

        pr.draw_text("MAIN", self.width // 2, 100, 60, pr.DARKBLUE)
        if pr.gui_button(pr.Rectangle(300, 300, 100, 40), "SETTINGS"):
            self.game_state = GameState.SETTINGS
            self.screen_state = ScreenState.SETTINGS

        pr.draw_fps(0, 0)
        pr.draw_text(f"GAME:{self.game_state}", 0, 20, 20, pr.GREEN)
        pr.draw_text(f"SCREEN:{self.screen_state}", 0, 40, 20, pr.GREEN)
        pr.draw_text(f"RUN TIME:{int(pr.get_time())}", 0, 60, 20, pr.GREEN)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)
        pr.draw_line(0, self.height // 2, 0, self.height // 2, pr.RED)
        pr.end_drawing()

    def draw_title(self) -> None:
        """title screen"""
        pr.begin_drawing()
        pr.clear_background(self.title_background_color)

        pr.draw_text("TITLE", self.width // 2, 100, 60, pr.DARKBLUE)

        self.title_screen_button_1.draw()
        self.title_screen_button_2.draw()

        # if pr.gui_button(pr.Rectangle(150, 300, 100, 40), "START"):
        #     self.game_state = GameState.RUN
        #     self.screen_state = ScreenState.MAIN
        # if pr.gui_button(pr.Rectangle(350, 300, 100, 40), "SETTINGS"):
        #     self.game_state = GameState.SETTINGS
        #     self.screen_state = ScreenState.SETTINGS

        pr.draw_fps(0, 0)
        pr.draw_text(f"GAME:{self.game_state}", 0, 20, 20, pr.GREEN)
        pr.draw_text(f"SCREEN:{self.screen_state}", 0, 40, 20, pr.GREEN)
        pr.draw_text(f"RUN TIME:{int(pr.get_time())}", 0, 60, 20, pr.GREEN)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)
        pr.draw_line(0, self.height // 2, 0, self.height // 2, pr.RED)
        pr.end_drawing()

    def draw_setting(self) -> None:
        """settings screen"""
        pr.begin_drawing()
        pr.clear_background(self.settings_background_color)

        pr.draw_text("SETTINGS", self.width // 2, 100, 60, pr.DARKBLUE)
        if pr.gui_button(pr.Rectangle(300, 300, 100, 40), "TITLE"):
            self.game_state = GameState.INIT
            self.screen_state = ScreenState.TITLE

        pr.draw_fps(0, 0)
        pr.draw_text(f"GAME:{self.game_state}", 0, 20, 20, pr.GREEN)
        pr.draw_text(f"SCREEN:{self.screen_state}", 0, 40, 20, pr.GREEN)
        pr.draw_text(f"RUN TIME:{int(pr.get_time())}", 0, 60, 20, pr.GREEN)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)
        pr.draw_line(0, self.height // 2, 0, self.height // 2, pr.RED)
        pr.end_drawing()

    def end(self) -> None:
        pr.close_window()


async def main() -> None:
    button1 = Button(
        position=pr.Vector2(150, 300),
        size=pr.Vector2(150, 50),
        roundness=40,
        segments=50,
        base_color=pr.DARKGREEN,
        changed_color=pr.RED,
    )

    button2 = Button(
        position=pr.Vector2(350, 300),
        size=pr.Vector2(150, 50),
        roundness=40,
        segments=50,
        base_color=pr.DARKGREEN,
        changed_color=pr.RED,
    )

    game = Game(
        width=600,
        height=600,
        fps_target=60,
        name="app",
        title_background_color=pr.BLACK,
        main_background_color=pr.RAYWHITE,
        settings_background_color=pr.DARKGRAY,
        title_screen_button_1=button1,
        title_screen_button_2=button2,
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
