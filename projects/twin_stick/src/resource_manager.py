import json


class ResourceManager:
    def __init__(self, resources_path: str) -> None:
        self.resources_path = resources_path
        self.resources_data = {}

        with open(self.resources_path, "r") as f:
            self.resources_data = json.load(f)

    def game_data(self) -> dict[str : int | str]:
        return self.resources_data.get("game")

    def player_data(self) -> dict[str : int | str]:
        return self.resources_data.get("player")
    
    def laser_data(self) -> dict[str: int | str]:
        return self.resources_data.get("laser")

    def asteroid_data(self) -> dict[str: int | str]:
        return self.resources_data.get("asteroid")
    
    def timer_game_data(self) -> dict[str: int | str]:
        return self.resources_data.get("timer_game")

    def print_game_data(self) -> str:
        print(self.resources_data.get("game"))
