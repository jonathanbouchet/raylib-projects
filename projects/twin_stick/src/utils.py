import math
import pyray as pr


def rotate_point(p: pr.Vector2, center: pr.Vector2, angle_deg: float) -> pr.Vector2:
    """
    - perform a rotation of point around center
    - rotation is done in local coordinate of the rectangle
    """
    a = math.radians(angle_deg)
    s, c = math.sin(a), math.cos(a)
    # translate to center
    x, y = p.x - center.x, p.y - center.y
    # rotate
    xr = x * c - y * s
    yr = x * s + y * c
    # translate back
    return pr.Vector2(center.x + xr, center.y + yr)


def draw_rotated_rect_lines(
    center: pr.Vector2, size: pr.Vector2, angle_deg: float, thick: float, color
):
    half = pr.Vector2(size.x / 2, size.y / 2)

    tl = pr.Vector2(center.x - half.x, center.y - half.y)
    tr = pr.Vector2(center.x + half.x, center.y - half.y)
    br = pr.Vector2(center.x + half.x, center.y + half.y)
    bl = pr.Vector2(center.x - half.x, center.y + half.y)

    tl = rotate_point(tl, center, angle_deg)
    tr = rotate_point(tr, center, angle_deg)
    br = rotate_point(br, center, angle_deg)
    bl = rotate_point(bl, center, angle_deg)

    pr.draw_line_ex(tl, tr, thick, color)
    pr.draw_line_ex(tr, br, thick, color)
    pr.draw_line_ex(br, bl, thick, color)
    pr.draw_line_ex(bl, tl, thick, color)
