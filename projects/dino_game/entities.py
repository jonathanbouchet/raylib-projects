import random
from pathlib import Path
import pyray as pr
import raylib as rl

THIS_DIR = (Path(__file__).parent / "assets").resolve()


class Sprite:
    def __init__(
        self,
        position: pr.Vector2,
        texture: pr.Texture,
        color: pr.Color,
        debug_color: pr.Color,
    ):
        self.position = position
        self.texture = texture
        self.color = color
        self.debug_color = debug_color

    def get_rectangle(self) -> pr.Rectangle:
        return pr.Rectangle(
            self.position.x, self.position.y, self.texture.width, self.texture.height
        )

    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pr.draw_texture_v(self.texture, self.position, self.color)
        pr.draw_rectangle_lines(
            int(self.position.x),
            int(self.position.y),
            int(self.texture.width),
            int(self.texture.height),
            self.debug_color,
        )


class Player(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        texture: pr.Texture,
        color: pr.Color,
        debug_color: pr.Color,
    ):
        super().__init__(
            position=position, texture=texture, color=color, debug_color=debug_color
        )
        # Physics state
        self.vy: float = 0.0  # vertical velocity (px/s)
        self.gravity: float = 1500.0  # gravity (px/s^2) — tune to taste
        self.jump_speed: float = 500.0  # initial jump impulse (px/s)
        self.is_grounded: bool = False
        self.dead = False

    def update(self, dt: float, other: pr.Rectangle) -> None:
        self.move(dt=dt, other=other)

    def check_collision(self, other: pr.Rectangle) -> bool:
        return pr.check_collision_recs(self.get_rectangle(), other)

    def check_collisions_enemies(self, enemies: list[pr.Rectangle]):
        for enemy in enemies:
            # print(f"{enemy.width}, {enemy.height}, {enemy.x, enemy.y}")
            if pr.check_collision_recs(self.get_rectangle(), enemy):
                print(f"{enemy.width}, {enemy.height}, {type(enemy)}")
                print("COLLISION")
                dead_texture = pr.load_texture("assets/dino/dino_dead_64x64.png")
                self.texture = dead_texture
                self.dead = True

    def move(self, dt: float, other: pr.Rectangle):
        if pr.is_key_pressed(rl.KEY_SPACE) and self.is_grounded:
            self.vy = -self.jump_speed
            self.is_grounded = False

        # Apply gravity
        self.vy += self.gravity * dt

        # Integrate vertical velocity
        self.position.y += self.vy * dt

        # Simple collision resolution (vertical only)
        if self.check_collision(other):
            # If we hit the platform from above, snap on top and stop vertical velocity
            if self.vy >= 0 and self.position.y + self.texture.height > other.y:
                self.position.y = other.y - self.texture.height
                self.vy = 0.0
                self.is_grounded = True
            else:
                # Basic fallback: prevent penetrating from below (optional improvement)
                self.position.y = other.y + other.tecture.height
                self.vy = 0.0
                self.is_grounded = False
        else:
            self.is_grounded = False


class Enemy(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        texture: pr.Texture,
        color: pr.Color,
        speed: float,
        scale: float,
        debug_color: pr.Color,
    ):
        super().__init__(
            position=position, texture=texture, color=color, debug_color=debug_color
        )
        self.speed = speed
        self.direction = pr.Vector2(-1, 0)
        self.scale = scale
        self.disable = False

    # tuning because rectangle from sprite is too wide
    def get_rectangle(self) -> pr.Rectangle:
        return pr.Rectangle(
            self.position.x, self.position.y, self.texture.width, self.texture.height
        )

    def update(self, dt: float) -> None:
        # update velocity
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        if self.position.x < 0:
            self.disable = True

    def draw(self) -> None:
        # reposition the texture after scaling, if necessary
        tmp_pos = pr.Vector2(
            self.position.x, self.position.y - (self.scale - 1) * self.texture.height
        )
        pr.draw_texture_ex(self.texture, tmp_pos, 0, self.scale, self.color)
        pr.draw_rectangle_lines(
            int(tmp_pos.x),
            int(tmp_pos.y),
            int(self.texture.width * self.scale),
            int(self.texture.height * self.scale),
            self.debug_color,
        )