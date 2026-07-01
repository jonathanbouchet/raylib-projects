from pathlib import Path
import random
import PolygonCollision
from enum import Enum
import pyray as pr
from .asteroid import Asteroid
from .player import Player
from .scorer import Scorer
from .resource_manager import ResourceManager
from .timer import Timer

THIS_DIR = (Path(__file__).parent.parent / "assets").resolve()


class GameStates(Enum):
    INIT = 0  # start of the app
    RUN = 1  # game is running
    PAUSE = 2  # game is paused
    OVER = 3  # game is over


class GameManager:
    def __init__(self, resources_manager) -> None:
        self.resources_manager: ResourceManager = resources_manager

        # generalities
        self.width: int = self.resources_manager.game_data().get("width")
        self.height: int = self.resources_manager.game_data().get("height")
        self.fps_target: int = self.resources_manager.game_data().get("fps")
        self.background_color: pr.Color = tuple(
            self.resources_manager.game_data().get("background_color")
        )
        self.name: str = self.resources_manager.game_data().get("name")
        self.use_shader: str = self.resources_manager.game_data().get("use_shader")

        # scorer
        self.scorer = Scorer(
            number_enemies=self.resources_manager.scorer_data().get("number_enemies"),
            remaining_time=self.resources_manager.scorer_data().get("remaining_time"),
        )

        # shader
        self.shader_bloom = self.resources_manager.shaders().get("bloom")

        # player
        self.player = Player(
            position=pr.Vector2(
                self.resources_manager.player_data().get("position")[0],
                self.resources_manager.player_data().get("position")[1],
            ),
            window_borders=pr.Vector2(self.width, self.height),
            v1=pr.Vector3(self.width / 2 - 15, 100 + self.height / 2, 0),  # bottom left
            v2=pr.Vector3(
                self.width / 2 + 15, 100 + self.height / 2, 0
            ),  # bottom right
            v3=pr.Vector3(self.width / 2, 100 + self.height / 2 - 40, 0),  # top center,
            speed=self.resources_manager.player_data().get("speed"),
            angular_speed=self.resources_manager.player_data().get("angular_speed"),
            color=tuple(self.resources_manager.player_data().get("color")),
            scale=self.resources_manager.player_data().get("scale"),
            debug=self.resources_manager.player_data().get("debug"),
            debug_color=tuple(self.resources_manager.player_data().get("debug_color")),
            shoot_cooldown=self.resources_manager.player_data().get("shoot_cooldown"),
            shoot_timer=self.resources_manager.player_data().get("shoot_timer"),
            laser_data=self.resources_manager.laser_data(),
        )

        # asteroids
        self.asteroids: list[Asteroid] = [
            Asteroid(
                position=pr.Vector2(
                    random.randint(
                        self.resources_manager.asteroid_data().get("position")[0],
                        self.resources_manager.asteroid_data().get("position")[1],
                    ),
                    random.randint(
                        self.resources_manager.asteroid_data().get("position")[0],
                        self.resources_manager.asteroid_data().get("position")[1],
                    ),
                ),
                direction=pr.Vector2(
                    random.randint(-100, 100), random.randint(-100, 100)
                ),
                window_borders=pr.Vector2(self.width, self.height),
                size=pr.Vector2(
                    self.resources_manager.asteroid_data().get("size")[0],
                    self.resources_manager.asteroid_data().get("size")[1],
                ),
                color=tuple(self.resources_manager.asteroid_data().get("color")),
            )
            for _ in range(self.resources_manager.scorer_data().get("number_enemies"))
        ]

        self.asteroids_wave_timer = Timer(
            duration=self.resources_manager.timer_game_data().get("duration"),
            repeat=True,
            autostart=True,
            func=self.create_asteroid_wave,
        )

    def init(self) -> None:
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        self.frame_counter: int = 0
        self.state = GameStates.INIT
        # load shader
        if self.use_shader:
            self.target = pr.load_render_texture(
                pr.get_screen_width(), pr.get_screen_height()
            )
            self.shader = pr.load_shader(
                pr.ffi.NULL, f"{THIS_DIR}/{self.shader_bloom}"
            )  # Point to your downloaded shader file

    def create_asteroid_wave(self) -> None:
        self.asteroids.extend(
            [
                Asteroid(
                    position=pr.Vector2(
                        random.randint(
                            self.resources_manager.asteroid_data().get("position")[0],
                            self.resources_manager.asteroid_data().get("position")[1],
                        ),
                        random.randint(
                            self.resources_manager.asteroid_data().get("position")[0],
                            self.resources_manager.asteroid_data().get("position")[1],
                        ),
                    ),
                    direction=pr.Vector2(
                        random.randint(-100, 100), random.randint(-100, 100)
                    ),
                    window_borders=pr.Vector2(self.width, self.height),
                    size=pr.Vector2(
                        self.resources_manager.asteroid_data().get("size")[0],
                        self.resources_manager.asteroid_data().get("size")[1],
                    ),
                    color=tuple(self.resources_manager.asteroid_data().get("color")),
                )
                for _ in range(2)
            ]
        )

    def discard_asteroids(self) -> None:
        self.asteroids = [
            asteroid for asteroid in self.asteroids if not asteroid.discard
        ]

    def discard_lasers(self) -> None:
        self.player.lasers = [
            laser for laser in self.player.lasers if not laser.discard
        ]

    def check_collisions(self) -> None:
        """check any collision between asteroids and lasers"""
        for laser in self.player.lasers:
            for asteroid in self.asteroids:
                # pylygoncollision
                asteroid_rect = asteroid.get_rectangle()
                laser_rect = laser.get_rectangle()
                asteroid_polygon = PolygonCollision.shape.Shape(
                    vertices=[tuple([r.x, r.y]) for r in asteroid_rect]
                )
                laser_polygon = PolygonCollision.shape.Shape(
                    vertices=[tuple([r.x, r.y]) for r in laser_rect]
                )
                if asteroid_polygon.collide(laser_polygon):
                    print(f"COLLISION between :{asteroid_polygon} and {laser_polygon}")
                    asteroid.discard = True  # checking if discard works ; the asteroid should not be rendered (--> YES, it works)
                    laser.discard = True  # checking if discard works ; the laser should not be rendered (--> YES, it works)
                    self.discard_asteroids()
                    self.discard_lasers()
                    # self.scorer.number_enemies -= 1

    def update(self) -> None:
        # logic
        dt = pr.get_frame_time()
        self.frame_counter += 1
        # self.asteroids_wave_timer.update()

        # update player
        self.player.update(dt=dt)

        # update asteroids
        _ = [asteroid.update(dt=dt) for asteroid in self.asteroids]

        # update lasers
        if len(self.player.lasers) > 0:
            _ = [laser.update(dt=dt) for laser in self.player.lasers]

        # check laser-asteroid collision
        self.check_collisions()

    async def run(self) -> None:
        while not pr.window_should_close():
            # draw start screen
            if (
                pr.gui_button(
                    pr.Rectangle(self.width / 2 - 100, self.height / 2 - 20, 200, 40),
                    "Start the game",
                )
                or self.state == GameStates.RUN
            ):
                self.state = GameStates.RUN
                self.update()
                if self.use_shader:
                    self.draw_with_shader()
                else:
                    self.draw()
            else:
                self.draw_blanck()
                self.draw_debug()

    def draw_blanck(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        pr.end_drawing()

    def draw_debug(self) -> None:
        pr.draw_fps(0, 0)
        pr.draw_text(f"{self.state}", 0, 20, 20, pr.GREEN)
        pr.draw_text(f"ASTEROIDS: {len(self.asteroids)}", 0, 40, 20, pr.GREEN)
        pr.draw_text(f"TIME: {self.scorer.remaining_time}", 0, 60, 20, pr.GREEN)
        pr.draw_text(f"LASERS: {len(self.player.lasers)}", 0, 80, 20, pr.GREEN)
        pr.draw_text(
            f"{str(int(pr.get_time()))}, {self.frame_counter}", 0, 100, 20, pr.GREEN
        )
        pr.draw_text(f"USE SHADER: {str(self.use_shader)}", 0, 120, 20, pr.GREEN)
        pr.draw_text(f"WAVE: {str(self.scorer.wave)}", 0, 140, 20, pr.GREEN)
        pr.draw_line(0, self.height // 2, self.width, self.height // 2, pr.RED)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)

    def draw_with_shader(self) -> None:
        dt = pr.get_frame_time()
        # --- RENDER SCENE TO TEXTURE ---
        pr.begin_texture_mode(self.target)

        pr.begin_drawing()
        pr.clear_background(self.background_color)

        # draw player
        self.player.draw(dt=dt)

        # draw asteroids
        _ = [
            asteroid.draw(dt=dt) for asteroid in self.asteroids if not asteroid.discard
        ]

        # draw lasers
        _ = [laser.draw() for laser in self.player.lasers if not laser.discard]

        self.draw_debug()
        pr.end_texture_mode()

        # --- DRAW AND APPLY GLOW ---
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_shader_mode(self.shader)
        # Draw the rendered texture with the bloom shader applied
        pr.draw_texture_rec(
            self.target.texture,
            pr.Rectangle(0, 0, pr.get_screen_width(), -pr.get_screen_height()),
            pr.Vector2(0, 0),
            pr.WHITE,
        )
        pr.end_shader_mode()
        pr.end_drawing()

    def draw(self) -> None:
        dt = pr.get_frame_time()

        pr.begin_drawing()
        pr.clear_background(self.background_color)

        # draw player
        self.player.draw(dt=dt)

        # draw asteroids
        _ = [
            asteroid.draw(dt=dt) for asteroid in self.asteroids if not asteroid.discard
        ]

        # draw lasers
        _ = [laser.draw() for laser in self.player.lasers if not laser.discard]

        self.draw_debug()
        pr.end_drawing()

    def end(self) -> None:
        if self.use_shader:
            pr.unload_render_texture(self.target)
            pr.unload_shader(self.shader)
        pr.close_window()
