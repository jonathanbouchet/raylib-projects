import pyray as pr
import raylib as rl
import os


width, height = 600, 600
icon_width, icon_height = 20, 20

def load_model(choice: int) -> tuple[bool, pr.Model]:
    if choice == 1:
        model_pathname = os.getcwd() + "/projects/load_render/models/cube.glb"
        model = pr.load_model(model_pathname)
        is_model_selected = True
    elif choice == 2:
        model_pathname = os.getcwd() + "/projects/load_render/models/sphere.glb"
        model = pr.load_model(model_pathname)
        is_model_selected = True
    elif choice == 3:
        model_pathname = os.getcwd() + "/projects/load_render/models/torus.glb"
        model = pr.load_model(model_pathname)
        is_model_selected = True
    elif choice == 4:
        model = os.getcwd() + "/projects/load_render/models/cube_colored.glb"
        is_model_selected = True
    else:
        is_model_selected = False
        model = None
    return is_model_selected, model


pr.init_window(width, height, "render")
pr.set_target_fps(60)

# camera
camera = pr.Camera3D()
camera.position = pr.Vector3(0.0, 5.0, 10.0)
camera.target = pr.Vector3(0.0, 0.0, 0.0)
camera.up = pr.Vector3(0.0, 1.0, 0.0)
camera.fovy = 45.0
camera.projection = rl.CAMERA_PERSPECTIVE


slider_value = pr.ffi.new("float *", 1.0)  # Initial value
camera_speed = 2
dl: float = 0

dropdown_edit_mode = False
active_index_ptr = pr.ffi.new("int *", 0)
is_model_selected = False

# transform
rotation = 0

model_pathname: str = ""

while not pr.window_should_close():
    # update
    if pr.gui_button(
        pr.Rectangle(0, 20, icon_width, icon_height), "#118#ICON_ARROW_LEFT_FILL"
    ):
        camera.position.x -= camera_speed
    if pr.gui_button(
        pr.Rectangle(40, 20, icon_width, icon_height), "#119#ICON_ARROW_RIGHT_FILL"
    ):
        camera.position.x += camera_speed
    if pr.gui_button(
        pr.Rectangle(20, 0, icon_width, icon_height), "#121#ICON_ARROW_UP_FILL"
    ):
        camera.position.z -= camera_speed
    if pr.gui_button(
        pr.Rectangle(20, 40, icon_width, icon_height), "#120#ICON_ARROW_DOWN_FILL"
    ):
        camera.position.z += camera_speed
    if pr.gui_button(
        pr.Rectangle(20, 20, icon_width, icon_height), "#169#ICON_CAMERA_CURSOR"
    ):
        camera.target = pr.Vector3(0.0, 0.0, 0.0)

    if pr.gui_dropdown_box(
        pr.Rectangle(80, 20, 120, 20),
        "CHOOSE A MODEL;CUBE;SPHERE;TORE;CUBE COLORED",
        active_index_ptr,
        dropdown_edit_mode,
    ):
        dropdown_edit_mode = not dropdown_edit_mode

    selected_value = active_index_ptr[0]

    sliderOption = pr.gui_slider(
        pr.Rectangle(80, 0, 120, 20), "0", "2.0", slider_value, 0.0, 2.0
    )

    is_model_selected, model = load_model(selected_value)

    dt = pr.get_frame_time()
    dl += dt * slider_value[0]  # take into account the factor from the slider

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.Color(43, 46, 44, 255))
    pr.begin_mode_3d(camera)

    if is_model_selected:
        pr.draw_model_ex(
            model,
            pr.Vector3(0, 0, 0),
            pr.Vector3(0, 1, 0),
            rotation,
            pr.Vector3(1, 1, 1),
            rl.WHITE,
        )

    pr.draw_grid(10, 2.0)
    pr.end_mode_3d()

    pr.draw_fps(0, 575)
    pr.end_drawing()

pr.close_window()
