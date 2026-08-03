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

    # extract textures data
    def textures_data(self) -> dict[str:str]:
        return self.resources_data.get("textures")

    def textures_data_path(self) -> dict[str, str]:
        """
        - format the textures metadata as k,v "path_to_png":"tilen_name"
        - this is used when loading a map
        """
        textures = self.resources_data.get("textures")
        tmp = {}
        for k, v in textures.items():
            tmp[v.get("path")] = k
        return tmp

    # extract maps data
    def maps_data(self) -> dict[str, dict[str, str]]:
        return self.resources_data.get("maps")
