import raylib as rl
import pyray as pr


window_width, window_height = 600, 400
brick_height: int = 30
bricks_num: int = 5
bricks_rows: int = 4
brick_color: pr.Color = pr.DARKGREEN
brick_disabled: bool = False

player_width: int = 100
player_height: int = 20
player_speed: int = 400
player_roundness: int = 0.75
player_color: pr.Color = rl.DARKGRAY
player_disabled: bool = False

ball_speed: int = 500
ball_color: pr.Color = rl.DARKBLUE
ball_width: int = 10
ball_height: int = 10
ball_disabled: bool = False
