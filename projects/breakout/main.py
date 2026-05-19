import random
import math
import pyray as pr
import raylib as rl
from utils import Player, Ball, Bricks
import settings as setting


def generate_random_unit_vector():
    # Pick a random angle between 0 and 2*pi
    theta = random.uniform(0, 2 * math.pi)

    # Calculate x and y using trigonometry
    x = math.cos(theta)
    y = math.sin(theta)

    return [x, y]


pr.init_window(setting.window_width, setting.window_height, "breakout")
pr.set_target_fps(60)

bricks = Bricks(
    brick_height=setting.brick_height,
    num_row=setting.bricks_rows,
    num_brick=setting.bricks_num,
)
bricks.make_bricks()

player = Player(
    position=pr.Vector2(
        setting.window_width / 2 - setting.player_width / 2, setting.window_height - 40
    ),
    direction=pr.Vector2(0, 0),
    width=setting.player_width,
    height=setting.player_height,
    speed=setting.player_speed,
    roundness=setting.player_roundness,
    color=setting.player_color,
    disabled=setting.player_disabled,
)

ball = Ball(
    position=pr.Vector2(setting.window_width / 2, setting.window_height / 2),
    direction=pr.Vector2(random.uniform(-0.75, 0.75), random.uniform(-1, 1)),
    # direction=pr.Vector2(ball_direction[0], ball_direction[1]),
    width=setting.ball_width,
    height=setting.ball_height,
    speed=setting.ball_speed,
    color=setting.ball_color,
    disabled=setting.ball_disabled,
)


while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    player.update(dt=dt)
    ball.update(dt=dt)
    bricks.update(dt, ball.position, ball.width)

    # rendering
    pr.begin_drawing()
    pr.clear_background(rl.BLACK)
    player.draw()
    ball.draw()
    bricks.draw()
    pr.draw_fps(0, 380)
    pr.end_drawing()

pr.close_window()
