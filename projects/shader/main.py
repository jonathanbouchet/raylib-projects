from pathlib import Path
import pyray as pr
import raylib as rl

width, height = 600, 600

THIS_DIR = (Path(__file__).parent).resolve()

pr.init_window(width, height, "app")
pr.set_target_fps(60)

background_texture = pr.load_texture(f"{THIS_DIR}/background.png")
player_texture = pr.load_texture(f"{THIS_DIR}/0.png")
player_speed = 10

player_pos = pr.Vector2(
    int(width / 2 - player_texture.width / 2),
    int(height / 2 - player_texture.height / 2),
)

shader = pr.load_shader(
    pr.ffi.NULL, f"{THIS_DIR}/test.fs"
)  # vertex shader can be default raylib one
loc_shader = pr.get_shader_location(shader, "test")

while not pr.window_should_close():
    # logic
    player_pos.x += int(pr.is_key_down(rl.KEY_RIGHT) * player_speed) - int(
        pr.is_key_down(rl.KEY_LEFT) * player_speed
    )
    player_pos.y += int(pr.is_key_down(rl.KEY_DOWN) * player_speed) - int(
        pr.is_key_down(rl.KEY_UP) * player_speed
    )

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    pr.draw_texture_ex(background_texture, pr.Vector2(), 0, 1.0, pr.WHITE)

    pr.begin_shader_mode(shader)
    pr.draw_texture_ex(player_texture, player_pos, 0, 1.0, pr.WHITE)
    pr.end_shader_mode()

    pr.end_drawing()

pr.close_window()
