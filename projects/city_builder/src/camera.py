import pyray as pr
import raylib as rl


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scroll = pr.Vector2(0, 0)
        self.dx = 0
        self.dy = 0
        self.speed = 5

    def update(self) -> None:
        self.update_kb()

    def update_kb(self) -> None:
        if pr.is_key_down(rl.KEY_LEFT) or pr.is_key_down(rl.KEY_A):
            self.dx = 1 * self.speed
        elif pr.is_key_down(rl.KEY_RIGHT) or pr.is_key_down(rl.KEY_D):
            self.dx = -1 * self.speed
        elif pr.is_key_down(rl.KEY_UP) or pr.is_key_down(rl.KEY_W):
            self.dy = 1 * self.speed
        elif pr.is_key_down(rl.KEY_DOWN) or pr.is_key_down(rl.KEY_D):
            self.dy = -1 * self.speed
        else:
            self.dx = 0
            self.dy = 0

        # update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy

    def update_mouse(self):
        mouse = pr.get_mouse_position()
        if (
            mouse.x >= 0
            and mouse.x <= self.width
            and mouse.y >= 0
            and mouse.y <= self.height
        ):
            if mouse.x > self.width * 0.95:
                self.dx = -1 * self.speed  # move in opposite direction
            elif mouse.x < self.width * 0.05:
                self.dx = self.speed
            else:
                self.dx = 0

            if mouse.y > self.height * 0.95:
                self.dy = -1 * self.speed  # move in opposite direction
            elif mouse.y < self.height * 0.05:
                self.dy = self.speed
            else:
                self.dy = 0
        else:
            self.dx = 0
            self.dy = 0

        # update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy
