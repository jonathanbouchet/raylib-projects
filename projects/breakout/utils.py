import math
import random
import pyray as pr


def generate_random_unit_vector() -> tuple[float, float]:
    theta = random.uniform(0, 2 * math.pi)
    x = math.cos(theta)
    y = math.sin(theta)
    return [x, y]


def rect_to_bounding_box(rect: pr.Rectangle) -> pr.BoundingBox:
    min_vec = pr.Vector3(rect.x, rect.y, 0.0)
    max_vec = pr.Vector3(rect.x + rect.width, rect.y + rect.height, 0.0)
    return pr.BoundingBox(min_vec, max_vec)
