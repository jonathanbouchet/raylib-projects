import pyray as pr
from sprites import Player, Enemy, WayPoints

window_width, window_height = 800, 800

pr.init_window(window_width, window_height, "test")
pr.set_target_fps(60)

player_width: int = 20
player_height: int = 20
player_color = pr.GREEN
player_direction: pr.Vector2 = pr.Vector2(0, 0)
player_speed: int = 300
player_area: int = 200
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
enemy_color = pr.YELLOW
enemy_color_detected = pr.RED
enemy_direction: pr.Vector2 = pr.Vector2(0, 0)
enemy_speed: int = 300
enemy_area: int = 100
enemy_debug = True
enemy = Enemy(
    position=pr.Vector2(20, 20),
    direction=enemy_direction,
    speed=enemy_speed,
    detection_area=enemy_area,
    width=enemy_width,
    height=enemy_height,
    color=enemy_color,
    debug=enemy_debug,
    color_detected=enemy_color_detected,
)

markers_positions = [
    pr.Vector2(20, window_height / 2),
    pr.Vector2(window_width / 2, 20),
    pr.Vector2(window_width - 20, window_height / 2),
    pr.Vector2(window_width / 2, window_height - 20),
]
markers = WayPoints(
    positions=markers_positions, color=pr.BLUE, detection_area=20, width=10, height=10
)
markers.make_points()

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    player.update(dt=dt)
    enemy.update(dt=dt, player=player, waypoints=markers)

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    player.draw()
    enemy.draw()
    markers.draw_points()
    pr.draw_fps(0, 0)
    pr.end_drawing()

pr.close_window()
