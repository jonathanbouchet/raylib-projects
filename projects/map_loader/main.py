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

# add collision layer tiles
walls = map.get_collision_layer()
print(f"{walls=}")

# add dummy player to showcase
y_coord: float = 0
player = pr.Rectangle(100, y_coord, 20,20, pr.BLACK)

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    # collision:
    for wall in walls:
        if pr.check_collision_recs(player, wall):
            player.y = wall.y - 20 # 20 is the height of the player
    player.y += 20*dt

    pr.begin_drawing()
    pr.clear_background(pr.DARKGRAY)
    map.draw()
    map.draw_grid()
    map.draw_collision_layer()
    pr.draw_rectangle_rec(player, pr.BLACK)
    pr.draw_fps(0, 0)

    pr.end_drawing()
pr.close_window()
