import pyray as pr
from pathlib import Path

THIS_DIR = (Path(__file__).parent.parent).resolve()


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

    return {
        "curve_L_B": {"texture": curve_L_B, "id": 0, "path": [pr.Vector2(0, 32), pr.Vector2(20, 40), pr.Vector2(32, 64)]},
        "curve_L_T": {"texture": curve_L_T, "id": 1, "path": [pr.Vector2(0, 32), pr.Vector2(20, 24), pr.Vector2(32, 0)]},
        "curve_B_R": {"texture": curve_B_R, "id": 2, "path": [pr.Vector2(32, 64), pr.Vector2(40, 44), pr.Vector2(64, 32)]},
        "curve_T_R": {"texture": curve_T_R, "id": 3, "path": [pr.Vector2(32, 0), pr.Vector2(40, 26), pr.Vector2(64, 32)]},
        "straight_L_R": {"texture": straight_horizontal, "id": 4, "path": [pr.Vector2(0, 32), (64, 32)]},
        "straight_T_B": {"texture": straight_vertical, "id": 5, "path": [pr.Vector2(32, 0), (32, 64)]},
        "crossing": {"texture": crossing, "id": 6, "path": []},
        "grass": {"texture": grass, "id": 7, "path": []},
        "dirt": {"texture": dirt, "id": 8, "path": []},
    }
