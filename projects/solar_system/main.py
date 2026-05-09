import pyray as pr
import os
import math

width, height = 600, 600
DRAW_BACKGROUND = False
# ellipse equation:
# x=a*np.cos(t)
# y=b*np.sin(t)

# earth parameters
a: int = 200  # radiusH
b: int = 100  # radiusV
c: int = int(math.sqrt(a**2 + b**2))  # 1 of the focus point of the ellipse

center_x: int = int(width / 2)
center_y: int = int(height / 2)
speed_revolution = 0.5

# moon parameters
distance_to_earth = 30
r_moon = 5
moon_speed_revolution = 0.5

pr.init_window(width, height, "ellipse")
pr.set_target_fps(60)

# background
if DRAW_BACKGROUND:
    background_path = (
        os.getcwd() + "/projects/solar_system/assets/deepsky_background.png"
    )
    background = pr.load_texture(background_path)

dl = 0
dl_moon = 0
speed_revolution = 1 / 30
slider_value = pr.ffi.new("float *", 1.0)  # Initial value

while not pr.window_should_close():
    # logic
    sliderOption = pr.gui_slider(
        pr.Rectangle(20, 40, 100, 20), "0", "2.0", slider_value, 0.0, 2.0
    )

    dt = pr.get_frame_time()
    dl += dt * slider_value[0]
    dl_moon += dt
    x = a * math.cos(dl * speed_revolution * 2 * math.pi) + center_x
    y = b * math.sin(dl * speed_revolution * 2 * math.pi) + center_y

    # update

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    if DRAW_BACKGROUND:
        pr.draw_texture(background, 0, 0, pr.WHITE)

    # draw trajectory
    pr.draw_ellipse_lines(center_x, center_y, a, b, pr.GREEN)

    # draw earth
    pr.draw_circle_v(pr.Vector2(x, y), 20, pr.BLUE)

    # draw sun
    pr.draw_circle_v(pr.Vector2(c, center_y), 5, pr.YELLOW)

    # draw moon
    x_moon = x + distance_to_earth * math.cos(
        dl_moon * moon_speed_revolution * 2 * math.pi
    )
    y_moon = y + distance_to_earth * math.sin(
        dl_moon * moon_speed_revolution * 2 * math.pi
    )
    pr.draw_circle_v(pr.Vector2(x_moon, y_moon), r_moon, pr.DARKGRAY)

    pr.draw_fps(0, 0)
    pr.end_drawing()

if DRAW_BACKGROUND:
    pr.unload_texture(background)
pr.close_window()
