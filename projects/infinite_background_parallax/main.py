from pathlib import Path
import pyray as pr

width, height = 700, 432

THIS_DIR = (Path(__file__).parent / "assets").resolve()

pr.init_window(width, height, "app")
pr.set_target_fps(60)
foreground_1 = pr.load_texture(f"{THIS_DIR}/ground.png")
foreground_2 = pr.load_texture(f"{THIS_DIR}/ground.png")
foreground_3 = pr.load_texture(f"{THIS_DIR}/ground.png")
foreground_4 = pr.load_texture(f"{THIS_DIR}/ground.png")
foreground_pos_1 = pr.Vector2(0, height - 50)
foreground_pos_2 = pr.Vector2(foreground_1.width, height - 50)
foreground_pos_3 = pr.Vector2(2 * foreground_2.width, height - 50)
foreground_pos_4 = pr.Vector2(3 * foreground_3.width, height - 50)

background_11 = pr.load_texture(f"{THIS_DIR}/plx-5.png")
background_12 = pr.load_texture(f"{THIS_DIR}/plx-5.png")
background_pos_11 = pr.Vector2(0, 0)
background_pos_12 = pr.Vector2(background_11.width, 0)

background_21 = pr.load_texture(f"{THIS_DIR}/plx-4.png")
background_22 = pr.load_texture(f"{THIS_DIR}/plx-4.png")
background_pos_21 = pr.Vector2(0, 0)
background_pos_22 = pr.Vector2(background_21.width, 0)


while not pr.window_should_close():
    dt = pr.get_frame_time()
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    foreground_pos_1.x -= dt * 100
    foreground_pos_2.x -= dt * 100
    foreground_pos_3.x -= dt * 100
    foreground_pos_4.x -= dt * 100

    background_pos_11.x -= dt * 50
    background_pos_12.x -= dt * 50

    background_pos_21.x -= dt * 20
    background_pos_22.x -= dt * 20

    pr.draw_texture_v(background_21, background_pos_21, pr.WHITE)
    pr.draw_texture_v(background_22, background_pos_22, pr.WHITE)

    pr.draw_texture_v(background_11, background_pos_11, pr.WHITE)
    pr.draw_texture_v(background_12, background_pos_12, pr.WHITE)

    pr.draw_texture_v(foreground_1, foreground_pos_1, pr.WHITE)
    pr.draw_texture_v(foreground_2, foreground_pos_2, pr.WHITE)
    pr.draw_texture_v(foreground_3, foreground_pos_3, pr.WHITE)
    pr.draw_texture_v(foreground_4, foreground_pos_4, pr.WHITE)

    if (foreground_pos_1.x + foreground_1.width) < 0:
        foreground_pos_1.x = 3 * foreground_1.width
    if (foreground_pos_2.x + foreground_2.width) < 0:
        foreground_pos_2.x = 3 * foreground_2.width
    if (foreground_pos_3.x + foreground_3.width) < 0:
        foreground_pos_3.x = 3 * foreground_3.width
    if (foreground_pos_4.x + foreground_4.width) < 0:
        foreground_pos_4.x = 3 * foreground_4.width

    if (background_pos_21.x + background_21.width) < 0:
        background_pos_21.x = background_21.width
    if (background_pos_22.x + background_22.width) < 0:
        background_pos_22.x = background_22.width

    if (background_pos_11.x + background_11.width) < 0:
        background_pos_11.x = background_11.width
    if (background_pos_12.x + background_12.width) < 0:
        background_pos_12.x = background_12.width

    pr.end_drawing()

pr.close_window()
