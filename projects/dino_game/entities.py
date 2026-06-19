from enum import Enum
from pathlib import Path
import pyray as pr
import raylib as rl

THIS_DIR = (Path(__file__).parent / "assets").resolve()


class PlayerStates(Enum):
    IDLE = 0
    RUNNING = 1
    JUMPING = 2
    DEAD = 3


class StaticSprite:
    """base class for static texture"""

    def __init__(
        self, window_width: int, window_height: int, floor_y_pos: int, show_debug: bool
    ) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.floor_y_pos = floor_y_pos
        self.floor_rect = pr.Rectangle(
            0,
            self.window_height - self.floor_y_pos,
            self.window_width,
            self.window_height - self.floor_y_pos,
        )
        self.show_debug = show_debug

    def draw(self) -> None:
        # draw floor
        if self.show_debug:
            pr.draw_rectangle_rec(self.floor_rect, pr.YELLOW)
            pr.draw_line_v(
                pr.Vector2(0, self.window_height - self.floor_y_pos),
                pr.Vector2(self.window_width, self.window_height - self.floor_y_pos),
                pr.RED,
            )
        else:
            pr.draw_line_v(
                pr.Vector2(0, self.window_height - self.floor_y_pos),
                pr.Vector2(self.window_width, self.window_height - self.floor_y_pos),
                pr.BLACK,
            )


class Sprite:
    """base class for the textures used in the game"""

    def __init__(
        self,
        position: pr.Vector2,
        texture: pr.Texture,
        color: pr.Color,
        debug_color: pr.Color,
        show_debug: bool,
    ):
        self.position = position
        self.texture = texture
        self.color = color
        self.debug_color = debug_color
        self.show_debug = show_debug

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
        if self.show_debug:
            pr.draw_rectangle_lines(
                int(self.position.x),
                int(self.position.y),
                int(self.texture.width),
                int(self.texture.height),
                self.debug_color,
            )


class Player(Sprite):
    """player class"""

    def __init__(
        self,
        position: pr.Vector2,  # player position
        texture: pr.Texture,  # player idle texture
        running_textures_path: list[str],  # path to player running textures
        dead_texture_path: str,  # path to player dead texture
        color: pr.Color,  # player tint
        debug_color: pr.Color,  # player debug color
        show_debug: bool,  # flag to show player debug variables
    ):
        super().__init__(
            position=position,
            texture=texture,
            color=color,
            debug_color=debug_color,
            show_debug=show_debug,
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
        self.jump_speed: float = 600.0  # initial jump impulse (px/s)
        self.is_grounded: bool = False
        self.state = PlayerStates.IDLE

    def update(self, dt: float, other: pr.Rectangle) -> None:
        self.move(dt=dt, other=other)

    def check_collision(self, other: pr.Rectangle) -> bool:
        """check collision with floor"""
        return pr.check_collision_recs(self.get_rectangle(), other)

    def check_collisions_enemies(self, enemies: list[pr.Rectangle]):
        """chcekc collisions with enemies"""
        for enemy in enemies:
            # print(f"{enemy.width}, {enemy.height}, {enemy.x, enemy.y}")
            if pr.check_collision_recs(self.get_rectangle(), enemy):
                print(f"{enemy.width}, {enemy.height}, {type(enemy)}")
                print("COLLISION")
                self.state = PlayerStates.DEAD
                self.texture = self.dead_texture

    def move(self, dt: float, other: pr.Rectangle):
        # update player state
        self.state = PlayerStates.RUNNING
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
        """draw texture player"""
        if self.state == PlayerStates.RUNNING:
            self.animation_index += len(self.running_textures) * (6 * dt)
            pr.draw_texture_v(
                self.running_textures[
                    int(self.animation_index % len(self.running_textures))
                ],
                self.position,
                self.color,
            )
            if self.show_debug:
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
            # player is dead
            pr.draw_texture_v(self.texture, self.position, self.color)
        if self.show_debug:
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

    def get_state(self) -> PlayerStates:
        """return player state"""
        return self.state


class Enemy(Sprite):
    def __init__(
        self,
        position: pr.Vector2,  # position of the enemy
        texture: pr.Texture,  # texture of the enemy
        color: pr.Color,  # tint of the enemy
        speed: float,  # enemy's speed
        scale: float,  # enemy's texture scale
        debug_color: pr.Color,  # enemy debug color
        show_debug: bool,  # flag to show enemy's variables
    ):
        super().__init__(
            position=position,
            texture=texture,
            color=color,
            debug_color=debug_color,
            show_debug=show_debug,
        )
        self.speed = speed
        self.direction = pr.Vector2(-1, 0)
        self.scale = scale
        self.disable = False

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
        tmp_pos = pr.Vector2(
            self.position.x, self.position.y - (self.scale - 1) * self.texture.height
        )
        pr.draw_texture_ex(self.texture, tmp_pos, 0, self.scale, self.color)
        if self.show_debug:
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
        position: pr.Vector2,  # position of the cloud
        texture: pr.Texture,  # cloud's texture
        speed: float,  # cloud's texture
        screen_width: int,  # game screen width
        color: pr.Color,  # cloud's tint
        debug_color: pr.Color,  # cloud debug color
        show_debug: bool,  # flag to show debug variables
    ):
        super().__init__(
            position=position,
            texture=texture,
            color=color,
            debug_color=debug_color,
            show_debug=show_debug,
        )
        self.speed = speed
        self.direction = pr.Vector2(-1, 0)
        self.screen_width = screen_width
        self.disable = False

    def update(self, dt: float) -> None:
        # update velocity
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        # re-spawn clouds at the right of the screen
        if self.position.x - self.texture.width < 0:
            self.position.x = self.screen_width
