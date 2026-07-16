import asyncio
from pathlib import Path
import pyray as pr

width, height = 640, 640
# width, height = 960, 960

THIS_DIR = (Path(__file__).parent / "assets").resolve()


class Tile:
    def __init__(self, position: pr.Vector2, texture_path) -> None:
        self.position = position
        self.texture: pr.Texture = pr.load_texture(texture_path)
        self.width = self.texture.width
        self.height = self.texture.height
        self.rect = pr.Rectangle(0, 0, self.width, self.height)

    def draw(self) -> None:
        pr.draw_texture_rec(self.texture, self.rect, self.position, pr.WHITE)

    def unload_font(self) -> None:
        pr.unload_texture(self.texture)


async def main():
    pr.init_window(width, height, "texture")
    pr.set_target_fps(60)

    # load font
    font = pr.load_font(f"{THIS_DIR}/Thin Sans.ttf")

    grass_tile_32x32 = Tile(
        position=pr.Vector2(50, 200), texture_path=f"{THIS_DIR}/grass.png"
    )
    grass_tile_64x64 = Tile(
        position=pr.Vector2(50, 400), texture_path=f"{THIS_DIR}/grass_64x64.png"
    )

    rock_tile_32x32 = Tile(
        position=pr.Vector2(200, 200), texture_path=f"{THIS_DIR}/rock.png"
    )
    rock_tile_64x64 = Tile(
        position=pr.Vector2(200, 400), texture_path=f"{THIS_DIR}/rock_64x64.png"
    )

    player_tile_32x32 = Tile(
        position=pr.Vector2(350, 200), texture_path=f"{THIS_DIR}/player.png"
    )
    player_tile_64x64 = Tile(
        position=pr.Vector2(350, 400), texture_path=f"{THIS_DIR}/player_64x64.png"
    )

    button_tile_32x32 = Tile(
        position=pr.Vector2(500, 200), texture_path=f"{THIS_DIR}/play_button.png"
    )
    button_tile_64x64 = Tile(
        position=pr.Vector2(500, 400), texture_path=f"{THIS_DIR}/play_button_64x64.png"
    )

    textures = [
        grass_tile_32x32,
        grass_tile_64x64,
        rock_tile_32x32,
        rock_tile_64x64,
        player_tile_32x32,
        player_tile_64x64,
        button_tile_32x32,
        button_tile_64x64,
    ]

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        # grass
        grass_tile_32x32.draw()
        pr.draw_text_ex(font, "32x32", pr.Vector2(50, 170), 20, 2, pr.GRAY)
        grass_tile_64x64.draw()
        pr.draw_text_ex(font, "64x64", pr.Vector2(50, 370), 20, 2, pr.GRAY)

        # rock
        rock_tile_32x32.draw()
        pr.draw_text_ex(font, "32x32", pr.Vector2(200, 170), 20, 2, pr.GRAY)
        rock_tile_64x64.draw()
        pr.draw_text_ex(font, "64x64", pr.Vector2(200, 370), 20, 2, pr.GRAY)

        # player
        player_tile_32x32.draw()
        pr.draw_text_ex(font, "32x32", pr.Vector2(350, 170), 20, 2, pr.GRAY)
        player_tile_64x64.draw()
        pr.draw_text_ex(font, "64x64", pr.Vector2(350, 370), 20, 2, pr.GRAY)

        # play button
        button_tile_32x32.draw()
        pr.draw_text_ex(font, "32x32", pr.Vector2(500, 170), 20, 2, pr.GRAY)
        button_tile_64x64.draw()
        pr.draw_text_ex(font, "64x64", pr.Vector2(500, 370), 20, 2, pr.GRAY)

        pr.end_drawing()
        await asyncio.sleep(0)

    pr.unload_font(font)
    _ = [texture.unload_font() for texture in textures]
    pr.close_window()


if __name__ == "__main__":
    asyncio.run(main())
