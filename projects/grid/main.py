import pyray as pr
from Grid import Grid

window_width, window_height = 600, 600

pr.init_window(window_width, window_height, "grid")
pr.set_target_fps(60)

grid = Grid(num_rows=10, num_cols=10, cell_size=60)
grid.print()  # debug
is_mouse_pressed: bool = False

while not pr.window_should_close():
    # logic
    if pr.is_mouse_button_pressed(0):
        cell_ids = grid.get_cell_clicked(pos=pr.get_mouse_position())
        is_mouse_pressed = True

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    grid.draw()
    if is_mouse_pressed:
        pr.draw_text(f"cell X: {cell_ids[0]}", 0, 20, 20, pr.DARKGREEN)
        pr.draw_text(f"cell Y: {cell_ids[1]}", 0, 40, 20, pr.DARKGREEN)
    pr.draw_fps(0, 0)
    pr.end_drawing()

pr.close_window()
