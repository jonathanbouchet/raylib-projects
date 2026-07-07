import random
import math
import platform
import pyray as pr
import raylib as rl
from pathlib import Path
import asyncio
import json
from enum import Enum
from typing import Any
from game_manager import GameManager
from resource_manager import ResourceManager


async def main():
    print("start")
    resources_manager = ResourceManager(resources_path="./resources.json")
    print("resources_manager done")
    resources_manager.print_game_data()
    game = GameManager(
        resources_manager = resources_manager
    )
    print("game_manager done")
    game.init()
    print("init done")
    await game.run()
    game.end()


asyncio.run(main())
