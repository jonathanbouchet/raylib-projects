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

    # extract grid data
    def grid_data(self) -> dict[str : int | str]:
        return self.resources_data.get("grid")

    # print game data
    def print_game_data(self) -> str:
        print(self.resources_data.get("grid"))
