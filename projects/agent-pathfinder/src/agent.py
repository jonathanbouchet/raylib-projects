import random
import math
import copy
import numpy as np
from scipy.spatial import KDTree
import pyray as pr
from .waypoint import WayPoints, WayPoint


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
        color: pr.Color
    ) -> None:
        self.position = position
        self.direction = direction
        self.speed = speed
        self.debug = debug
        # self.waypoint_idx: int = 19
        self.rotation = 0
        self.rotation_speed = 180
        self.is_turning = False
        self.texture = texture
        self.origin = pr.Vector2(self.texture.width / 2, self.texture.height / 2)
        self.width=width
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

        # if True:#waypoint_id == 1:
        #     self.rotation = lerp_angle_2d(current_angle=self.rotation, target_angle=self.rotation+90, t=dt)

    def draw(self) -> None:

        # # Source rectangle (entire texture)
        # source = pr.Rectangle(0, 0, self.texture.width, self.texture.height)
        # # Destination rectangle (where it draws and its scaled size)
        # dest = pr.Rectangle(
        #     self.position.x, self.position.y, self.texture.width, self.texture.height
        # )
        # pr.draw_texture_pro(
        #     self.texture, source, dest, self.origin, self.rotation, pr.WHITE
        # )

        pr.draw_rectangle_v(pr.vector2_subtract(self.position, pr.Vector2(self.width//2, self.height//2)), pr.Vector2(self.width, self.height), self.color)
        # pr.draw_texture_v(self.texture, self.position, pr.WHITE)
        # pr.draw_texture_ex(self.texture, self.position, self.rotation, 1.0, pr.WHITE)
        # print(f"{self.rotation=}")
        # if self.debug:
        #     pr.draw_circle_lines_v(
        #         pr.Vector2(
        #             self.position.x + self.width / 2, self.position.y + self.height / 2
        #         ),
        #         self.detection_area,
        #         self.current_color,
        #     )

    def update(self, dt: float, waypoints: WayPoints) -> None:
        # print(f"player x: {self.position.x}, {self.position.y}")
        current_waypoint = waypoints.get_waypoint(self.waypoint_idx)
        # waypoints.waypoints.index
        # print(waypoints.waypoint_ids[self.waypoint_idx])
        # current_waypoint = waypoints.get_waypoint_data(self.find_closest(markers=waypoints))

        # current_waypoint = waypoints.get_waypoint_data(self.find_closest_2(markers=waypoints))
        # print(f"{self.waypoint_idx}")

        # Vector math: direction to target
        dir_x = current_waypoint.position.x - self.position.x
        dir_y = current_waypoint.position.y - self.position.y

        distance = math.hypot(dir_x, dir_y)
        reach_threshold = 5
        # print(f"{distance=}")

        if distance <= reach_threshold:
            print(f"current: {current_waypoint.get_idx()}, reached: {distance}")
            # print(f"player x: {self.position.x}, {self.position.y}")
            # Snap to target and switch to next waypoint
            self.position.x = current_waypoint.position.x
            self.position.y = current_waypoint.position.y
            # self.waypoint_idx += 1
            
            # test: finding closest marker to the current position
            # TO DO: do not include the current waypoint, otherwise it will go back to it
            tmp: list[pr.Vector2] = []
            # tmp: list[WayPoint] = []
            print("to be used in current search:")
            for cnt, waypoint in enumerate(waypoints.waypoints):
                # if waypoint.get_idx() != self.waypoint_idx:
                # if waypoint.get_idx() not in [current_waypoint.get_idx()]:
                if cnt not in [current_waypoint.get_idx(), self.previous]:
                    print(f"{waypoint.get_idx()}, {waypoint.get_position().x}, {waypoint.get_position().y}")
                    tmp.append(waypoint.get_position())
                else:
                    tmp.append(pr.Vector2(-9999, -9999))
                    print(f"adding fake at position: {cnt}")

            # make a deepcopy:
            # tmp: WayPoints = copy.deepcopy(waypoints)
            # tmp_waypoint_index = waypoints.index(self.waypoint_idx)
            # tmp.pop(tmp_waypoint_index)

            print(f"previous: {self.previous}")
            self.previous = self.waypoint_idx

            self.waypoint_idx = self.find_closest(tmp)
            # test_kdtree = self.find_closest_kdtree(tmp)
            # print(f"result from KDTree: {test_kdtree=}")
            # self.waypoint_idx = self.find_closest_3(tmp)
            # self.waypoint_idx = self.find_closest_2(waypoints)
            
            # if self.waypoint_idx > waypoints.num_points - 1:
            #     # warp around the max number of way points
            #     self.waypoint_idx = 0
        else:
            # Move toward target linearly
            self.position.x += (dir_x / distance) * self.speed * dt
            self.position.y += (dir_y / distance) * self.speed * dt

        # testing: handling corner rotation
        # if self.waypoint_idx > 0 and self.waypoint_idx <= 2:
        #     self.is_turning = True
        #     self.rotation += self.rotation_speed * dt
        # else:
        #     self.is_turning = False
        #     # correcting by hand the desired rotation
        #     if self.waypoint_idx == 3:
        #         self.rotation = 90
        #     elif self.waypoint_idx == 4:
        #         self.rotation = 180
        #     elif self.waypoint_idx == 5:
        #         self.rotation = 270
        #     elif self.waypoint_idx == 0:
        #         self.rotation = 0

        # self.move(dt=dt, target_pos=current_waypoint.position)
        # # check if entity has arrived to the waypoint, then increment the waypoint_idx to patrol to the next one
        # if pr.check_collision_point_circle(
        #     self.position,
        #     current_waypoint.position,
        #     current_waypoint.detection_area,
        # ):
        #     self.rotation += self.rotation_speed * dt
        #     self.waypoint_idx += 1
        #     # possible_waypoints = list(range(4))
        #     # possible_waypoints.remove(self.waypoint_idx)
        #     # idx = random.choices(possible_waypoints)
        #     # self.waypoint_idx = idx[0]
        #     # print(f"{self.waypoint_idx}, {waypoints.num_points}")
        #     if self.waypoint_idx > waypoints.num_points - 1:
        #         # warp around the max number of way points
        #         self.waypoint_idx = 0

    def find_closest0(self, markers: list[WayPoint]) -> int:
        print(f"starting search with player pos: {self.position.x}, {self.position.y}")
        min = 0
        first = markers[0]
        min_dst_sq = (self.position.x - first.position.x)**2 + (self.position.y - first.position.y)**2
        for i in range(1, len(markers)):
            current = markers[i]
            current_dst_sq = (self.position.x - current.position.x)**2 + (self.position.y - current.position.y)**2
            print(f"{i=}, {current.position.x=},{current.position.y=},{current_dst_sq=}")
            if current_dst_sq < min_dst_sq:
                min = current.get_idx()
                min_dst_sq = current_dst_sq
                print(f"{min=}, {min_dst_sq=}")
        print(f"final: {min=}, {min_dst_sq}")
        return min

    def find_closest(self, markers: list[pr.Vector2]) -> int:
            print(f"starting search with player pos: {self.position.x}, {self.position.y}")
            min = 0
            first = markers[0]
            min_dst_sq = (self.position.x - first.x)**2 + (self.position.y - first.y)**2
            for i in range(1, len(markers)):
                current = markers[i]
                current_dst_sq = (self.position.x - current.x)**2 + (self.position.y - current.y)**2
                print(f"{i=}, {current.x=},{current.y=},{current_dst_sq=}")
                if current_dst_sq < min_dst_sq:
                    min = i
                    min_dst_sq = current_dst_sq
                    print(f"{min=}, {min_dst_sq=}")
            print(f"final: {min=}, {min_dst_sq}")
            return min

    def find_closest_2(self, markers: WayPoints) -> int:
        agent_xy = np.array((self.position.x, self.position.y), dtype=float)  # shape (2,)

        waypoints = np.array(
            [(markers.get_waypoint(m).position.x, markers.get_waypoint(m).position.y) for m in range(0, markers.get_number_waypoints())], 
            dtype=float
        )

        # Squared distances (no sqrt needed)
        d2 = np.sum((waypoints - agent_xy) ** 2, axis=1)  # shape (N,)

        # Indices of 2 smallest distances
        i2 = np.argpartition(d2, 2)[:2]  # unordered
        i2 = i2[np.argsort(d2[i2])]     # order by distance

        closest_idx = int(i2[0])
        second_closest_idx = int(i2[1])
        print(f"{closest_idx=}, {second_closest_idx=}")

        # closest = waypoints[i2]
        # print(f"{closest=}, {d2[i2]=}")
        # return closest, d2[i2]
        return second_closest_idx

    def find_closest_3(self, markers: list[pr.Vector2]) -> int:
        agent_xy = np.array((self.position.x, self.position.y), dtype=float)  # shape (2,)
    
        waypoints = np.array(
            [(m.x, m.y) for m in markers], 
            dtype=float
        )

        # Squared distances (no sqrt needed)
        d2 = np.sum((waypoints - agent_xy) ** 2, axis=1)  # shape (N,)

        # Indices of 2 smallest distances
        i2 = np.argpartition(d2, 2)[:2]  # unordered
        i2 = i2[np.argsort(d2[i2])]     # order by distance

        closest_idx = int(i2[0])
        second_closest_idx = int(i2[1])
        print(f"{closest_idx=}, {second_closest_idx=}")

        # closest = waypoints[i2]
        # print(f"{closest=}, {d2[i2]=}")
        # return closest, d2[i2]
        # return second_closest_idx
        return closest_idx

    def find_closest_kdtree(self, markers: list[pr.Vector2]) -> int:
        points = np.array([(m.x, m.y) for m in markers], 
        dtype=float)

        tree = KDTree(points)  # builds the index once

        agent_pos = np.array([self.position.x, self.position.y], dtype=float)
        dist, idx = tree.query(agent_pos)  # nearest neighbor

        closest_waypoint = points[idx]
        print("closest idx:", idx, "point:", closest_waypoint, "dist:", dist) 

        return idx

