import pyray as pr
import raylib as rl
import math

width, height = 800, 600
icon_width, icon_height = 20, 20

# earth parameters
a: int = 200  # radiusH
b: int = 100  # radiusV
c: int = int(math.sqrt(a**2 + b**2))  # 1 of the focus point of the ellipse

# sun radius
sun_radius = 1
# earth parameters
speed_revolution = 0.5
earth_distance_to_sun = 20
earth_radius = 2

# moon parameters
distance_to_earth = 3
r_moon = 0.5
moon_speed_revolution = 0.5

# mars parameters
mars_distance_to_sun = 30
mars_radius = 1.5
# moons
distance_to_mars = [2, 3]
r_mars_moon = [0.25, 0.35]
mars_moon_speed_revolution = 0.5

pr.init_window(width, height, "ellipse")
pr.set_target_fps(60)

# camera
camera = pr.Camera3D()
camera.position = pr.Vector3(0.0, 20.0, 60.0)
camera.target = pr.Vector3(0.0, 0.0, 0.0)
camera.up = pr.Vector3(0.0, 1.0, 0.0)
camera.fovy = 45.0
camera.projection = rl.CAMERA_PERSPECTIVE

dl = 0
dl_moon = 0
speed_revolution = 1 / 4
slider_value = pr.ffi.new("float *", 1.0)  # Initial value

camera_speed = 5

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
    dl += dt * slider_value[0]
    dl_moon += dt
    x = earth_distance_to_sun * math.cos(dl * speed_revolution * 2 * math.pi)
    z = earth_distance_to_sun * math.sin(dl * speed_revolution * 2 * math.pi)

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.Color(43, 46, 44, 255))
    pr.begin_mode_3d(camera)

    # draw sun
    pr.draw_sphere(pr.Vector3(-10, 0, 0), sun_radius, pr.Color(252, 229, 112, 255))

    # draw Earth's trajectory
    pr.draw_circle_3d(
        pr.Vector3(0, 0, 0),
        earth_distance_to_sun,
        pr.Vector3(1, 0, 0),
        90,
        pr.Color(40, 122, 184, 255),
    )

    # draw Earth
    pr.draw_sphere(pr.Vector3(x, 0, z), earth_radius, pr.Color(40, 122, 184, 255))

    # draw Earth's moon
    x_moon = x + distance_to_earth * math.cos(
        dl_moon * moon_speed_revolution * 2 * math.pi
    )
    z_moon = z + distance_to_earth * math.sin(
        dl_moon * moon_speed_revolution * 2 * math.pi
    )
    pr.draw_sphere(pr.Vector3(x_moon, 0, z_moon), r_moon, pr.Color(246, 241, 213, 255))

    # draw Mars's trajectory
    pr.draw_circle_3d(
        pr.Vector3(0, 0, 0),
        mars_distance_to_sun,
        pr.Vector3(1, 0, 0),
        90,
        pr.Color(150, 69, 20, 255),
    )

    x_mars = mars_distance_to_sun * math.cos(dl * speed_revolution / 1.9 * 2 * math.pi)
    z_mars = mars_distance_to_sun * math.sin(dl * speed_revolution / 1.9 * 2 * math.pi)

    # draw Mars
    pr.draw_sphere(
        pr.Vector3(x_mars, 0, z_mars), mars_radius, pr.Color(150, 69, 20, 255)
    )

    # draw Mars's moon
    for i in range(0, 2):
        x_mars_moon = x_mars + distance_to_mars[i] * math.cos(
            dl_moon * moon_speed_revolution * 2 * math.pi
        )
        z_mars_moon = z_mars + distance_to_mars[i] * math.sin(
            dl_moon * moon_speed_revolution * 2 * math.pi
        )
        pr.draw_sphere(
            pr.Vector3(x_mars_moon, 0, z_mars_moon),
            r_mars_moon[i],
            pr.Color(142, 106, 90, 255),
        )

    pr.draw_grid(15, 5.0)
    pr.end_mode_3d()

    pr.draw_fps(0, 580)
    pr.end_drawing()

# pr.unload_texture(background)
pr.close_window()
