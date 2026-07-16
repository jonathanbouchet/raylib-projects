import asyncio
import pyray as pr
import raylib as rl

width, height = 600, 600


class Level:
    def __init__(self, gamestate_manager):
        self.gamestate_manager = gamestate_manager
        self.name = "Level"

    def run(self):
        # logic
        if pr.is_key_pressed(rl.KEY_SPACE):
            self.gamestate_manager.set_state("start")
        # rendering
        pr.clear_background(pr.DARKBLUE)
        pr.draw_fps(0, 0)
        pr.draw_text(f"CURRENT STATE: {self.name}", 0, 20, 20, pr.GREEN)
        pr.draw_line(width // 2, 0, width // 2, height, pr.RED)
        pr.draw_line(0, height // 2, width, height // 2, pr.RED)


class Start:
    def __init__(self, gamestate_manager):
        self.gamestate_manager = gamestate_manager
        self.name = "Start"

    def run(self):
        # logic
        if pr.is_key_pressed(rl.KEY_SPACE):
            self.gamestate_manager.set_state("level")

        # rendering
        pr.clear_background(pr.DARKGREEN)
        pr.draw_fps(0, 0)
        pr.draw_text(f"CURRENT STATE: {self.name}", 0, 20, 20, pr.GREEN)
        pr.draw_line(width // 2, 0, width // 2, height, pr.RED)
        pr.draw_line(0, height // 2, width, height // 2, pr.RED)


class GameStateManager:
    def __init__(self, currentState):
        self.current_state = currentState

    def get_state(self):
        return self.current_state

    def set_state(self, new_state):
        self.current_state = new_state


class Game:
    def __init__(self, width, height) -> None:
        pr.init_window(width, height, "app")
        pr.set_target_fps(60)

        self.gameStateManager = GameStateManager("start")
        self.start = Start(self.gameStateManager)
        self.level = Level(self.gameStateManager)

        self.states = {"start": self.start, "level": self.level}

    async def run(self) -> None:
        while not pr.window_should_close():
            pr.begin_drawing()
            # logic here
            self.states[self.gameStateManager.get_state()].run()
            # rendering
            pr.end_drawing()

            await asyncio.sleep(0)

        pr.close_window()


async def main() -> None:
    game = Game(width=width, height=height)
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
