# this script compares the collision detection for 3 methods
# 1. AABB straight collider  
# 2. using Polygoncollider
# 3. using a custom Oriented Bounding Boxes (OBB) using Separating Axis Theorem (SAT)

import math
import PolygonCollision
import pyray as pr
width, height = 600, 600

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

def get_rotated_corners(center: pr.Vector2, size: pr.Vector2, angle_deg: float):
    half = pr.Vector2(size.x / 2, size.y / 2)

    pts = [
        pr.Vector2(center.x - half.x, center.y - half.y),  # tl
        pr.Vector2(center.x + half.x, center.y - half.y),  # tr
        pr.Vector2(center.x + half.x, center.y + half.y),  # br
        pr.Vector2(center.x - half.x, center.y + half.y),  # bl
    ]
    for i in range(4):
        pts[i] = rotate_point(pts[i], center, angle_deg)
    return pts

def dot(a: pr.Vector2, b: pr.Vector2) -> float:
    return a.x * b.x + a.y * b.y

def project_polygon(axis: pr.Vector2, pts):
    mn = mx = dot(axis, pts[0])
    for p in pts[1:]:
        v = dot(axis, p)
        mn = min(mn, v)
        mx = max(mx, v)
    return mn, mx

def polygons_overlap_sat(poly_a, poly_b):
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

def AABB_collisions(r1: pr.Rectangle, r2: pr.Rectangle) -> bool:
    return (r1.x < r2.x + r2.width and
            r1.x + r1.width > r2.x and
            r1.y < r2.y + r2.height and
            r1.y + r1.height > r2.y)

pr.init_window(width, height, "app")
pr.set_target_fps(60)

rect1 = pr.Rectangle(0, 0, 40, 40)
rect2 = pr.Rectangle(width//2, height//2, 100, 80)
rect3 = pr.Rectangle(400, 400, 100, 80)

rotation = 90
angle = 0

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    angle += rotation * dt 
    pos = pr.get_mouse_position()
    rect1 = pr.Rectangle(pos.x, pos.y, 40, 40)

    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_line(0, height//2, width, height//2, pr.RED)
    pr.draw_line(width//2, 0, width//2, height, pr.RED)

    pr.draw_rectangle_lines_ex(rect1, 2, pr.GREEN)
    pr.draw_rectangle_pro(rect2, pr.Vector2(rect2.width/2, rect2.height/2), angle, pr.BLUE)
    pr.draw_rectangle_lines_ex(rect3, 2, pr.YELLOW)

    # tl, tr, br, bl
    rect1_pts = [
        pr.Vector2(rect1.x, rect1.y), 
        pr.Vector2(rect1.x + rect1.width, rect1.y), 
        pr.Vector2(rect1.x + rect1.width, rect1.y + rect1.height), 
        pr.Vector2(rect1.x, rect1.y + rect1.height)
    ]

    rect2_pts = get_rotated_corners(pr.Vector2(rect2.x, rect2.y), pr.Vector2(rect2.width, rect2.height), angle)

    # pylygoncollision
    polygon1 = PolygonCollision.shape.Shape(vertices = [tuple([r.x, r.y]) for r in rect1_pts])
    polygon2 = PolygonCollision.shape.Shape(vertices = [tuple([r.x, r.y]) for r in rect2_pts])


    pr.draw_fps(0,0)
    pr.draw_text("AABB:" + str((AABB_collisions(r1=rect1, r2=rect2))), 0, 20, 20, pr.BLUE)
    pr.draw_text("OBB:" + str(polygons_overlap_sat(rect1_pts, rect2_pts)),0, 40, 20, pr.BLUE)
    pr.draw_text("POLYGON-COL:" + str(polygon1.collide(polygon2)),0, 60, 20, pr.BLUE)
    pr.draw_text(str((AABB_collisions(r1=rect1, r2=rect3))), 0, 80, 20, pr.YELLOW)
    pr.draw_fps(0,0)
    pr.end_drawing()

pr.close_window()