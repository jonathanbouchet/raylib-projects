from pathlib import Path
import pyray as pr

THIS_DIR = (Path(__file__).parent).resolve()

# 1. Initialization
pr.init_window(800, 450, "pyray Glow Effect")
target = pr.load_render_texture(pr.get_screen_width(), pr.get_screen_height())
shader = pr.load_shader(
    pr.ffi.NULL, f"{THIS_DIR}/bloom.fs"
)  # Point to your downloaded shader file

pr.set_target_fps(60)

# 2. Main Game Loop
while not pr.window_should_close():
    # --- RENDER SCENE TO TEXTURE ---

    pr.begin_texture_mode(target)
    pr.clear_background(pr.BLACK)

    # Draw glowing objects here...
    pr.draw_circle(400, 225, 30, pr.Color(255, 0, 255, 255))
    pr.end_texture_mode()

    # --- DRAW AND APPLY GLOW ---
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)

    pr.begin_shader_mode(shader)
    # Draw the rendered texture with the bloom shader applied
    pr.draw_texture_rec(
        target.texture,
        pr.Rectangle(0, 0, pr.get_screen_width(), -pr.get_screen_height()),
        pr.Vector2(0, 0),
        pr.WHITE,
    )
    pr.end_shader_mode()

    # Draw non-glowing objects here...
    pr.draw_rectangle(400 - 15, 100, 30, 30, pr.BLUE)

    pr.end_drawing()

pr.unload_render_texture(target)
pr.unload_shader(shader)
pr.close_window()
