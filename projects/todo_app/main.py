import pyray as pr
import raylib as rl

width, height = 600, 600

blue = pr.Color(149, 204, 186, 255)
pink = pr.Color(255, 222, 222, 255)
orange = pr.Color(242, 204, 132, 255)
light_orange = pr.Color(255, 240, 203, 255)
green = pr.Color(167, 186, 66, 255)


# Initialize raylib window
pr.init_window(width, height, "raygui TextInputBox")
pr.set_target_fps(60)
# Syntax: GuiSetStyle(control, property, value)
# pr.gui_set_style(pr.TEXTBOX, rl.TEXT_COLOR_NORMAL, pr.color_to_int(pr.PINK))

# TextInputBox parameters
box_text = "Edit me!"
box_title = "Add todo"
box_width, box_height = 200, 140

# pr.gui_set_style()

# Window position state (Centered initially)
box_rec = pr.Rectangle(0, 100, box_width, box_height)
show_window = True

# Dragging state variables
is_dragging = False
mouse_offset_x = 0.0
mouse_offset_y = 0.0

while not pr.window_should_close():
    # 0. background
    # pr.draw_line(int(width/2), 0, int(width/2), pr.get_screen_height(), blue)
    # pr.draw_rectangle(int(width/2), 0, int(width/2) + 5, pr.get_screen_height(), blue)
    pr.draw_rectangle(
        int(width / 2) + 5, 0, pr.get_screen_width(), pr.get_screen_height(), orange
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
            if (box_rec.x + box_rec.width) > width / 2:
                box_rec.x = width / 2 - box_rec.width

    # 2. Draw Logic
    pr.begin_drawing()
    pr.clear_background(light_orange)

    pr.draw_text("TO DO app \nPress A to show window", 10, 10, 20, green)

    # Draw the GUI text input box using our dynamic box_rec
    # Note: raygui buttons are 0 (normal), 1 (pressed), -1 (hidden/canceled)
    if show_window:
        result = pr.gui_text_input_box(
            box_rec, box_title, "Type title here:", "Ok", box_text, 255, None
        )

        # Handle dialog buttons if needed
        if result == 1:
            print(f"User clicked OK. Text: {box_text}")
        elif result == 0:
            print("User clicked Cancel or Closed the box.")
            show_window = False
    if pr.is_key_down(rl.KEY_A):
        show_window = True
    pr.draw_fps(0, 580)
    pr.end_drawing()

pr.close_window()
