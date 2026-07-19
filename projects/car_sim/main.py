import asyncio
from pathlib import Path
from src.game_manager import Game
from src.resource_manager import ResourceManager

THIS_DIR = (Path(__file__).parent / "src").resolve()


async def main() -> None:
    """
    - main entry oint of the game
    - resource_manager is called first and added as a member of the Game
        - it defines the different constants in the game., such as windoe size, color of assets, etc ...
    - game.init() is called independently since it needs the window size.; it is also needed to call it before loading any textures
    """

    resource_manager = ResourceManager(resources_path=f"{THIS_DIR}/resources.json")
    resource_manager.print_game_data()

    game = Game(resource_manager=resource_manager)
    game.init()
    game.board.print()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
