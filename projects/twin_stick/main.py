import pyray as pr
import asyncio
from src.game_manager import GameManager


async def main() -> None:
    game = GameManager(
        width=600,
        height=600,
        fps_target=60,
        name="app",
        background_color=pr.BLACK,
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
