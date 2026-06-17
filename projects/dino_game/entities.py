from enum import Enum
from pathlib import Path
import pyray as pr
import raylib as rl

THIS_DIR = (Path(__file__).parent / "assets").resolve()


class States(Enum):
    IDLE = 0
    WALKING = 1
    JUMPING = 2
    DEAD = 3


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

    def move(self) -> None:
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
        running_textures_path: list[str],
        dead_texture_path: str,
        color: pr.Color,
        debug_color: pr.Color,
    ):
        super().__init__(
            position=position, texture=texture, color=color, debug_color=debug_color
        )
        # other textures
        self.running_textures_path = running_textures_path
        self.running_textures = [pr.load_texture(x) for x in self.running_textures_path]
        self.dead_texture_path = dead_texture_path
        self.dead_texture = pr.load_texture(self.dead_texture_path)
        self.animation_index: int = 0
        # Physics state
        self.vy: float = 0.0  # vertical velocity (px/s)
        self.gravity: float = 1500.0  # gravity (px/s^2) — tune to taste
        self.jump_speed: float = 500.0  # initial jump impulse (px/s)
        self.is_grounded: bool = False
        self.state = States.IDLE

    # def load_running_textures(self) -> None:
    #     self.running_textures = [pr.load_texture(x) for x in self.running_textures_path]

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
                self.state = States.DEAD
                # dead_texture = pr.load_texture("assets/dino/dino_dead_64x64.png")
                self.texture = self.dead_texture
                # self.dead = True

    def move(self, dt: float, other: pr.Rectangle):
        # update player state
        self.state = States.WALKING
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

    def draw(self, dt: float) -> None:
        if self.state != States.DEAD:
            self.animation_index += len(self.running_textures) * (6 * dt)
            pr.draw_texture_v(
                self.running_textures[
                    int(self.animation_index % len(self.running_textures))
                ],
                self.position,
                self.color,
            )
            pr.draw_rectangle_lines(
                int(self.position.x),
                int(self.position.y),
                int(
                    self.running_textures[
                        int(self.animation_index % len(self.running_textures))
                    ].width
                ),
                int(
                    self.running_textures[
                        int(self.animation_index % len(self.running_textures))
                    ].height
                ),
                self.debug_color,
            )
        else:
            pr.draw_texture_v(self.texture, self.position, self.color)

        pr.draw_rectangle_lines(
            int(self.position.x),
            int(self.position.y),
            int(self.texture.width),
            int(self.texture.height),
            self.debug_color,
        )
        pr.draw_text(
            str(self.state),
            int(self.position.x),
            int(self.position.y) - 10,
            10,
            self.debug_color,
        )

    def get_state(self) -> States:
        return self.state


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

class Cloud(Sprite):
    def __init__(
        self,
        position: pr.Vector2,
        texture: pr.Texture,
        speed: float,
        color: pr.Color,
        debug_color: pr.Color,
    ):
        super().__init__(
            position=position, texture=texture, color=color, debug_color=debug_color
        )
        self.speed = speed
        self.direction = pr.Vector2(-1, 0)
        self.disable = False

    def update(self, dt: float) -> None:
        # update velocity
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        if self.position.x < 0:
            self.disable = True
