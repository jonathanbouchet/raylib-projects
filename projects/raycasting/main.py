import pyray as pr
import math

window_width, window_height = 600, 600
DEBUG = False

pr.init_window(window_width, window_width, "test")
pr.set_target_fps(60)

walls = [
    {"pos": pr.Rectangle(400, 100, 50, 250), "color": pr.DARKGRAY},
    {"pos": pr.Rectangle(100, 400, 50, 50), "color": pr.DARKGRAY},
    {"pos": pr.Rectangle(300, 25, 200, 25), "color": pr.DARKGRAY},
    {"pos": pr.Rectangle(10, 300, 30, 200), "color": pr.DARKGRAY},
]


def rectangle_to_bounding_box(rect):
    """convert a Rectangle to a BBox"""
    bbox = pr.BoundingBox(
        pr.Vector3(rect.x, rect.y),
        pr.Vector3(rect.x + rect.width, rect.y + rect.height),
    )
    return bbox


max_rays = 50
frame_count = 0
while not pr.window_should_close():
    # logic
    frame_count += 1
    rays = []  # store the rays definition
    hits = []  # store all collisions (all rays to all boxes)
    boxes = []  # store the conversion of BBox to Rectangle

    current_position = pr.get_mouse_position()
    pr.draw_circle_v(current_position, 5, pr.GREEN)  # draw mouse position

    # define the ray starting point and direction
    for i in range(max_rays):
        theta = (2 * math.pi / max_rays) * i
        x = math.cos(theta)
        y = math.sin(theta)
        rays.append(
            pr.Ray(
                pr.Vector3(current_position.x, current_position.y, 0),
                pr.Vector3(x, y, 0),
            )
        )

    # obstacle
    for wall in walls:
        my_bbox = rectangle_to_bounding_box(wall.get("pos"))
        boxes.append(my_bbox)

    # check collision for each ray
    # save the result of the collision (true, false) as well as the ray id
    # this will be used later for displaying the rays that hit the BBox or not
    for ray_id, ray in enumerate(rays):
        for box in boxes:
            collision = pr.get_ray_collision_box(ray, box)
            hits.append({"ray_id": ray_id, "collision": collision})

    if DEBUG:
        print("all hits")
        for hit in hits:
            print(
                f"ray_id: {hit['ray_id']}, {hit['collision'].hit}, {hit['collision'].distance}, ({hit['collision'].point.x}, {hit['collision'].point.y})"
            )

    # cleanup ghost collisions = collisions that happen for a box behind one that has been hit by the ray
    clean_hits = []
    for id in range(0, max_rays):
        tmp_hits = []
        no_hits = []
        has_hits = []

        for hit in hits:
            if hit["ray_id"] == id:
                if hit["collision"].hit:
                    tmp_hits.append(hit)
                else:
                    no_hits.append(hit)

        if len(tmp_hits) > 1:
            min_distance_hit = min(
                tmp_hits, key=lambda x: abs(x["collision"].distance)
            )  # take the absolute value because the distance of the collision to the mouse is signed
            has_hits.append(min_distance_hit)
            clean_hits.extend(no_hits + has_hits)
        else:
            clean_hits.extend(no_hits + tmp_hits)
    if DEBUG:
        print("clean hits")
        for hit in clean_hits:
            print(
                f"ray_id: {hit['ray_id']}, {hit['collision'].hit}, {hit['collision'].distance}, ({hit['collision'].point.x}, {hit['collision'].point.y})"
            )

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    # draw_wall
    for wall in walls:
        pr.draw_rectangle_rec(wall.get("pos"), pr.DARKBLUE)

    # get ray_id that did not collide with any box
    ray_id_not_hit = [hit["ray_id"] for hit in clean_hits]
    ray_results = []
    for r in range(0, max_rays):
        tmp = {}
        tmp_collision = []
        for hit in clean_hits:
            if hit["ray_id"] == r:
                tmp_collision.append(hit["collision"].hit)
        tmp[r] = tmp_collision
        ray_results.append(tmp)
    # example output:
    # {"ray_id": [collision_with box_1, collision_with box_1,collision_with box_2, ... collision_with box_i]}
    # [{0: [False, False, False, False]}, {1: [False, False, False, False]}, {2: [False, False, False, False]}, {3: [False, False, False, False]}}

    if DEBUG:
        print(f"ray results: {ray_results}")
    results = [[k for k, v in d.items() if not any(v)] for d in ray_results]
    no_hit_ray_id = [int(r[0]) for r in results if len(r) > 0]
    if DEBUG:
        print(f"{no_hit_ray_id=}")

    for id, ray in enumerate(rays):
        if id in no_hit_ray_id:
            pr.draw_ray(ray, pr.RED)

    # draw the rays that did collide
    for hit in clean_hits:
        if hit["collision"].hit:
            if DEBUG:
                print(
                    f"green: ray_id: {hit['ray_id']}, {hit['collision'].hit}, {hit['collision'].distance}, ({hit['collision'].point.x}, {hit['collision'].point.y})"
                )
            pr.draw_line_v(
                current_position,
                pr.Vector2(hit["collision"].point.x, hit["collision"].point.y),
                pr.GREEN,
            )
            pr.draw_circle_v(
                pr.Vector2(hit["collision"].point.x, hit["collision"].point.y),
                5,
                pr.GREEN,
            )

    pr.draw_fps(0, 0)
    if DEBUG:
        pr.draw_text(f"frame:{frame_count}", 0, 20, 20, pr.GREEN)
    pr.end_drawing()
pr.close_window()
