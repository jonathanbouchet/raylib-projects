import random
import PolygonCollision
from enum import Enum
import pyray as pr
from .asteroid import Asteroid
from .player import Player
from .scorer import Scorer
from .resource_manager import ResourceManager
from .timer import Timer


class GameStates(Enum):
    INIT = 0  # start of the app
    RUN = 1  # game is running
    PAUSE = 2  # game is paused
    OVER = 3  # game is over


class GameManager:
    def __init__(self, resources_manager) -> None:
        self.resources_manager: ResourceManager = resources_manager
        self.width: int = self.resources_manager.game_data().get("width")
        self.height: int = self.resources_manager.game_data().get("width")
        self.fps_target: int = self.resources_manager.game_data().get("fps")
        self.background_color: pr.Color = tuple(
            self.resources_manager.game_data().get("background_color")
        )
        self.name: str = self.resources_manager.game_data().get("name")
        self.state = GameStates.INIT
        self.scorer = Scorer(number_enemies=10, remaining_time=60)
        self.frame_counter: int = 0
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
            laser_data=self.resources_manager.laser_data()
        )
        self.asteroids_wave_timer = Timer(
            duration=5,  # testing: create wave of 2 asteroids every 2 seconds
            repeat=True,
            autostart=True,
            func=self.create_asteroid_wave,
        )
        self.asteroids: list[Asteroid] = []

    def init(self) -> None:
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

    def create_asteroid_wave(self) -> None:
        self.asteroids.extend(
            [
                Asteroid(
                    position=pr.Vector2(
                        random.randint(0, self.width), random.randint(0, self.height)
                    ),
                    direction=pr.Vector2(
                        random.randint(-100, 100), random.randint(-100, 100)
                    ),
                    window_borders=pr.Vector2(self.width, self.height),
                    size=pr.Vector2(20, 20),
                    color=pr.WHITE,
                )
                for _ in range(2)
            ]
        )

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
                    asteroid.discard = True  # checking if discard works ; the laser should not be rendered (--> YES, it works)

    def update(self) -> None:
        # logic
        dt = pr.get_frame_time()
        self.frame_counter += 1
        self.asteroids_wave_timer.update()

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
        self.state = GameStates.RUN
        while not pr.window_should_close():
            self.update()
            self.draw()

    def draw_debug(self) -> None:
        pr.draw_fps(0, 0)
        pr.draw_text(f"{self.state}", 0, 20, 20, pr.DARKGREEN)
        pr.draw_text(f"ASTEROIDS: {len(self.asteroids)}", 0, 40, 20, pr.DARKGREEN)
        pr.draw_text(f"TIME: {self.scorer.remaining_time}", 0, 60, 20, pr.DARKGREEN)
        pr.draw_text(f"LASERS: {len(self.player.lasers)}", 0, 80, 20, pr.DARKGREEN)
        pr.draw_text(
            f"{str(int(pr.get_time()))}, {self.frame_counter}", 0, 100, 20, pr.GREEN
        )
        pr.draw_line(0, self.height // 2, self.width, self.height // 2, pr.RED)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)

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
        pr.close_window()
