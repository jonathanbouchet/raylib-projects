import pyray as pr
from simple_board import BaseBoard
import settings as settings

pr.init_window(settings.window_width, settings.window_height, "grid")
pr.set_target_fps(60)

board = BaseBoard(
    num_rows=settings.num_cells,
    num_cols=settings.num_cells,
    cell_size=int(settings.window_width / settings.num_cells),
)
board.print()  # debug
is_mouse_pressed: bool = False

while not pr.window_should_close():
    # logic
    if pr.is_mouse_button_pressed(0):
        cell_ids = board.get_cell_clicked(pos=pr.get_mouse_position())
        is_mouse_pressed = True

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    board.draw()
    if is_mouse_pressed:
        pr.draw_text(f"cell X: {cell_ids[0]}", 0, 20, 20, pr.DARKGREEN)
        pr.draw_text(f"cell Y: {cell_ids[1]}", 0, 40, 20, pr.DARKGREEN)
    pr.draw_fps(0, 0)
    pr.end_drawing()

pr.close_window()
