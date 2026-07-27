import asyncio
from pathlib import Path
import pyray as pr
from src.resource_manager import ResourceManager
from src.game import Game

THIS_DIR = (Path(__file__).parent/"src").resolve()

async def main() -> None:
    resource_manager = ResourceManager(resources_path=f"{THIS_DIR}/resources.json")
    print(f"{resource_manager.resources_data}")
    game = Game(
        width=resource_manager.game_data().get("width"),
        height=resource_manager.game_data().get("height"),
        fps_target=resource_manager.game_data().get("fps_target"),
        name=resource_manager.game_data().get("name"),
        background_color=resource_manager.game_data().get("background_color"),
        tile_x=resource_manager.game_data().get("tile_x"),
        tile_y=resource_manager.game_data().get("tile_y"),
        debug=resource_manager.game_data().get("debug")
    )
    game.init()
    await game.run()
    game.end()


if __name__ == "__main__":
    asyncio.run(main())
