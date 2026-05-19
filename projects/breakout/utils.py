import pyray as pr
import raylib as rl
import settings as setting

def rect_to_bounding_box(rect: pr.Rectangle) -> pr.BoundingBox:
    # Define the minimum corner (top-left)
    min_vec = pr.Vector3(rect.x, rect.y, 0.0)
    
    # Define the maximum corner (bottom-right)
    max_vec = pr.Vector3(rect.x + rect.width, rect.y + rect.height, 0.0)
    
    # Return the new BoundingBox structure
    return pr.BoundingBox(min_vec, max_vec)


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        color: pr.Color,
        disabled: bool,
    ) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.width: int = width
        self.height: int = height
        self.speed: int = speed
        self.color: pr.Color = color
        self.disabled: bool = disabled


class Player(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        roundness: float,
        color: pr.Color,
        disabled: bool,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color,
            disabled=disabled,
        )
        self.player_roundness = roundness

    def move(self, dt: float) -> None:
        self.direction.x = int(pr.is_key_down(rl.KEY_RIGHT)) - int(
            pr.is_key_down(rl.KEY_LEFT)
        )
        if self.position.x < 0:
            self.position.x = 0
        if self.position.x + self.width > setting.window_width:
            self.position.x = setting.window_width - self.width
        dt = pr.get_frame_time()
        self.position.x += self.direction.x * self.speed * dt

    def draw(self) -> None:
        pr.draw_rectangle_rounded(
            pr.Rectangle(self.position.x, self.position.y, self.width, self.height),
            self.player_roundness,
            20,
            self.color,
        )

    def update(self, dt) -> None:
        self.move(dt=dt)


class Brick(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        roundness: float,
        color: pr.Color,
        disabled: bool,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color,
            disabled=disabled,
        )

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pr.draw_rectangle_v(
            pr.Vector2(self.position.x, self.position.y),
            pr.Vector2(self.width, self.height),
            self.color,
        )


class Bricks(Brick):
    def __init__(self, num_brick: int, brick_height: int, num_row: int):
        self.num_brick: int = num_brick
        self.brick_height: int = brick_height
        self.num_row: int = num_row
        self.brick_width: int = int(setting.window_width / self.num_brick) - 20
        self.bricks_list: list[Brick] = []

    def make_bricks(self):
        for i in range(5):
            for j in range(2):
                # print(i,j)
                pos_x = i*120 + 10
                pos_y = j*40 + 10
                print(f"{pos_x=}, {pos_y=}, {self.brick_width=}")
                brick = Brick(
                    pr.Vector2(pos_x, pos_y), 
                    direction=pr.Vector2(0,0), 
                    width=100, 
                    height=30, 
                    speed=0, 
                    roundness=0, 
                    color=setting.brick_color, 
                    disabled=False,
                )
                self.bricks_list.append(brick)

    def update(self, dt: float, ball_center: pr.Vector2, ball_radius: float) -> None:
        for brick in self.bricks_list:
            brick_bounding_box = rect_to_bounding_box(pr.Rectangle(brick.position.x, brick.position.y, 100, 300))
            if pr.check_collision_box_sphere(pr.BoundingBox(brick_bounding_box), pr.Vector3(ball_center.x, ball_center.y, 0), ball_radius):
                brick.disabled = True

    def draw(self) -> None:
        _ = [brick.draw() for brick in self.bricks_list if not brick.disabled]



class Ball(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        width: int,
        height: int,
        speed: int,
        color: pr.Color,
        disabled: bool,
    ) -> None:
        super().__init__(
            position=position,
            direction=direction,
            width=width,
            height=height,
            speed=speed,
            color=color,
            disabled=disabled,
        )

    def move(self, dt: float) -> None:
        if (
            self.position.x - self.width / 2 < 0
            or self.position.x + self.width / 2 > setting.window_width
        ):
            self.direction.x *= -1
        if (
            self.position.y - self.width / 2 < 0
            or self.position.y + self.width / 2 > setting.window_height
        ):
            self.direction.y *= -1

        dt = pr.get_frame_time()
        self.direction = pr.vector2_normalize(self.direction)
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

    def draw(self) -> None:
        pr.draw_circle_v(self.position, self.width, self.color)

    def update(self, dt) -> None:
        self.move(dt=dt)
