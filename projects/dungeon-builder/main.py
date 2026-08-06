import asyncio
import pyray as pr
from src.game import Game


async def main() -> None:
    game = Game(
        width=896, 
        height=640, 
        fps_target=60, 
        name="app",
        background_color=pr.BLACK, 
        tile_x=6,
        tile_y=6
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
