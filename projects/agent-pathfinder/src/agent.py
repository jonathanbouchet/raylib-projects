import math
import pyray as pr
from .waypoint import WayPoints


def lerp_angle_2d(current_angle, target_angle, t):
    """Smoothly interpolates between two 2D angles in radians via the shortest path."""
    difference = target_angle - current_angle

    # Normalize the difference to the range [-PI, PI] to get the shortest path
    # difference = (difference + math.pi) % (2 * math.pi) - math.pi

    return current_angle + difference * t


class Agent:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: int,
        debug: bool,
        texture: pr.Texture,
        width: int,
        height: int,
        color: pr.Color,
    ) -> None:
        self.position = position
        self.direction = direction
        self.speed = speed
        self.debug = debug
        self.rotation = 90
        self.rotation_speed = 180
        self.is_turning = False
        self.texture = texture
        self.origin = pr.Vector2(self.texture.width / 2, self.texture.height / 2)
        self.width = width
        self.height = height
        self.color = color
        self.previous: int = None

    def set_initial_waypoint(self, markers: list[pr.Vector2]) -> None:
        self.waypoint_idx = self.find_closest(markers)

    def move(self, dt: float, target_pos: pr.Vector2) -> None:
        current_pos = self.position
        lerp_speed = 0.04  # 0.020

        current_pos = pr.vector2_lerp(current_pos, target_pos, lerp_speed)
        self.position = current_pos

    def draw(self) -> None:

        # Source rectangle (entire texture)
        source = pr.Rectangle(0, 0, self.texture.width, self.texture.height)
        # Destination rectangle (where it draws and its scaled size)
        dest = pr.Rectangle(
            self.position.x, self.position.y, self.texture.width, self.texture.height
        )
        pr.draw_texture_pro(
            self.texture, source, dest, self.origin, self.rotation, pr.WHITE
        )

    def update(self, dt: float, waypoints: WayPoints) -> None:
        current_waypoint = waypoints.get_waypoint(self.waypoint_idx)

        # Vector math: direction to target
        dir_x = current_waypoint.position.x - self.position.x
        dir_y = current_waypoint.position.y - self.position.y

        distance = math.hypot(dir_x, dir_y)
        reach_threshold = 10

        if distance <= reach_threshold:
            # Snap to target and switch to next waypoint
            self.position.x = current_waypoint.position.x
            self.position.y = current_waypoint.position.y

            # test: finding closest marker to the current position
            tmp: list[pr.Vector2] = []
            for cnt, waypoint in enumerate(waypoints.waypoints):
                if cnt not in [current_waypoint.get_idx(), self.previous]:
                    tmp.append(waypoint.get_position())
                else:
                    tmp.append(pr.Vector2(-9999, -9999))

            self.previous = self.waypoint_idx
            self.waypoint_idx = self.find_closest(tmp)
        else:
            # Move toward target linearly
            self.position.x += (dir_x / distance) * self.speed * dt
            self.position.y += (dir_y / distance) * self.speed * dt

            # handle rotation
            targetpos = waypoints.get_waypoint(self.waypoint_idx).get_position()
            direction = pr.Vector2(
                targetpos.x - self.position.x, targetpos.y - self.position.y
            )
            self.rotation = 90 + math.degrees(math.atan2(direction.y, direction.x))

    def find_closest(self, markers: list[pr.Vector2]) -> int:
        min = 0
        first = markers[0]
        min_dst_sq = (self.position.x - first.x) ** 2 + (self.position.y - first.y) ** 2
        for i in range(1, len(markers)):
            current = markers[i]
            current_dst_sq = (self.position.x - current.x) ** 2 + (
                self.position.y - current.y
            ) ** 2
            if current_dst_sq < min_dst_sq:
                min = i
                min_dst_sq = current_dst_sq
        return min
