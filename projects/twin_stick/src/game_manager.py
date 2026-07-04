from pathlib import Path
import random
import PolygonCollision
import pyray as pr
import raylib as rl
from .asteroid import Asteroid
from .player import Player
from .scorer import Scorer
from .resource_manager import ResourceManager
from .timer import Timer
from .states import GameStates, WaveStates
from .explosion import Explosion

THIS_DIR = (Path(__file__).parent.parent / "assets").resolve()


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
        # self.use_shader: str = self.resources_manager.game_data().get("use_shader")
        self.debug: bool = self.resources_manager.game_data().get("debug")

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
                speed=self.resources_manager.asteroid_data().get("speed"),
                window_borders=pr.Vector2(self.width, self.height),
                size=pr.Vector2(
                    self.resources_manager.asteroid_data().get("size")[0],
                    self.resources_manager.asteroid_data().get("size")[1],
                ),
                color=tuple(self.resources_manager.asteroid_data().get("color")),
            )
            for _ in range(self.scorer.number_enemies)
        ]

        self.asteroids_wave_timer = Timer(
            duration=self.resources_manager.scorer_data().get("remaining_time"),
            repeat=False,
            autostart=False,
            func=self.create_asteroid_wave,
        )

        # explosions
        self.explosions: list[Explosion] = []

    def load_sound_effects(self) -> None:
        """needs to be done AFTER raylib is initialized"""
        # sound effect
        self.laser_sound: pr.Sound = pr.load_sound(
            f"{THIS_DIR}/{self.resources_manager.sound_effect_data().get('laser')}"
        )
        self.explosion_sound: pr.Sound = pr.load_sound(
            f"{THIS_DIR}/{self.resources_manager.sound_effect_data().get('explosion')}"
        )

    def init(self) -> None:
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        pr.init_audio_device()
        self.load_sound_effects()
        self.player.load_laser_sound(self.laser_sound)
        self.frame_counter: int = 0
        self.state = GameStates.INIT
        # load shader
        self.target = pr.load_render_texture(
            pr.get_screen_width(), pr.get_screen_height()
        )
        self.shader = pr.load_shader(pr.ffi.NULL, f"{THIS_DIR}/{self.shader_bloom}")

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
                    speed=self.resources_manager.asteroid_data().get("speed"),
                    window_borders=pr.Vector2(self.width, self.height),
                    size=pr.Vector2(
                        self.resources_manager.asteroid_data().get("size")[0],
                        self.resources_manager.asteroid_data().get("size")[1],
                    ),
                    color=tuple(self.resources_manager.asteroid_data().get("color")),
                )
                for _ in range(self.scorer.number_enemies)
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
                    # print(f"COLLISION between :{asteroid_polygon} and {laser_polygon}")
                    asteroid.discard = True  # checking if discard works ; the asteroid should not be rendered (--> YES, it works)
                    laser.discard = True  # checking if discard works ; the laser should not be rendered (--> YES, it works)
                    # increment player score
                    self.scorer.player_has_shot += 1
                    # create an explosion
                    self.explosions.append(
                        Explosion(
                            position=asteroid.position,
                            max_size=pr.Vector2(
                                self.resources_manager.explosion_data().get("size")[0],
                                self.resources_manager.explosion_data().get("size")[1],
                            ),
                            children=self.resources_manager.explosion_data().get(
                                "children"
                            ),
                            speed=self.resources_manager.explosion_data().get("speed"),
                            lifetime=self.resources_manager.explosion_data().get(
                                "lifetime"
                            ),
                            color=tuple(
                                self.resources_manager.explosion_data().get("color")
                            ),
                        )
                    )
                    # play explosion sound effect
                    pr.play_sound(self.explosion_sound)
                    self.discard_asteroids()
                    self.discard_lasers()

    def update(self) -> None:
        # logic
        dt = pr.get_frame_time()
        self.frame_counter += 1

        # update player
        self.player.update(dt=dt)

        # update asteroids
        _ = [asteroid.update(dt=dt) for asteroid in self.asteroids]

        # update lasers
        if len(self.player.lasers) > 0:
            _ = [laser.update(dt=dt) for laser in self.player.lasers]

        # check laser-asteroid collision
        self.check_collisions()

        # update explosions
        _ = [explosion.update(dt=dt) for explosion in self.explosions]

        # update scorer
        if self.scorer.update(
            current_wave_number_enemies=len(self.asteroids),
            current_wave_time=self.asteroids_wave_timer.get_wave_time(
                wave_state=self.scorer.wave_state
            ),
        ) in [WaveStates.SUCCESS, WaveStates.FAIL]:
            self.asteroids_wave_timer.deactivate()
        else:
            # update asteroid timer
            self.asteroids_wave_timer.update()

    def draw_init(self) -> None:
        # draw start screen
        self.draw_score()
        enter_triggered = pr.is_key_pressed(rl.KEY_ENTER)
        if (
            pr.gui_button(
                pr.Rectangle(self.width / 2 - 150, self.height / 2 - 20, 300, 60),
                "Start the game\nleft, top, right arrow to control the ship\nspace to shoot",
            )
            or enter_triggered
        ):
            self.state = GameStates.RUN
            self.asteroids_wave_timer.activate()
            self.scorer.wave_state = WaveStates.ONGOING

        # self.draw_blanck()
        if self.debug:
            self.draw_debug()

    def draw_sucess_wave(self) -> None:
        self.draw_score()
        if self.state == GameStates.PAUSE:
            res = pr.gui_message_box(
                pr.Rectangle(self.width // 2 - 150, self.height // 2 - 40, 300, 80),
                "",
                "WAVE SUCCESSFULL, CHOOSE :",
                "ASTEROIDS INCREASE;TIME DECREASES",
            )
            if res > 0:
                current_remaining_time = self.scorer.remaining_time
                current_asteroids = self.scorer.original_number_enemies
                if res == 1:
                    self.scorer.next_wave(user_choice=1, current_asteroids=current_asteroids, current_remaining_time=current_remaining_time)
                elif res == 2:
                    self.scorer.next_wave(user_choice=2,current_asteroids=current_asteroids, current_remaining_time=current_remaining_time)

                # reset player current score:
                self.scorer.player_has_shot = 0
                self.asteroids_wave_timer.set_duration(self.scorer.remaining_time)
                self.asteroids_wave_timer.activate()
                self.create_asteroid_wave()
                self.state = GameStates.RUN
                self.scorer.wave_state = WaveStates.ONGOING

                self.draw_score()

    def fail_wave_screen(self) -> None:
        self.draw_score()
        enter_triggered = pr.is_key_pressed(rl.KEY_ENTER)
        if (
            pr.gui_button(
                pr.Rectangle(self.width / 2 - 100, self.height / 2 - 20, 200, 40),
                "WAVE FAILED, RESTART",
            )
            or enter_triggered
        ):
            # clear list of lasers
            self.asteroids = []
            # reset all
            self.scorer.player_has_shot = 0
            self.scorer.reset_score()
            self.asteroids_wave_timer.set_duration(self.scorer.remaining_time)
            self.asteroids_wave_timer.activate()
            self.create_asteroid_wave()
            self.state = GameStates.RUN
            self.scorer.wave_state = WaveStates.ONGOING

        # self.draw_blanck()
        if self.debug:
            self.draw_debug()

    async def run(self) -> None:
        while not pr.window_should_close():
            if (
                self.state == GameStates.RUN
                and self.scorer.wave_state == WaveStates.SUCCESS
                or self.state == GameStates.PAUSE
            ):
                self.state = GameStates.PAUSE
                self.draw_sucess_wave()

            if self.scorer.wave_state == WaveStates.FAIL:
                self.state = GameStates.OVER
                self.fail_wave_screen()

            if self.state == GameStates.RUN:
                self.update()
                self.draw()
            else:
                self.draw_blanck()
                if self.debug:
                    self.draw_debug()

            if self.state == GameStates.INIT:
                self.draw_init()

    def draw_score(self) -> None:
        # player UI
        pr.draw_text(f"WAVE {str(self.scorer.wave)}", 500, 0, 10, pr.RED)
        pr.draw_text(
            f"ASTEROIDS: {self.scorer.player_has_shot} / {self.scorer.original_number_enemies}",
            500,
            10,
            10,
            pr.RED,
        )
        pr.draw_text(f"TIME: {self.scorer.remaining_time}", 500, 20, 10, pr.RED)

    def draw_blanck(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        pr.end_drawing()

    def draw_debug(self) -> None:
        pr.draw_fps(0, 0)
        pr.draw_text(f"{self.state}", 0, 20, 20, pr.GREEN)
        pr.draw_text(
            f"ASTEROIDS: {self.scorer.number_enemies} TIME: {self.scorer.remaining_time}",
            0,
            40,
            20,
            pr.GREEN,
        )
        pr.draw_text(f"LASERS: {len(self.player.lasers)}", 0, 60, 20, pr.GREEN)
        pr.draw_text(
            f"{str(int(pr.get_time()))}, {self.frame_counter}", 0, 80, 20, pr.GREEN
        )
        pr.draw_text(
            f"WAVE: {str(self.scorer.wave)} {self.scorer.wave_state}",
            0,
            100,
            20,
            pr.GREEN,
        )
        pr.draw_line(0, self.height // 2, self.width, self.height // 2, pr.RED)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)

    def draw(self) -> None:
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

        # draw explosions
        _ = [explosion.draw() for explosion in self.explosions]

        # draw UI
        self.draw_score()

        if self.debug:
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

    def end(self) -> None:
        # if self.use_shader:
        pr.unload_render_texture(self.target)
        pr.unload_shader(self.shader)
        pr.close_audio_device()
        pr.close_window()
