from pathlib import Path
import pyray as pr

THIS_DIR = (Path(__file__).parent / "player_anims").resolve()
print(f"{str(THIS_DIR)=}")


def load_textures() -> dict[str, list[pr.Texture2D]]:
    """load_textures for different animations
    each animation contains severals png

    :return: _description_
    :rtype: dict[str, list[pr.Texture2D]]
    """
    textures = {}
    for anim in ["idle", "run"]:
        anim_dir = Path(f"{THIS_DIR}/{anim}")
        file_count = sum(1 for x in anim_dir.iterdir() if x.is_file())
        textures[anim] = [
            pr.load_texture(f"{str(anim_dir)}/{i}.png") for i in range(file_count)
        ]
    return textures
