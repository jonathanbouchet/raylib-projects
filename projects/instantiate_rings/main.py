import pyray as pr
from sprite import Sprite
import random
import settings as setting


class Game:
    def __init__(self) -> None:
        pr.init_window(setting.WINDOW_WIDTH, setting.WINDOW_HEIGHT, "game")
        pr.set_target_fps(setting.TARGET_FPS)
        self.rings: list[Sprite] = []

    def get_num_objects(self) -> int:
        return len(self.rings)

    def update(self, dt) -> None:
        [r.update(dt) for r in self.rings]

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        [r.draw() for r in self.rings]
        pr.draw_fps(0, 0)
        pr.draw_text(f"RINGS {len(self.rings)}", 0, 20, 20, pr.DARKGREEN)
        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            # input
            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                player_pos: pr.Vector2 = pr.get_mouse_position()
                self.rings.append(
                    Sprite(
                        player_pos,  # instantiate the ring where the mouse is clicked
                        pr.Vector2(
                            random.uniform(-1, 1), random.uniform(-1, 1)
                        ),  # random direction
                        random.randint(400, 600),  # random speed in [400, 600]
                        random.randint(10, 15),  # random inner radius
                        random.randint(20, 40),  # random outer radius
                        random.choice(setting.COLORS),  # random color
                    )
                )
                print(self.rings[-1])

            # update
            dt = pr.get_frame_time()
            self.update(dt)

            # drawing
            self.draw()

        pr.close_window()


if __name__ == "__main__":
    game = Game()
    game.run()
