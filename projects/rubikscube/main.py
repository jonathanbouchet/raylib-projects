import math
import pyray as pr
import raylib as rl

width, height = 600, 600

pr.init_window(width, height, "rubikscube")
pr.set_target_fps(60)

camera = pr.Camera3D(
    pr.Vector3(6, 4, 6),
    pr.Vector3(0, 0, 0),
    pr.Vector3(0, 1, 0),
    90,
    rl.CAMERA_PERSPECTIVE,
)

# Generate a cube model
mesh = pr.gen_mesh_cube(4.0, 4.0, 4.0)
model = pr.load_model_from_mesh(mesh)

pitch: float = 0.0  # Rotation around X axis
yaw: float = 0.0  # Rotation around Y axis
roll: float = 0.0  # Rotation around Z axis

slider_value_pitch = pr.ffi.new("float *", 0)  # Initial value
slider_value_yaw = pr.ffi.new("float *", 0)  # Initial value
slider_value_roll = pr.ffi.new("float *", 0)  # Initial value

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    pitch += slider_value_pitch[0] * dt
    yaw += slider_value_yaw[0] * dt
    roll += slider_value_roll[0] * dt

    # COMBINE THE THREE ANGLES INTO ONE QUATERNION
    # Note: Raylib expects angles in radians for quaternion conversions
    combined_quaternion = pr.quaternion_from_euler(pitch, yaw, roll)

    # CONVERT THE QUATERNION INTO A 4x4 ROTATION MATRIX
    rotation_matrix = pr.quaternion_to_matrix(combined_quaternion)

    # APPLY THE MATRIX TO THE MODEL
    # This overrides the model's internal orientation instantly
    model.transform = rotation_matrix

    # UI
    pr.gui_group_box(pr.Rectangle(10, 10, 100, 60), "ROTATION")
    sliderOption_pitch = pr.gui_slider(
        pr.Rectangle(30, 20, 60, 10),
        "-1",
        "1",
        slider_value_pitch,
        -1 * math.pi,
        math.pi,
    )
    sliderOption_yaw = pr.gui_slider(
        pr.Rectangle(30, 35, 60, 10), "-1", "1", slider_value_yaw, -1 * math.pi, math.pi
    )
    sliderOption_roll = pr.gui_slider(
        pr.Rectangle(30, 50, 60, 10),
        "-1",
        "1",
        slider_value_roll,
        -1 * math.pi,
        math.pi,
    )

    pr.begin_drawing()
    pr.clear_background(pr.DARKGRAY)
    pr.begin_mode_3d(camera)

    # Draw the rotated model at the center (0, 0, 0)
    # The scale vector is set to (1, 1, 1) because the size is defined in the mesh
    pr.draw_model(model, pr.Vector3(0.0, 0.0, 0.0), 1.0, pr.YELLOW)

    # Draw wireframe lines over the cube so you can clearly see the 3D rotation
    pr.draw_model_wires(model, pr.Vector3(0.0, 0.0, 0.0), 1.0, pr.BLACK)

    pr.draw_grid(10, 2)

    pr.end_mode_3d()
    pr.draw_fps(0, 580)
    pr.end_drawing()

pr.close_window()
