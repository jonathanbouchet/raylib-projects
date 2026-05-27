import pyray as pr
from sprites import Player, Enemy

window_width, window_height = 600, 600

pr.init_window(window_width, window_height, "test")
pr.set_target_fps(60)

player_width: int = 20
player_height: int = 20
player_color = pr.YELLOW
player_direction: pr.Vector2 = pr.Vector2(0, 0)
player_speed: int = 300
player_area: int = 150
player_debug: bool = True
player = Player(
    position=pr.Vector2(
        window_width / 2 - player_width / 2, window_height / 2 - player_height / 2
    ),
    direction=player_direction,
    speed=player_speed,
    width=player_width,
    height=player_height,
    color=player_color,
    detection_area=player_area,
    debug=player_debug,
)

enemy_width: int = 20
enemy_height: int = 20
enemy_color = pr.ORANGE
enemy_color_detected = pr.RED
enemy_direction: pr.Vector2 = pr.Vector2(0, 0)
enemy_speed: int = 300
enemy_debug = True
enemy = Enemy(
    position=pr.Vector2(20, 20),
    direction=enemy_direction,
    speed=enemy_speed,
    width=enemy_width,
    height=enemy_height,
    color=enemy_color,
    debug=enemy_debug,
    color_detected=enemy_color_detected
)


while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    player.update(dt=dt)
    enemy.update(dt=dt, player=player)

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    player.draw()
    enemy.draw()
    pr.draw_fps(0, 0)
    pr.end_drawing()

pr.close_window()
