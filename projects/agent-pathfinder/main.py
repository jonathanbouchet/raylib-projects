import asyncio
import pyray as pr
from src.game import Game


async def main() -> None:
    game = Game(
        # width=512,
        # height=512,
        width=640,
        height=640,
        fps_target=60,
        name="app",
        background_color=pr.BLACK,
        # tile_x=8,
        # tile_y=8,
        tile_x=10,
        tile_y=10,
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
