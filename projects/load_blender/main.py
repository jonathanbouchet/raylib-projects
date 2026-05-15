from pathlib import Path
import pyray as pr
import raylib as rl
from model_loader import Model

THIS_DIR = (Path(__file__).parent / "models").resolve()
print(f"{THIS_DIR=}")

width, height = 600, 600
icon_width, icon_height = 20, 20


def get_input(camera: pr.Camera3D) -> None:
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


pr.init_window(width, height, "render")
pr.set_target_fps(60)

# camera
camera = pr.Camera3D()
camera.position = pr.Vector3(0.0, 5.0, 10.0)
camera.target = pr.Vector3(0.0, 0.0, 0.0)
camera.up = pr.Vector3(0.0, 1.0, 0.0)
camera.fovy = 45.0
camera.projection = rl.CAMERA_PERSPECTIVE
camera_speed = 2

# model
model = Model(
    position=pr.Vector3(0, 0, 0), rotation_axis=pr.Vector3(0, 1, 0), rotation=0
)

# UI
slider_value = pr.ffi.new("float *", 0.0)  # Initial value
dropdown_edit_mode = False
active_index_ptr = pr.ffi.new("int *", 0)

# transform
dl: float = 0
selected_value: int = -1

while not pr.window_should_close():
    # update
    get_input(camera=camera)

    if pr.gui_dropdown_box(
        pr.Rectangle(80, 20, 120, 20),
        "CHOOSE A MODEL;CUBE;SPHERE;TORE;CUBE COLORED",
        active_index_ptr,
        dropdown_edit_mode,
    ):
        dropdown_edit_mode = not dropdown_edit_mode
        selected_value = active_index_ptr[0]
        model.load(choice=selected_value)
        print(
            f"{model.is_selected}, {model.position.x}, {model.position.y}, {model.position.z}, {model.rotation}"
        )
        print(f"{selected_value=}")

    sliderOption = pr.gui_slider(
        pr.Rectangle(80, 0, 120, 20), "-1", "1", slider_value, -1.0, 1.0
    )

    dt = pr.get_frame_time()
    dl += 200 * dt * slider_value[0]  # take into account the factor from the slider

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.Color(43, 46, 44, 255))
    pr.begin_mode_3d(camera)

    if model.is_selected:
        pr.draw_model_ex(
            model.blender_model,
            model.position,
            model.rotation_axis,
            dl, # updated rotation by the slider
            pr.Vector3(1, 1, 1),
            rl.WHITE,
        )

    pr.draw_grid(10, 2.0)
    pr.end_mode_3d()

    pr.draw_fps(0, 575)
    pr.end_drawing()

pr.close_window()
