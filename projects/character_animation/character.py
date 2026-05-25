from enum import Enum
import pyray as pr
import raylib as rl


class States(Enum):
    IDLE = 0
    WALKING = 1
    JUMPING = 2


class BaseSprite:
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: int,
    ) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.speed: int = speed
        self.state: States = States.IDLE

    def update(self, dt: float, other: pr.Rectangle) -> None:
        self.move(dt=dt, other=other)

    def move(self, dt: float, other: pr.Rectangle) -> None:
        self.direction.x = int(pr.is_key_down(rl.KEY_RIGHT)) - int(
            pr.is_key_down(rl.KEY_LEFT)
        )
        self.direction.y = int(pr.is_key_down(rl.KEY_DOWN)) - int(
            pr.is_key_down(rl.KEY_UP)
        )
        self.position = pr.vector2_add(
            self.position,
            pr.vector2_scale(pr.vector2_scale(self.direction, self.speed), dt),
        )

    def draw(self, dt: float) -> None:
        pass

    def get_position(self) -> pr.Vector2:
        return self.position

    def get_state(self) -> States:
        return self.state

    def set_state(self):
        if self.is_grounded:
            if self.direction.x == 0 and self.direction.y == 0:
                self.state = States.IDLE
            elif self.direction.x != 0:
                self.state = States.WALKING
        else:
            self.state = States.JUMPING


class Sprite(BaseSprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: float,
        width: int,
        height: int,
        color: pr.Color,
    ) -> None:
        super().__init__(position=position, direction=direction, speed=speed)
        self.width: int = width
        self.height: int = height
        self.color: pr.Color = color

        # Physics state
        self.vy: float = 0.0  # vertical velocity (px/s)
        self.gravity: float = 1500.0  # gravity (px/s^2) — tune to taste
        self.jump_speed: float = 500.0  # initial jump impulse (px/s)
        self.is_grounded: bool = False

    def get_rectangle(self) -> pr.Rectangle:
        return pr.Rectangle(self.position.x, self.position.y, self.width, self.height)

    def check_collision(self, other: pr.Rectangle) -> bool:
        return pr.check_collision_recs(self.get_rectangle(), other)

    def move(self, dt: float, other: pr.Rectangle) -> None:
        # Horizontal input & move
        self.direction.x = int(pr.is_key_down(rl.KEY_RIGHT)) - int(
            pr.is_key_down(rl.KEY_LEFT)
        )
        self.position.x += self.direction.x * self.speed * dt

        # Jump input (use is_key_pressed for single press)
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
            if self.vy >= 0 and self.position.y + self.height > other.y:
                self.position.y = other.y - self.height
                self.vy = 0.0
                self.is_grounded = True
            else:
                # Basic fallback: prevent penetrating from below (optional improvement)
                self.position.y = other.y + other.height
                self.vy = 0.0
                self.is_grounded = False
        else:
            self.is_grounded = False

        self.set_state()

    def draw(self, dt: float) -> None:
        pr.draw_rectangle_v(
            self.position, pr.Vector2(self.width, self.height), self.color
        )


class AnimatedSprite(BaseSprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: int,
        textures: dict[str, list[pr.Texture2D]],
    ) -> None:
        self.position: pr.Vector2 = position
        self.direction: pr.Vector2 = direction
        self.speed: int = speed
        self.animation_index: int = 0
        self.state: States = States.IDLE
        self.all_textures: dict[str, list[pr.Texture2D]] = textures
        self.idle_textures: list[pr.Texture2D] = self.all_textures.get("idle")
        self.run_textures: list[pr.Texture2D] = self.all_textures.get("run")

    def draw(self, dt: float) -> None:
        if self.direction.x == 0 and self.direction.y == 0:
            self.state = States.IDLE
            self.animation_index += len(self.idle_textures) * dt
            pr.draw_texture_v(
                self.idle_textures[int(self.animation_index % len(self.idle_textures))],
                self.position,
                pr.WHITE,
            )
        else:
            self.state = States.WALKING
            self.animation_index += len(self.run_textures) * dt
            pr.draw_texture_v(
                self.run_textures[int(self.animation_index % len(self.run_textures))],
                self.position,
                pr.WHITE,
            )
