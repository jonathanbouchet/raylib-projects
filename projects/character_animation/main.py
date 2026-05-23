import pyray as pr
from character import Player
from utils import load_textures

width, height = 1280, 720

pr.init_window(width, height, "anim")
pr.set_target_fps(60)

# player = Player(
#     position=pr.Vector2(width / 2, height / 2), direction=pr.Vector2(0, 0), speed=200
# )
player_textures = load_textures()
player = Player(
    position=pr.Vector2(width / 2, height / 2),
    direction=pr.Vector2(0, 0),
    speed=200,
    textures=player_textures,
)

while not pr.window_should_close():
    # input
    # logic
    dt = pr.get_frame_time()
    player.update(dt=dt)

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    player.draw(dt=dt)

    pr.draw_fps(0, 0)
    pr.draw_text(f"PLAYER STATE: {player.get_state()}", 0, 20, 20, pr.GREEN)
    pr.end_drawing()
pr.close_window()
