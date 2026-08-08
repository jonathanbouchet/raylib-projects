from enum import Enum
from typing import Any
import pyray as pr

""" 
this class is to provide an animation based on tile. 
Character's animations can be found in separate png's, or stitch together into 1 png file. 
The goal is then to access each of the texture to render an animation
Note:
- scale_factor can either be < or > than 1
- the speed of the animation is driver by the current FPS and the number of animations.
    - for fastest animation, increase the anim_index by a factor:
        self.anim_index += my_factor * self.texture_len/fps
- there's a check when drawing the animations on the FPS value. Indeed I see that at the very beginninng, FPS (in Raylib) is set to 0:
    dt=0.0, fps=0
    dt=0.0170668326318264, fps=1758
    dt=0.039377789944410324, fps=1758
    dt=0.01689937524497509, fps=883
- instance example: foam = TextureAnim(texture_path="./Foam.png", position=pr.Vector2(100, 200), tile_size=192, scale=1.0)
"""


class TextureAnim:
    def __init__(
        self,
        textures: list[pr.Texture],
        position: pr.Vector2,
        scale: float = 1.0,
    ) -> None:
        self.tilesets = self.extract_tilesets(textures=textures)
        self.position = position  # position of the texture
        self.anim_index = 0
        self.scale_factor = scale
        self.fps_target_mult: float = 1.0
        self.animation_row: int = 0

    def extract_tilesets(self, textures: dict[str: dict[str, Any]]):
        tilesets = {}
        for texture_name, texture_data in textures.items():
            tilesets[texture_name] = {
                "texture": texture_data.get('texture'),
                "tile_size": texture_data.get('tile_size'),
                "num_rows": int(texture_data.get('texture').width / texture_data.get('tile_size')),
                "num_cols": int(texture_data.get('texture').height / texture_data.get('tile_size'))
            }
        self.animations = tilesets
        self.current_animation_name = list(tilesets.keys())[0]

    def update(self, selected_value: int, fps_target_mult: float, animation_row: int) -> None:
        if selected_value is not None:
            self.current_animation_name = list(self.animations.keys())[selected_value]
        if fps_target_mult is not None:
            self.fps_target_mult = fps_target_mult
        if animation_row is not None: # make sure it doesn't mess with the other animations that only have 1 row
            self.animation_row = animation_row

    def get_animation_names(self) -> list[str]:
        return list(self.animations.keys())

    def __str__(self) -> str:
        res = ""
        for texture_name, texture_data in self.animations.items():
            res += f"name:{texture_name}, tile size: {texture_data.get('tile_size')}, rows: {texture_data.get('num_rows')}, cols: {texture_data.get('num_cols')}\n"
        return res

    def draw(self, dt: float, fps: int) -> None:
        if fps == 0:
            return
        # get the current animation data
        current_animation_data = self.animations.get(self.current_animation_name)
        current_animation_frames = current_animation_data.get('texture')
        current_num_row = current_animation_data.get('num_rows')
        current_num_col = current_animation_data.get('num_cols')
        current_tile_size = current_animation_data.get('tile_size')

        # first animation start at index=0
        tile_x = int(self.anim_index) * current_tile_size
        tile_y = self.animation_row * current_tile_size

        # point to the ith animation frame in the texture
        source_rec = pr.Rectangle(tile_x, tile_y, current_tile_size, current_tile_size)

        dest_rec = pr.Rectangle(
            self.position.x,
            self.position.y,
            int(current_tile_size * self.scale_factor),
            int(current_tile_size * self.scale_factor),
        )
        pr.draw_texture_pro(
            current_animation_frames,
            source_rec,
            dest_rec,
            pr.Vector2(dest_rec.width / 2, dest_rec.height / 2),
            0,
            pr.WHITE,
        )
        self.anim_index += current_num_row / int(fps*self.fps_target_mult)
        if self.anim_index > current_num_row:
            self.anim_index = 0
