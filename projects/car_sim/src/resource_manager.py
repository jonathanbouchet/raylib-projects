import json


class ResourceManager:
    """this class reads the resources.json and provides access to its keys"""

    def __init__(self, resources_path: str) -> None:
        self.resources_path = resources_path
        self.resources_data = {}

        with open(self.resources_path, "r") as f:
            self.resources_data = json.load(f)

    # extract game data
    def game_data(self) -> dict[str : int | str]:
        return self.resources_data.get("game")

    # extract board data
    def board_data(self) -> dict[str : int | str]:
        return self.resources_data.get("board")
    
    # player sprite
    def player_sprite(self) -> dict[str: int | str | tuple]:
        return self.resources_data.get("player_sprite")

    # print game data
    def print_game_data(self) -> str:
        print(self.resources_data.get("board"))
