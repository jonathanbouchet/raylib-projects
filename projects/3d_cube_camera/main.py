import pyray as pr
import raylib as rl

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600

pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT,"cube")
pr.set_target_fps(60)

# define the 3D camera
camera = pr.Camera3D(pr.Vector3(6,4,6), pr.Vector3(0,0,0), pr.Vector3(0,1,0), 90, rl.CAMERA_PERSPECTIVE)

# Generate a cube model
mesh = pr.gen_mesh_cube(2.0, 2.0, 2.0)
model = pr.load_model_from_mesh(mesh)
rotation: float = 0

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    rotation += 100 * dt

    # draw
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.begin_mode_3d(camera)

    # pr.draw_cube_wires_v(position=pr.Vector3(-3,0,3), size=pr.Vector3(2,2,2), color=pr.BLUE) # not working
    pr.draw_cube_wires_v(pr.Vector3(-3,0,3), pr.Vector3(2,2,2), pr.BLUE)
    pr.draw_model_ex(model, pr.Vector3(0,0,0), pr.Vector3(0, 1, 0), rotation, pr.Vector3(1,1,1), pr.RED)

    pr.draw_grid(10,1)
    
    pr.end_mode_3d()
    pr.draw_fps(0,0)
    
    pr.end_drawing()
pr.close_window()