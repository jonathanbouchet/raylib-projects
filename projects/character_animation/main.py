import pyray as pr
from character import Sprite, AnimatedSprite
from utils import load_textures

width, height = 1280, 720

pr.init_window(width, height, "anim")
pr.set_target_fps(60)


player = Sprite(
    position=pr.Vector2(width / 2, height / 2),
    direction=pr.Vector2(0, 0),
    speed=300,
    width=40,
    height=80,
    color=pr.YELLOW,
)
# player_textures = load_textures()
# player = AnimatedSprite(
#     position=pr.Vector2(width / 2, height / 2),
#     direction=pr.Vector2(0, 0),
#     speed=200,
#     textures=player_textures,
# )

# add floor
floor = pr.Rectangle(0, height - 140, width, 40)

while not pr.window_should_close():
    # input
    # logic
    dt = pr.get_frame_time()
    player.update(dt=dt, other=floor)

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    player.draw(dt=dt)

    # draw floor
    pr.draw_rectangle_rec(floor, pr.DARKGRAY)

    pr.draw_fps(0, 0)
    pr.draw_text(
        f"{str(player.get_state()).split('.')[1]}",
        int(player.get_position().x),
        int(player.get_position().y) - 20,
        20,
        pr.GREEN,
    )
    pr.end_drawing()
pr.close_window()
