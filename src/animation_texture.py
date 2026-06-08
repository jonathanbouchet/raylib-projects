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
- instnce example: foam = TextureAnim(texture_path="./Foam.png", position=pr.Vector2(100, 200), tile_size=192, scale=1.0)
"""


class TextureAnim:
    def __init__(
        self,
        texture_path: str,
        position: pr.Vector2,
        tile_size: int,
        scale: float = 1.0,
    ) -> None:
        self.texture = pr.load_texture(texture_path)
        self.position: pr.Vector2 = position  # position of the texture
        self.tile_size: int = tile_size  # size in pizels of a single frame
        self.texture_width: int = (
            self.texture.width
        )  # width in pixels of the whole texture
        self.texture_heigth: int = (
            self.texture.height
        )  # height in pixels of the whole texture
        self.texture_len: int = int(
            self.texture.width / self.texture.height
        )  # number of animations in the texture
        self.anim_index: int = 0
        self.scale_factor: float = scale

    def draw(self, dt: float, fps: int):
        if fps == 0:
            return

        # first animation start at index=0
        tile_x = int(self.anim_index) * self.tile_size
        tile_y = 0

        # point to the ith animation frame in the texture
        source_rec = pr.Rectangle(tile_x, tile_y, self.tile_size, self.tile_size)

        dest_rec = pr.Rectangle(
            self.position.x,
            self.position.y,
            int(self.tile_size * self.scale_factor),
            int(self.tile_size * self.scale_factor),
        )
        pr.draw_texture_pro(
            self.texture,
            source_rec,
            dest_rec,
            pr.Vector2(dest_rec.width / 2, dest_rec.height / 2),
            0,
            pr.WHITE,
        )
        self.anim_index += self.texture_len / fps
        if self.anim_index > self.texture_len:
            self.anim_index = 0
