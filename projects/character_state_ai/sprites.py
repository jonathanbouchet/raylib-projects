import pyray as pr
import raylib as rl


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        color: pr.Color,
        speed: int,
        debug: bool = False,
    ) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.color: pr.Color = color
        self.speed: int = speed
        self.debug: bool = debug

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

    def update(self, dt: float) -> None:
        self.move(dt=dt)

    def draw(self) -> None:
        pass


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
            debug=debug,
        )
        self.width: int = width
        self.height: int = height
        self.detection_area: int = detection_area

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
                pr.Color(0, 255, 0, 255),
            )


class Enemy(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: int,
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
            debug=debug,
        )
        self.width: int = width
        self.height: int = height
        self.color_detected: pr.Color = color_detected
        self.current_color: pr.Color = self.color

    def move(self, dt: float, target_pos: pr.Vector2) -> None:
        current_pos = self.position
        lerp_speed = 0.025

        current_pos = pr.vector2_lerp(current_pos, target_pos, lerp_speed)
        self.position = current_pos

    def draw(self) -> None:
        pr.draw_rectangle_v(
            self.position, pr.Vector2(self.width, self.height), self.current_color
        )

    def update(self, dt: float, player: Player) -> None:
        self.detect_player(dt=dt, player=player)

    def detect_player(self, dt: float, player: Player):
        if pr.check_collision_point_circle(
            self.position, player.position, player.detection_area
        ):
            self.current_color = self.color_detected
            self.move(dt=dt, target_pos=player.position)
        else:
            self.current_color = self.color
