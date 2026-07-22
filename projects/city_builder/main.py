import asyncio
import pyray as pr
from src.game import Game


async def main() -> None:
    game = Game(
        width=640, height=360, fps_target=60, name="app", background_color=pr.BLACK
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())