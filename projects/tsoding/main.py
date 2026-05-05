import pyray as pr
from data import vals, vertices
import math

window_width, window_height = 600, 600
default_size: int = 10  # pixels
default_color: pr.Color = pr.GREEN


pr.init_window(window_width, window_height, "test")
pr.set_target_fps(60)


def project(x: float, y: float, z: float):
    """convert screen coordinates to raylib display coordinates
    screen coordinates: x: [-1, 1], y: [-1, 1], center at (0,0)
    raylib coordinates: x:[ 0, width], y:[0, height], cneter of top left
    """
    return x / z, y / z, z


def translate_dz(x: float, y: float, z: float, dz: float):
    """translate a vertex in the z direction"""
    return x, y, z + dz


def rotate_xz(x: float, y: float, z: float, da: float):
    """rotate a vertex in the xz plane (around y)"""
    c = math.cos(da)
    s = math.sin(da)
    return x * c - z * s, y, x * s + z * c


def get_point(
    x: float, y: float, z: float, transformation: str, transformation_val: list[float]
) -> pr.Vector2:
    """return a vertex from the screen coordiantes to raylib coordinates"""
    if transformation == "translation":
        x, y, z = translate_dz(x, y, z, dz=transformation_val[0])

    if transformation == "rotation":
        x, y, z = rotate_xz(x, y, z, transformation_val[0])

    if transformation == "both":
        x, y, z = rotate_xz(x, y, z, transformation_val[1])
        x, y, z = translate_dz(x, y, z, dz=transformation_val[0])

    x, y, z = project(x, y, z)
    x = (x + 1) / 2 * window_width - default_size / 2
    y = (1 - (y + 1) / 2) * window_height - default_size / 2
    return pr.Vector2(x, y)


def draw_vertices():
    for val in vals:
        p = get_point(
            x=val.get("x"),
            y=val.get("y"),
            z=val.get("z"),
            transformation="both",
            transformation_val=[dz, da],
        )
        pr.draw_rectangle_v(
            pr.Vector2(int(p.x), int(p.y)),
            pr.Vector2(default_size, default_size),
            default_color,
        )


def draw_lines():
    for list_of_vertices in vertices:
        for idx in range(0, len(list_of_vertices) - 1):
            current = list_of_vertices[idx]
            next = list_of_vertices[idx + 1]
            p0 = vals[current]
            p1 = vals[next]
            pp0 = get_point(
                x=p0.get("x"),
                y=p0.get("y"),
                z=p0.get("z"),
                transformation="both",
                transformation_val=[dz, da],
            )
            pp1 = get_point(
                x=p1.get("x"),
                y=p1.get("y"),
                z=p1.get("z"),
                transformation="both",
                transformation_val=[dz, da],
            )
            pr.draw_line(
                int(pp0.x + default_size / 2),
                int(pp0.y + default_size / 2),
                int(pp1.x + default_size / 2),
                int(pp1.y + default_size / 2),
                default_color,
            )


dz = 1  # translation value by frame
da = 0  # rotation value by frame
active_ptr = pr.ffi.new("int *", 0)  # Initial value
slider_value = pr.ffi.new("float *", 3.14)  # Initial value

while not pr.window_should_close():
    selectedOption = pr.gui_toggle_group(
        pr.Rectangle(20, 20, 100, 20), "vertices;lines;both", active_ptr
    )
    sliderOption = pr.gui_slider(
        pr.Rectangle(20, 40, 100, 20), "0", "2pi", slider_value, 0.0, 6.28
    )

    dt = pr.get_frame_time()
    # dz += dt
    da += slider_value[0] * dt
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    if active_ptr[0] == 0:
        draw_vertices()
    elif active_ptr[0] == 1:
        draw_lines()
    else:
        draw_lines()
        draw_vertices()

    pr.draw_fps(20, 0)

    pr.end_drawing()

pr.close_window()
