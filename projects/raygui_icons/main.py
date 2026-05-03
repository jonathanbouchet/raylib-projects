import os
import pyray as pr
import json

width, height = 200, 600
icon_width, icon_height = 20, 20


def get_icon_name(pos: int, data: dict[str:int]) -> str:
    """return the name of the icon based on its index
    """
    for k, v in data.items():
        if v == pos:
            return k


pr.init_window(width, height, "test UI buttons")
pr.set_target_fps(60)
icon_name: str = os.getcwd() + "/projects/raygui_icons/assets/icon.json"
show_message_box: bool = False
has_been_clicked = False
num_icon = 200
max_icon_per_row = 10

with open(icon_name, "r") as f:
    data: dict[str, int] = json.load(f)

while not pr.window_should_close():
    # logic
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    current_row = 0
    current_col = 0
    click_icon_name: str
    click_icon_id: int
    for i in range(num_icon):
        current_row = int(i / max_icon_per_row)
        current_col = int(i % max_icon_per_row)
        icon_name = get_icon_name(pos=i, data=data)

        if pr.gui_button(
            pr.Rectangle(current_col * icon_width, current_row * icon_height, icon_width, icon_width),
            f"#{i}#{icon_name}",
        ):
            print(f"clicked {icon_name}")
            click_icon_id = i
            click_icon_name = icon_name
            show_message_box = True

        # Persist box while show_message is True
        if show_message_box:
            # gui_message_box returns 0 if closed
            result = pr.gui_message_box(
                pr.Rectangle(0, 400, 200, 120),
                f"#{click_icon_id}#{click_icon_name} clicked",
                "This message persists until\n closed.",
                "OK",
            )
            if result == 0:
                show_message_box = False

    pr.draw_fps(520, 0)
    pr.end_drawing()

pr.close_window()
