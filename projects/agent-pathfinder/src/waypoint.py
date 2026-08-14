import pyray as pr


class WayPoint:
    def __init__(
        self,
        idx: int,
        position: pr.Vector2,
    ) -> None:
        self.idx = idx
        self.position: pr.Vector2 = position

    def get_idx(self) -> int:
        return self.idx

    def get_position(self) -> pr.Vector2:
        return self.position

    def move(self, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pass

    def __str__(self) -> str:
        return f"""
        Waypoint ID: {self.get_idx()},
        Position: [{self.position.x}, {self.position.y}]
        """


class WayPoints:
    def __init__(
        self,
        positions: list[pr.Vector2],
    ):
        self.positions: list[pr.Vector2] = positions
        self.waypoints: list[WayPoint] = []
        self.waypoint_ids: list[int] = []
        self.make_points()

    def make_points(self) -> None:
        for cnt, position in enumerate(self.positions):
            point_sprite = WayPoint(
                idx=cnt,
                position=position,
            )
            self.waypoints.append(point_sprite)
            self.waypoint_ids.append(cnt)

    def get_waypoint(self, idx: int) -> WayPoint:
        return self.waypoints[idx]

    def get_previous(self, idx: int) -> WayPoint:
        return self.waypoints[idx - 1]

    def get_number_waypoints(self) -> int:
        return len(self.waypoints)

    def draw_waypoint_index(self) -> None:
        for cnt, waypoint in enumerate(self.waypoints):
            pr.draw_text(
                str(waypoint.get_idx()),
                int(waypoint.position.x),
                int(waypoint.position.y - 20),
                10,
                pr.RED,
            )
