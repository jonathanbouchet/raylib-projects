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


def dot(a: pr.Vector2, b: pr.Vector2) -> float:
    return a.x * b.x + a.y * b.y


def project_polygon(axis: pr.Vector2, pts):
    mn = mx = dot(axis, pts[0])
    for p in pts[1:]:
        v = dot(axis, p)
        mn = min(mn, v)
        mx = max(mx, v)
    return mn, mx


def check_OOB_collisions(poly_a, poly_b):
    # candidate axes: normals of all edges
    polys = [poly_a, poly_b]
    for poly in polys:
        for i in range(len(poly)):
            p1 = poly[i]
            p2 = poly[(i + 1) % len(poly)]
            edge = pr.Vector2(p2.x - p1.x, p2.y - p1.y)
            axis = pr.Vector2(-edge.y, edge.x)  # perpendicular

            # normalize axis
            length = math.hypot(axis.x, axis.y)
            if length == 0:
                continue
            axis = pr.Vector2(axis.x / length, axis.y / length)

            # optional normalize not required for overlap test
            a_min, a_max = project_polygon(axis, poly_a)
            b_min, b_max = project_polygon(axis, poly_b)
            if a_max < b_min or b_max < a_min:
                return False
    return True


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
