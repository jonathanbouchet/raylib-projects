from enum import Enum
import pyray as pr
from .asteroid import Asteroid
from .player import Player
from .scorer import Scorer


class GameStates(Enum):
    INIT = 0  # start of the app
    RUN = 1  # game is running
    PAUSE = 2  # game is paused
    OVER = 3  # game is over


class GameManager:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.state = GameStates.INIT
        self.scorer = Scorer(number_enemies=10, remaining_time=60)
        self.asteroid = Asteroid(
            position=pr.Vector2(self.width / 2, self.height / 2),
            size=pr.Vector2(20, 20),
            direction=pr.Vector2(10, 10),
            speed=0,
            angular_speed=90,
            scale=1,
            color=pr.WHITE,
            debug=False,
            debug_color=pr.YELLOW,
        )
        self.player = Player(
            position=pr.Vector2(self.width / 2, 500),
            window_size=pr.Vector2(self.width, self.height),
            v1=pr.Vector3(self.width / 2 - 15, 100 + self.height / 2, 0),  # bottom left
            v2=pr.Vector3(
                self.width / 2 + 15, 100 + self.height / 2, 0
            ),  # bottom right
            v3=pr.Vector3(self.width / 2, 100 + self.height / 2 - 40, 0),  # top center,
            speed=10,
            angular_speed=150,
            color=pr.WHITE,
            scale=1.0,
            debug=False,
            debug_color=pr.BLUE,
        )

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

    def update(self) -> None:
        # logic
        dt = pr.get_frame_time()
        # update player
        self.player.update(dt=dt)
        # update asteroids
        self.asteroid.update(dt=dt)
        # update lasers
        if len(self.player.lasers) > 0:
            _ = [l.update(dt=dt) for l in self.player.lasers]


    async def run(self) -> None:
        self.state = GameStates.RUN
        while not pr.window_should_close():
            self.update()
            self.draw()

    def draw_debug(self) -> None:
        pr.draw_fps(0, 0)
        pr.draw_text(f"{self.state}", 0, 20, 20, pr.DARKGREEN)
        pr.draw_text(f"ENEMIES: {self.scorer.number_enemies}", 0, 40, 20, pr.DARKGREEN)
        pr.draw_text(f"TIME: {self.scorer.remaining_time}", 0, 60, 20, pr.DARKGREEN)
        pr.draw_text(f"LASERS: {len(self.player.lasers)}", 0, 80, 20, pr.DARKGREEN)
        pr.draw_line(0, self.height // 2, self.width, self.height // 2, pr.RED)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)

    def draw(self) -> None:
        dt = pr.get_frame_time()
        pr.begin_drawing()
        pr.clear_background(self.background_color)
        # draw player
        self.player.draw(dt=dt)
        # draw asteroids
        self.asteroid.draw(dt=dt)
        # draw lasers
        _ = [laser.draw() for laser in self.player.lasers]
        self.draw_debug()
        pr.end_drawing()

    def end(self) -> None:
        pr.close_window()
