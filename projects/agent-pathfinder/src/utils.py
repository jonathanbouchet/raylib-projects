import pyray as pr
from pathlib import Path
import json
import xmltodict

THIS_DIR = (Path(__file__).parent.parent).resolve()


def parse_map(map_name: str):
    print(map_name)
    with open(map_name, "r") as f:
        map_dict = json.load(f)
    return map_dict


def parse_tileset(tileset_name: str):
    with open(tileset_name, "r", encoding="utf-8") as f:
        data_dict = xmltodict.parse(f.read())
    return data_dict


def load_textures():
    """load textures used throughout the game"""
    grass = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_25.png")
    dirt = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_26.png")
    straight_vertical = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_01.png")
    straight_horizontal = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_13.png")
    crossing = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_10.png")
    curve_B_R = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_02.png")
    curve_L_B = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_03.png")
    curve_T_R = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_14.png")
    curve_L_T = pr.load_texture(f"{THIS_DIR}/assets/roadTexture_15.png")
    agent = pr.load_texture(f"{THIS_DIR}/assets/compact_blue.png")

    return {
        "curve_L_B": {
            "texture": curve_L_B,
            "id": 0,
            "path": [pr.Vector2(0, 32), pr.Vector2(20, 40), pr.Vector2(32, 64)],
        },
        "curve_L_T": {
            "texture": curve_L_T,
            "id": 1,
            "path": [pr.Vector2(0, 32), pr.Vector2(20, 24), pr.Vector2(32, 0)],
        },
        "curve_B_R": {
            "texture": curve_B_R,
            "id": 2,
            "path": [pr.Vector2(32, 64), pr.Vector2(40, 44), pr.Vector2(64, 32)],
        },
        "curve_T_R": {
            "texture": curve_T_R,
            "id": 3,
            "path": [pr.Vector2(32, 0), pr.Vector2(40, 26), pr.Vector2(64, 32)],
        },
        "straight_L_R": {
            "texture": straight_horizontal,
            "id": 4,
            "path": [pr.Vector2(0, 32), (32, 32), (64, 32)],
        },
        "straight_T_B": {
            "texture": straight_vertical,
            "id": 5,
            "path": [pr.Vector2(32, 0), (32, 32), (32, 64)],
        },
        "crossing": {"texture": crossing, "id": 6, "path": []},
        "grass": {"texture": grass, "id": 7, "path": []},
        "dirt": {"texture": dirt, "id": 8, "path": []},
        "agent": {"texture": agent, "id": 9, "path": []},
    }


dict_texture_name_to_game = {
    "roadTexture_25.png": "grass",
    "roadTexture_26.png": "dirt",
    "roadTexture_01.png": "straight_T_B",
    "roadTexture_13.png": "straight_L_R",
    "roadTexture_10.png": "crossing",
    "roadTexture_02.png": "curve_B_R",
    "roadTexture_03.png": "curve_L_B",
    "roadTexture_14.png": "curve_T_R",
    "roadTexture_15.png": "curve_L_T",
    "compact_blue.png": "agent",
}
