from pathlib import Path
import pyray as pr
from texture_loader import MapLoader

width, height = 320, 160
TILE_WIDTH = 32
TILE_HEIGHT = 32

THIS_DIR = (Path(__file__).parent / "assets").resolve()

texture_path: str = str(THIS_DIR / "terrain_32x32.png")
map_path = str(THIS_DIR / "map_10_5.tmj")

pr.init_window(width, height, "texture")
pr.set_target_fps(60)

map = MapLoader(
    window_width=width,
    window_height=height,
    tile_size=TILE_WIDTH,
    texture_path=texture_path,
    map_path=map_path,
)
map.make_map()

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.DARKGRAY)
    map.draw()
    map.draw_grid()
    pr.draw_fps(0, 0)

    pr.end_drawing()
pr.close_window()
