import asyncio
from pathlib import Path
from src.game_manager import Game
from src.resource_manager import ResourceManager

THIS_DIR = (Path(__file__).parent / "src").resolve()


async def main() -> None:

    resource_manager = ResourceManager(resources_path=f"{THIS_DIR}/resources.json")
    resource_manager.print_game_data()

    game = Game(resource_manager=resource_manager)
    game.init()
    game.grid.print()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
