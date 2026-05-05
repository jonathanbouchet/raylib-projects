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
    return x, y, z + dz


def rotate_xz(x: float, y: float, z: float, da: float):
    c = math.cos(da)
    s = math.sin(da)
    return x * c - z * s, y, x * s + z * c


def draw_point(
    x: float, y: float, z: float, transformation: str, transformation_val: list[float]
):
    """draw a point if size default_size and color default_color"""
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
    pr.draw_rectangle_v(
        pr.Vector2(int(x), int(y)),
        pr.Vector2(default_size, default_size),
        default_color,
    )


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


while not pr.window_should_close():
    dt = pr.get_frame_time()
    dz += dt
    da += math.pi * dt
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    for val in vals:
        # draw_point(x=val.get("x"), y=val.get("y"), z=val.get("z"), transformation="translation", transformation_val=[dz])
        # draw_point(x=val.get("x"), y=val.get("y"), z=val.get("z"), transformation="rotation", transformation_val=[da])
        # draw_point(x=val.get("x"), y=val.get("y"), z=val.get("z"), transformation="both", transformation_val=[dz, da])
        draw_point(
            x=val.get("x"),
            y=val.get("y"),
            z=val.get("z"),
            transformation="both",
            transformation_val=[dz, da],
        )

    pr.draw_fps(0, 0)

    pr.end_drawing()

pr.close_window()
