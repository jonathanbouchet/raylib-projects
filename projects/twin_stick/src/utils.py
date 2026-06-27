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


def wrap_borders(position: pr.Vector2, width: int, height: int) -> pr.Vector2:
    # check borders to re-appear on the other side of the screen
    if position.x > width:
        position.x = 0
    if position.x < 0:
        position.x = width
    if position.y > height:
        position.y = 0
    if position.y < 0:
        position.y = height
    return position
