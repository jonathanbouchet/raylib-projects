from pathlib import Path
import pyray as pr

"""
refactoring into a class
Class Texture:
    # does not need moving or update; fixed texture
    draw

Class Texture2(Texture)
    # derive from Texture ; need update and moving texture
    update
    move

Class BackGround()
    # class to hold all background textures of the game
    textures: list[Texture]    
"""


class BaseTexture:
    def __init__(self, position: pr.Vector2, texture_path: str) -> None:
        self.position = position
        self.texture = pr.load_texture(texture_path)

    def draw(self) -> None:
        pr.draw_texture_v(self.texture, self.position, pr.WHITE)

    def update(self, dt: float):
        pass


class Texture(BaseTexture):
    def __init__(
        self, position: pr.Vector2, texture_path: str, speed: float, offset: int
    ) -> None:
        super().__init__(position=position, texture_path=texture_path)
        self.speed = speed
        self.offset = offset

    def update(self, dt: float):
        self.position.x -= dt * self.speed
        if (self.position.x + self.texture.width) < 0:
            self.position.x = self.offset * self.texture.width


class Background:
    def __init__(self, textures: list[Texture]) -> None:
        self.textures = textures

    def update(self, dt) -> None:
        _ = [texture.update(dt) for texture in self.textures]

    def draw(self, dt) -> None:
        _ = [texture.draw() for texture in self.textures]


width, height = 700, 432

THIS_DIR = (Path(__file__).parent / "assets").resolve()

pr.init_window(width, height, "app")
pr.set_target_fps(60)

fixed_background = BaseTexture(
    position=pr.Vector2(), texture_path=f"{THIS_DIR}/plx-1.png"
)
foreground_1 = Texture(
    position=pr.Vector2(0, height - 50),
    texture_path=f"{THIS_DIR}/ground.png",
    speed=100,
    offset=3,
)
foreground_2 = Texture(
    position=pr.Vector2(foreground_1.texture.width, height - 50),
    texture_path=f"{THIS_DIR}/ground.png",
    speed=100,
    offset=3,
)
foreground_3 = Texture(
    position=pr.Vector2(2 * foreground_2.texture.width, height - 50),
    texture_path=f"{THIS_DIR}/ground.png",
    speed=100,
    offset=3,
)
foreground_4 = Texture(
    position=pr.Vector2(3 * foreground_3.texture.width, height - 50),
    texture_path=f"{THIS_DIR}/ground.png",
    speed=100,
    offset=3,
)

background_1 = Texture(
    position=pr.Vector2(0, 0), texture_path=f"{THIS_DIR}/plx-5.png", speed=50, offset=1
)
background_2 = Texture(
    position=pr.Vector2(background_1.texture.width, 0),
    texture_path=f"{THIS_DIR}/plx-5.png",
    speed=50,
    offset=1,
)

background_3 = Texture(
    position=pr.Vector2(0, 0), texture_path=f"{THIS_DIR}/plx-4.png", speed=20, offset=1
)
background_4 = Texture(
    position=pr.Vector2(background_3.texture.width, 0),
    texture_path=f"{THIS_DIR}/plx-4.png",
    speed=50,
    offset=1,
)

# order matters !
background = Background(
    textures=[
        fixed_background,
        background_3,
        background_4,
        background_1,
        background_2,
        foreground_1,
        foreground_2,
        foreground_3,
        foreground_4,
    ]
)

while not pr.window_should_close():
    dt = pr.get_frame_time()
    background.update(dt=dt)
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    background.draw(dt)
    pr.end_drawing()

pr.close_window()
