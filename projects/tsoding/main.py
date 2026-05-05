import pyray as pr
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


dz = 1  # translation value by frame
da = 0  # rotation value by frame

vals = [
    {"x": -0.25, "y": 0.25, "z": 0.25},
    {"x": -0.25, "y": -0.25, "z": 0.25},
    {"x": 0.25, "y": 0.25, "z": 0.25},
    {"x": 0.25, "y": -0.25, "z": 0.25},
    {"x": -0.25, "y": 0.25, "z": -0.25},
    {"x": -0.25, "y": -0.25, "z": -0.25},
    {"x": 0.25, "y": 0.25, "z": -0.25},
    {"x": 0.25, "y": -0.25, "z": -0.25},
]

vertices = [
    [0, 1, 3, 2, 0],  # vertices front
    [4, 5, 7, 6, 4],  # vertices back
    [0, 4],  # vertices top left
    [2, 6],  # vertices top rigth
    [1, 5],  # vertices bottom left
    [3, 7],  # vertices bottom right
]


while not pr.window_should_close():
    dt = pr.get_frame_time()
    # dz += dt
    da += math.pi * dt
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    # draw vertices
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

    # draw lines
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

    pr.draw_fps(0, 0)

    pr.end_drawing()

pr.close_window()
