import asyncio
from pathlib import Path
import pyray as pr
from src.resource_manager import ResourceManager
from src.game import Game

THIS_DIR = (Path(__file__).parent/"src").resolve()

async def main() -> None:
    resource_manager = ResourceManager(resources_path=f"{THIS_DIR}/resources.json")
    print(f"{resource_manager.resources_data}")
    game = Game(resource_manager = resource_manager)
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
