from pathlib import Path
from typing import Any
import pyray as pr

THIS_DIR = (Path(__file__).parent.parent / "assets").resolve()
print(f"{str(THIS_DIR)=}")


def load_tilesets() -> dict[str: dict[str, Any]]:
    """load animations as a tileset"""
    return {
        "explosion": {
            "texture": pr.load_texture(f"{THIS_DIR}/Explosions.png"),
            "tile_size": 192
        },

        "foam": {
            "texture": pr.load_texture(f"{THIS_DIR}/Foam.png"),
            "tile_size": 192
        },
        "rock": 
        {
            "texture": pr.load_texture(f"{THIS_DIR}/Rocks_01.png"),
            "tile_size": 128
        },
        "walk":
        {
            "texture": pr.load_texture(f"{THIS_DIR}/Walk.png"),
            "tile_size": 128
        }
    }


def load_textures() -> dict[str, list[pr.Texture]]:
    """load_textures for different animations
    each animation contains severals png

    :return: _description_
    :rtype: dict[str, list[pr.Texture2D]]
    """
    textures = {}
    for anim in ["idle_SE", "run_SE", "pickup_SE"]:
        name_anim: str = ""
        if anim == "idle_SE":
            name_anim = "Idle"
        elif anim == "run_SE":
            name_anim = "Run"
        elif anim == "pickup_SE":
            name_anim = "Pickup"
        else:
            print(f"texture not found for :{anim}")
            return
        anim_dir = Path(f"{THIS_DIR}/{anim}")
        file_count = sum(1 for x in anim_dir.iterdir() if x.is_file())
        textures[anim] = [
            pr.load_texture(f"{str(anim_dir)}/Male_2_{name_anim}{i}.png") for i in range(file_count)
        ]
    return textures