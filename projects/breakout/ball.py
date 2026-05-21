import random
import pyray as pr
import raylib as rl
from sprite import Sprite
import settings as setting
from player import Player
from utils import rect_to_bounding_box
from bricks import Bricks


class Ball(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        color: list[pr.Color],
        disabled: bool,
        spawned: bool,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color[0],
            disabled=disabled,
        )
        self.spawned: bool = spawned
        self.spawn_count: int = 0

    def move(self, dt: float) -> None:
        if (
            self.position.x - self.width / 2 < 0
            or self.position.x + self.width / 2 > setting.window_width
        ):
            self.direction.x *= -1
        if self.position.y - self.width / 2 < 0:
            self.direction.y *= -1
        if self.position.y - self.width > setting.window_height:
            # disable the ball
            self.disabled = True
            self.spawned = False

        dt = pr.get_frame_time()

        if pr.vector2_length(self.direction) > 0:
            self.direction = pr.vector2_normalize(self.direction)
        self.direction = (
            pr.vector2_normalize(self.direction)
            if pr.vector2_length(self.direction) > 0
            else self.direction
        )
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def draw(self) -> None:
        if not self.disabled:
            pr.draw_circle_v(self.position, self.width, self.color)

    def spawn_ball(self, position: pr.Vector2) -> None:
        """spawn_ball: spawn the ball in the top-middle of the player with random direction

        :param position: the current location of the player
        :type position: pr.Vector2
        """
        self.position.x = position.x + setting.player_width / 2
        self.position.y = position.y - self.width
        self.speed = 0
        self.disabled = False

    def start(self) -> None:

        # pr.draw_text(
        #     "Press Space to spawn ball",
        #     int(self.position.x) - 100,
        #     int(self.position.y) - 40,
        #     20,
        #     pr.WHITE,
        # )
        pr.draw_text(
            "Press Space to start",
            150,
            300,
            20,
            pr.WHITE,
        )

        if pr.is_key_pressed(rl.KEY_SPACE):
            self.spawn_count += 1
            self.spawned = True
            self.direction = pr.Vector2(
                random.uniform(-0.25, 0.25), random.uniform(-1, 0)
            )
            self.speed = setting.ball_speed

    def update(self, dt) -> None:
        self.move(dt=dt)

    def check_collision_player(self, player: Player) -> None:
        player_bounding_box = rect_to_bounding_box(
            pr.Rectangle(
                player.position.x, player.position.y, player.width, player.height
            )
        )
        if pr.check_collision_box_sphere(
            player_bounding_box,
            pr.Vector3(self.position.x, self.position.y, 0),
            self.width,
        ):
            self.direction.y *= -1

    def check_collision_bricks(self, bricks: Bricks) -> None:
        for brick in bricks.bricks_list:
            brick_bounding_box = rect_to_bounding_box(
                pr.Rectangle(brick.position.x, brick.position.y, 50, 30)
            )
            if pr.check_collision_box_sphere(
                brick_bounding_box,
                pr.Vector3(self.position.x, self.position.y, 0),
                self.width,
            ):
                brick.strength -= 1
                if brick.strength > 0:
                    self.direction.y *= -1
                    brick.current_color = brick.color[1]
                else:
                    brick.disabled = True
