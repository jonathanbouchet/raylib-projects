import pyray as pr
import raylib as rl
import requests

width, height = 300, 600

blue = pr.Color(149, 204, 186, 255)
pink = pr.Color(255, 222, 222, 255)
orange = pr.Color(242, 204, 132, 255)
light_orange = pr.Color(255, 240, 203, 255)
green = pr.Color(167, 186, 66, 255)

base_url: str = "http://0.0.0.0:8000"
headers = {"Content-Type": "application/json"}


# Initialize raylib window
pr.init_window(width, height, "TODO APP")
pr.set_target_fps(60)

# TextInputBox parameters
box_text = "ok"
box_title = "add a todo"
box_width, box_height = 200, 100

# Window position state
box_rec = pr.Rectangle(40, 400, box_width, box_height)
show_window = True

# Dragging state variables
is_dragging = False
mouse_offset_x = 0.0
mouse_offset_y = 0.0

# api calls variables
show_status: bool = False
show_todos = False
button_clicked: bool = False
text_buffer = pr.ffi.new("char[64]", b"")

while not pr.window_should_close():
    pr.draw_text("TODO INPUT \nPress A to show window", 10, 10, 20, green)

    # API STATUS
    if pr.gui_button(pr.Rectangle(40, 60, 100, 40), "get API status"):
        response_status = requests.get(url=base_url, headers=headers)
        print(response_status, response_status.content)
        if response_status.ok:
            show_status = True
            response_status_json = response_status.json()
    if show_status:
        pr.gui_text_box(
            pr.Rectangle(150, 60, 100, 40),
            f"{response_status_json['status']}",
            20,
            False,
        )

    # API GET TODOS
    if pr.gui_button(pr.Rectangle(40, 110, 100, 40), "get TODOS"):
        url_get: str = f"{base_url}/todos"
        response_get = requests.get(url=url_get, headers=headers)
        print(response_get, response_get.content)
        if response_get.ok:
            show_todos = True
            response_get_json = response_get.json()
    if show_todos:
        for cnt, todo in enumerate(response_get_json):
            pr.gui_text_box(
                pr.Rectangle(150, 110 + (cnt) * 40 + cnt * 5, 100, 40),
                f"{todo['title']}",
                20,
                False,
            )

    # 1. Update Logic
    mouse_pos = pr.get_mouse_position()

    # Define the draggable "Title Bar" area (top 24 pixels of the box)
    title_bar_rec = pr.Rectangle(box_rec.x, box_rec.y, box_rec.width, 24)

    if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
        if pr.check_collision_point_rec(mouse_pos, title_bar_rec):
            is_dragging = True
            # Calculate distance from mouse to top-left corner of the box
            mouse_offset_x = mouse_pos.x - box_rec.x
            mouse_offset_y = mouse_pos.y - box_rec.y

    if is_dragging:
        # Update box position based on mouse position and offset
        box_rec.x = mouse_pos.x - mouse_offset_x
        box_rec.y = mouse_pos.y - mouse_offset_y

        # Stop dragging when mouse button is released
        if pr.is_mouse_button_released(pr.MOUSE_BUTTON_LEFT):
            is_dragging = False
            # check if TextInputBox is inside right part of the window
            if (box_rec.x + box_rec.width) > width:
                box_rec.x = 40
            elif box_rec.x < 0:
                box_rec.x = 40
            elif (box_rec.y + box_rec.height) > height:
                box_rec.y = height - box_rec.height
            elif box_rec.y < 0:
                box_rec.y = 0

    # 2. Draw Logic
    pr.begin_drawing()
    pr.clear_background(orange)

    if show_window:
        result = pr.gui_text_input_box(
            box_rec, box_title, "", "ok", text_buffer, 255, None
        )
        # Handle dialog buttons if needed
        if result == 1:
            # API ADD A TO-DO
            url_post = f"{base_url}/todos"
            data_to_send = pr.ffi.string(text_buffer).decode("utf-8")
            json_data = {"title": data_to_send}
            res = requests.post(url=url_post, headers=headers, json=json_data)
        elif result == 0: # this checks when the cross top rigth is clicked to close the window
            show_window = False

    if pr.is_key_down(rl.KEY_A):
        show_window = True

    pr.draw_fps(0, 580)
    pr.end_drawing()

pr.close_window()
