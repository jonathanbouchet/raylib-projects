import pyray as pr
import settings as setting
from brick import Brick


class Bricks(Brick):
    def __init__(self, num_brick: int, brick_height: int, num_row: int):
        self.num_brick: int = num_brick
        self.brick_height: int = brick_height
        self.num_row: int = num_row
        self.brick_width: int = int(setting.window_width / self.num_brick) - 20
        self.bricks_list: list[Brick] = []

    def make_bricks(self):
        for i in range(10):
            for j in range(3):
                pos_x = i * 60 + 10
                pos_y = j * 40 + 10
                brick = Brick(
                    pr.Vector2(pos_x, pos_y),
                    direction=pr.Vector2(0, 0),
                    width=50,
                    height=30,
                    speed=0,
                    roundness=0,
                    color=setting.brick_color,
                    disabled=False,
                )
                self.bricks_list.append(brick)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        _ = [brick.draw() for brick in self.bricks_list if not brick.disabled]

    def get_bricks_destroyed_count(self) -> None:
        return len([brick for brick in self.bricks_list if brick.disabled])
