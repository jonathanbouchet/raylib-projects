import random
import pyray as pr
from custom_timer import Timer

class Sprite:
    def __init__(self, position: pr.Vector2, size: pr.Vector2):
        self.position = position
        self.size = size
        self.color= pr.WHITE

    def randomize_color(self) -> None:
        self.color = random.choice([pr.RED, pr.BLUE, pr.GREEN, pr.YELLOW, pr.PINK])

    def draw(self) -> None:
        pr.draw_rectangle_v(self.position, self.size, self.color)

width, height = 600, 600

pr.init_window(width, height, "timer")
pr.set_target_fps(60)

sprite = Sprite(position=pr.Vector2(width//2 - 20, height//2 - 50), size=pr.Vector2(40, 100))
timer = Timer(duration=1, repeat=True, autostart=True, func=sprite.randomize_color)

while not pr.window_should_close():
    # logic here
    timer.update()

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    sprite.draw()
    pr.draw_fps(0,0)
    pr.draw_text(f"{str(int(pr.get_time()))}",0, 20, 20, pr.GREEN)
    pr.end_drawing()

pr.close_window()
