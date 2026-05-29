import pyray as pr
from Grid import Grid

window_width, window_height = 600, 600

pr.init_window(window_width, window_height, "grid")
pr.set_target_fps(60)

grid = Grid(num_rows=10, num_cols=10, cell_size=60)
grid.print()  # debug

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    grid.draw()
    pr.draw_fps(0, 0)
    pr.end_drawing()

pr.close_window()
