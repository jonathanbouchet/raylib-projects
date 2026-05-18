import random as rn
import pyray as pr
import raylib as rl
from utils import Player, Ball

width, height = 600, 400

pr.init_window(width, height, "breakout")
pr.set_target_fps(60)

player_width: int = 100
player_height: int = 20
player_speed: int = 400
player_roundness: int = 0.75
player_color: pr.Color = rl.DARKGRAY

player = Player(
    position=pr.Vector2(width / 2 - player_width / 2, height - 40),
    direction=pr.Vector2(0, 0),
    width=player_width,
    height=player_height,
    speed=player_speed,
    roundness=player_roundness,
    color=player_color,
)

ball_speed: int = 500
ball_color: pr.Color = rl.DARKBLUE

ball = Ball(
    position=pr.Vector2(width / 2, height / 2),
    direction=pr.Vector2(rn.uniform(-0.75, 0.75), rn.uniform(-1, 1)),
    width=10,
    height=10,
    speed=ball_speed,
    color=ball_color,
)

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    player.update(dt=dt)
    ball.update(dt=dt)

    # rendering
    pr.begin_drawing()
    pr.clear_background(rl.BLACK)
    player.draw()
    ball.draw()
    pr.draw_fps(0, 380)
    pr.end_drawing()

pr.close_window()
