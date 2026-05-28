import pyray as pr
import raylib as rl


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        color: pr.Color,
        speed: int,
        detection_area,
        debug: bool = False,
    ) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.color: pr.Color = color
        self.speed: int = speed
        self.detection_area: int = detection_area
        self.debug: bool = debug

    def move(self, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        self.move(dt=dt)

    def draw(self) -> None:
        pass


class WayPoints:
    def __init__(
        self,
        positions: list[pr.Vector2],
        color: pr.Color,
        width: int,
        height: int,
        detection_area: int,
    ):
        self.positions: list[pr.Vector2] = positions
        self.color: pr.Color = color
        self.num_points: int = len(self.positions)
        self.waypoint_width: int = width
        self.waypoint_height: int = height
        self.waypoints: list[Sprite] = []
        self.waypoint_ids: list[int] = []
        self.detection_area: int = detection_area

    def make_points(self) -> None:
        for cnt, position in enumerate(self.positions):
            point_sprite = Sprite(
                position=position,
                direction=pr.Vector2(0, 0),
                color=self.color,
                speed=0,
                detection_area=self.detection_area,
                debug=True,
            )
            self.waypoints.append(point_sprite)
            self.waypoint_ids.append(cnt)

    def get_waypoint_data(self, idx: int) -> Sprite:
        return self.waypoints[idx]

    def draw_points(self) -> None:
        for cnt, waypoint in enumerate(self.waypoints):
            pr.draw_rectangle_v(
                waypoint.position,
                pr.Vector2(self.waypoint_width, self.waypoint_height),
                self.color,
            )
            if waypoint.debug:
                pr.draw_circle_lines_v(
                    pr.Vector2(
                        waypoint.position.x + self.waypoint_width / 2,
                        waypoint.position.y + self.waypoint_height / 2,
                    ),
                    self.detection_area,
                    self.color,
                )
                pr.draw_text(
                    str(cnt),
                    int(waypoint.position.x),
                    int(waypoint.position.y - 20),
                    20,
                    self.color,
                )


class Player(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: int,
        color: pr.Color,
        width: int,
        height: int,
        detection_area: int,
        debug: bool,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            speed=speed,
            color=color,
            detection_area=detection_area,
            debug=debug,
        )
        self.width: int = width
        self.height: int = height

    def move(self, dt: float) -> None:

        # move player with mouse
        if pr.is_mouse_button_down(0):
            current_pos = self.position
            target_pos = pr.get_mouse_position()
            lerp_speed = 0.1

            current_pos = pr.vector2_lerp(current_pos, target_pos, lerp_speed)
            self.position = current_pos

        # move player with KB
        # self.direction.x = int(pr.is_key_down(rl.KEY_RIGHT)) - int(pr.is_key_down(rl.KEY_LEFT))
        # self.direction.y = int(pr.is_key_down(rl.KEY_DOWN)) - int(pr.is_key_down(rl.KEY_UP) )
        # this updates the position by adding to it a normalized direction
        # self.position = pr.vector2_add(
        #     self.position,
        #     pr.vector2_scale(pr.vector2_scale(self.direction, self.speed), dt),
        # )

    def draw(self) -> None:
        pr.draw_rectangle_v(
            self.position, pr.Vector2(self.width, self.height), self.color
        )
        if self.debug:
            pr.draw_circle_lines_v(
                pr.Vector2(
                    self.position.x + self.width / 2, self.position.y + self.height / 2
                ),
                self.detection_area,
                self.color,
            )


class Enemy(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: int,
        detection_area: int,
        color: pr.Color,
        width: int,
        height: int,
        debug: bool,
        color_detected: pr.Color,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            speed=speed,
            color=color,
            detection_area=detection_area,
            debug=debug,
        )
        self.width: int = width
        self.height: int = height
        self.color_detected: pr.Color = color_detected
        self.current_color: pr.Color = self.color
        self.waypoint_idx: int = 2

    def move(self, dt: float, target_pos: pr.Vector2) -> None:
        current_pos = self.position
        lerp_speed = 0.020

        current_pos = pr.vector2_lerp(current_pos, target_pos, lerp_speed)
        self.position = current_pos

    def draw(self) -> None:
        pr.draw_rectangle_v(
            self.position, pr.Vector2(self.width, self.height), self.current_color
        )
        if self.debug:
            pr.draw_circle_lines_v(
                pr.Vector2(
                    self.position.x + self.width / 2, self.position.y + self.height / 2
                ),
                self.detection_area,
                self.current_color,
            )

    def update(self, dt: float, player: Player, waypoints: WayPoints) -> None:
        # self.detect_player(dt=dt, player=player)
        current_waypoint = waypoints.get_waypoint_data(self.waypoint_idx)
        self.move(dt=dt, target_pos=current_waypoint.position)
        # check if enemy has arrived to the waypoint, then increment the waypoint_idx to patrol to the next one
        if pr.check_collision_point_circle(
            self.position, current_waypoint.position, current_waypoint.detection_area
        ):
            self.waypoint_idx += 1
            # print(f"{self.waypoint_idx}, {waypoints.num_points}")
            if self.waypoint_idx > waypoints.num_points - 1:
                # warp around the max number of way points
                self.waypoint_idx = 0

    def detect_player(self, dt: float, player: Player):
        if pr.check_collision_point_circle(
            self.position, player.position, player.detection_area
        ):
            self.current_color = self.color_detected
            self.move(dt=dt, target_pos=player.position)
        else:
            self.current_color = self.color
