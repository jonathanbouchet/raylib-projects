import pyray as pr
window_width, window_height = 600, 600

pr.init_window(window_width, window_height, "grid")
pr.set_target_fps(60)

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_fps(0,0)
    pr.end_drawing()

pr.close_window()