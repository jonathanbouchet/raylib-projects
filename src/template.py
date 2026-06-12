import pyray as pr

width, height = 600, 600

pr.init_window(width, height, "app")
pr.set_target_fps(60)

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.end_drawing()

pr.close_window()
