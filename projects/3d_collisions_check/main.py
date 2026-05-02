import pyray as pr
import raylib as rl



def get_bounding_pos(model, pos) -> pr.BoundingBox:
    bounding_box = pr.get_mesh_bounding_box(model.meshes[0])
    min_boundary = rl.Vector3Add(pos, bounding_box.min)
    max_boundary = rl.Vector3Add(pos, bounding_box.max)
    return pr.BoundingBox(min_boundary, max_boundary)


# settings
pr.init_window(800, 600, "3D basics")
pr.set_target_fps(60)
pr.set_exit_key(rl.KEY_ESCAPE)

# camera
camera = pr.Camera3D()
camera.position = pr.Vector3(0, 5.0, 10.0)
camera.target = pr.Vector3(0, 0, 0)
camera.up = pr.Vector3(0, 1, 0)
camera.fovy = 45
camera.projection = rl.CAMERA_PERSPECTIVE

# models
player_model = pr.load_model_from_mesh(pr.gen_mesh_cube(1, 1, 1))
player_position = pr.Vector3(0, 0, 0)
player_direction = pr.Vector3(0, 0, 0)
player_speed = 5

obs_model = pr.load_model_from_mesh(pr.gen_mesh_cube(3, 1, 3))
obs_position = pr.Vector3(3, 0, 0)

is_collision: bool = False
show_collision_box: int = 0


while not pr.window_should_close():
    # input
    player_direction.x = int(pr.is_key_down(rl.KEY_RIGHT)) - int(pr.is_key_down(rl.KEY_LEFT))
    player_direction.z = int(pr.is_key_down(rl.KEY_DOWN)) - int(pr.is_key_down(rl.KEY_UP))
    player_direction = rl.Vector3Normalize(player_direction)

    dt = pr.get_frame_time()
    player_position.x += player_direction.x * player_speed * dt
    player_position.z += player_direction.z * player_speed * dt

    # collisions
    is_collision = pr.check_collision_boxes(
            get_bounding_pos(player_model, player_position),
            get_bounding_pos(obs_model, obs_position),
        )

    pr.begin_drawing()
    pr.clear_background(rl.BLACK)

    pr.begin_mode_3d(camera)
    pr.draw_grid(10, 1)

    pr.draw_model(player_model, player_position, 1, pr.ORANGE)
    pr.draw_bounding_box(get_bounding_pos(player_model, player_position), pr.BLUE)
    pr.draw_model(obs_model, obs_position, 1, pr.GREEN) if not is_collision else pr.draw_model(obs_model, obs_position, 1, pr.SKYBLUE)
    pr.draw_bounding_box(get_bounding_pos(obs_model, obs_position), pr.DARKBLUE)

    pr.end_mode_3d()

    if is_collision:
        if pr.gui_text_box(pr.Rectangle(0, 40, 60, 20), b"Collision", 40, True):
            pass

    pr.draw_fps(0, 0)
    pr.draw_text(f"collision: {str(is_collision)}", 0, 20, 20, pr.GREEN)
    pr.end_drawing()

pr.close_window()
