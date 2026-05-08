import pyray as pr
import math

window_width, window_height = 600, 600

pr.init_window(window_width, window_width, "test")
pr.set_target_fps(60)

walls = [
    {"pos": pr.Vector2(50, 100), "size": pr.Vector2(50, 400), "color": pr.DARKGRAY},
    {"pos": pr.Vector2(450, 100), "size": pr.Vector2(50, 200), "color": pr.DARKGRAY},
]


def rectangle_to_bounding_box(rect):
    """convert a Rectangle to a BBox"""
    bbox = pr.BoundingBox(
        pr.Vector3(rect.x, rect.y),
        pr.Vector3(rect.x + rect.width, rect.y + rect.height),
    )
    return bbox


max_rays = 20
while not pr.window_should_close():
    # logic
    rays = []  # store the rays definition
    hits = []
    hits_data = []
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
    wall = pr.Rectangle(400, 100, 50, 250)
    my_bbox = rectangle_to_bounding_box(wall)

    # check collision for each ray
    # save the result of the collision (true, false) as well as the ray id
    # this will be used later for displaying the rays that hit the BBox or not
    for ray_id, ray in enumerate(rays):
        collision = pr.get_ray_collision_box(ray, my_bbox)
        hits.append({"ray_id": ray_id, "collision": collision})

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    # draw_wall
    pr.draw_rectangle_rec(wall, pr.DARKBLUE)

    # draw the rays that did not collide
    ray_id_not_hit = [hit["ray_id"] for hit in hits if not hit["collision"].hit]
    for id, ray in enumerate(rays):
        if id in ray_id_not_hit:
            pr.draw_ray(ray, pr.RED)

    # draw the rays that did collde
    for hit in hits:
        if hit["collision"].hit:
            print(
                f"ray_id: {hit['ray_id']}, {hit['collision'].hit}, {hit['collision'].distance}, ({hit['collision'].point.x}, {hit['collision'].point.y})"
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
    pr.end_drawing()
pr.close_window()
