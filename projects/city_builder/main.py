import asyncio
import pyray as pr
from src.game import Game


async def main() -> None:
    game = Game(
        width=1080, height=720, fps_target=60, name="app", background_color=pr.BLACK, tile_x=10, tile_y=10
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())