from enum import Enum
import pyray as pr
import raylib as rl


class States(Enum):
    IDLE = 0
    RUNNING = 1
    OTHER = 2


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

    def update(self, dt: float) -> None:
        self.move(dt=dt)

    def move(self, dt: float) -> None:
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

    def get_state(self) -> States:
        return self.state


class Sprite(BaseSprite):
    def __init__(
        self,
        position: pr.Vector2,
        direction: pr.Vector2,
        speed: int,
        width: int,
        height: int,
        color: pr.Color,
    ) -> None:
        super().__init__(position=position, direction=direction, speed=speed)
        self.width: int = width
        self.height: int = height
        self.color: pr.Color = color

    def draw(self, dt: float) -> None:
        """for a character based on Sprite, we expect a primitive shape to represnet the character, i.e rectangle

        :param dt: _description_
        :type dt: _type_
        :return: _description_
        :rtype: _type_
        """
        if self.direction.x == 0 and self.direction.y == 0:
            self.state = States.IDLE
            pr.draw_rectangle_v(
                self.position, pr.Vector2(self.width, self.height), self.color
            )
        else:
            self.state = States.RUNNING
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
            self.state = States.RUNNING
            self.animation_index += len(self.run_textures) * dt
            pr.draw_texture_v(
                self.run_textures[int(self.animation_index % len(self.run_textures))],
                self.position,
                pr.WHITE,
            )
