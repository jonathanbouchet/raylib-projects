import pyray as pr
import raylib as rl
from stellar_objects import Star, Planetoid


width, height = 800, 600
icon_width, icon_height = 20, 20

pr.init_window(width, height, "ellipse")
pr.set_target_fps(60)

# camera
camera = pr.Camera3D()
camera.position = pr.Vector3(0.0, 20.0, 60.0)
camera.target = pr.Vector3(0.0, 0.0, 0.0)
camera.up = pr.Vector3(0.0, 1.0, 0.0)
camera.fovy = 45.0
camera.projection = rl.CAMERA_PERSPECTIVE

sun = Star(pr.Vector3(0, 0, 0), radius=2, color=pr.Color(252, 229, 112, 255))
earth = Planetoid(
    pr.Vector3(0, 0, 0),
    radius=1,
    color=pr.Color(40, 122, 184, 255),
    speed_revolution=0.25,
    distance_to_center=20,
)
earth_moon = Planetoid(
    pr.Vector3(0, 0, 0),
    radius=0.5,
    color=pr.Color(246, 241, 213, 255),
    speed_revolution=1,
    distance_to_center=3,
)
mars = Planetoid(
    pr.Vector3(0, 0, 0),
    radius=0.5,
    color=pr.Color(150, 69, 20, 255),
    speed_revolution=earth.speed_revolution / 1.88,
    distance_to_center=30,
)

dl = 0  # t component in the ellipse coordinates
dl_moon = 0  # t (moon) component in the ellipse coordinates

slider_value = pr.ffi.new("float *", 1.0)  # Initial value


camera_speed = 2

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

    sliderOption = pr.gui_slider(
        pr.Rectangle(80, 20, 100, 20), "0", "2.0", slider_value, 0.0, 2.0
    )

    dt = pr.get_frame_time()
    dl += dt * slider_value[0]  # take into account the factor from the slider
    dl_moon += dt

    earth.update(
        dl=dl, x_offset=0, z_offset=0
    )  # earth has no offset, it rotates around the sun
    earth_moon.update(
        dl=dl_moon, x_offset=earth.position.x, z_offset=earth.position.z
    )  # moon has an offset, i.e the position of the earth w/r the Sun
    mars.update(
        dl=dl, x_offset=0, z_offset=0
    )  # mars has no offset, it rotates around the sun

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.Color(43, 46, 44, 255))
    pr.begin_mode_3d(camera)

    sun.draw()
    earth.draw()
    earth.draw_trajectory(x_offset=0, z_offset=0)

    earth_moon.draw()
    earth_moon.draw_trajectory(x_offset=earth.position.x, z_offset=earth.position.z)

    mars.draw()
    mars.draw_trajectory(x_offset=0, z_offset=0)

    pr.draw_grid(15, 5.0)
    pr.end_mode_3d()

    pr.draw_fps(0, 575)
    pr.end_drawing()

pr.close_window()
