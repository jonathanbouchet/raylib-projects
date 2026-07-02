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

    # extract player data
    def player_data(self) -> dict[str : int | str]:
        return self.resources_data.get("player")

    # extract laser data
    def laser_data(self) -> dict[str : int | str]:
        return self.resources_data.get("laser")

    # extract asteroid data
    def asteroid_data(self) -> dict[str : int | str]:
        return self.resources_data.get("asteroid")

    # extract scorer data
    def scorer_data(self) -> dict[str:int]:
        return self.resources_data.get("scorer")

    # extract shader data
    def shaders(self) -> dict[str, str]:
        return self.resources_data.get("shader")

    # extract explosion data
    def explosion_data(self) -> dict[str, str]:
        return self.resources_data.get("explosion")

    # print game data
    def print_game_data(self) -> str:
        print(self.resources_data.get("scorer"))
