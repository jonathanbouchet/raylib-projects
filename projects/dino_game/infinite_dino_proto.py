import random
import pyray as pr
width, height = 600, 400
floor_y_pos = 100
block_y_spawn = [100, 300]

class Block:
    def __init__(self, position: pr.Vector2, size: pr.Vector2, speed: float) -> None:
        self.position = position
        self.speed = speed
        self.size = size#pr.Vector2(10, random.randint(10,50))
        self.direction = pr.Vector2(-1, 0)
        self.disable = False

    def update(self, dt: float) -> None:
        # update velocity
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        if self.position.x < 0:
            self.disable = True

    def draw(self, dt):
        pr.draw_rectangle_v(self.position, self.size, pr.WHITE)


pr.init_window(width, height, "app")
pr.set_target_fps(60)
block_list: list[Block] = []

run_time = 0
frame_counter = 0
block_spawn_frame: bool = False

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    frame_counter += 1
    run_time = pr.get_time()
    if frame_counter % 60 == 0: # spawn a block every frame
        if random.random() < 0.95:# and not block_y_spawn:
            s = pr.Vector2(10, random.randint(10, 40))
            print(f"{s.x}, {s.y}")
            block_list.append(
                Block(
                    position=pr.Vector2(width, random.randint(200, 300 - int(s.y) - 10)), 
                    size=s,
                    speed = 100))#random.randint(50, 100)))
            block_y_spawn = True
    # updates all blocks
    _ = [block.update(dt=dt) for block in block_list]
    # clean list of blocks
    block_list = [x for x in block_list if x.position.x>0]
    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    # draw block
    # _ = [block.draw(dt=dt) for block in block_list if not block.disable]
    _ = [block.draw(dt=dt) for block in block_list if not block.disable]
    # draw floor
    pr.draw_line_v(pr.Vector2(0, height - floor_y_pos), pr.Vector2(width, height - floor_y_pos), pr.WHITE)
    pr.draw_line_v(pr.Vector2(0, int(height/2)), pr.Vector2(width, int(height/2)), pr.RED)
    pr.draw_fps(0,0)
    pr.draw_text(f"time ellapsed:{int(run_time)}",0 ,20, 20, pr.GREEN)
    pr.draw_text(f"frame count:{(int(frame_counter))}",0, 40, 20, pr.GREEN)
    pr.draw_text(f"blocks:{(len(block_list))}",0, 60, 20, pr.GREEN)
    pr.end_drawing()

    # reset block spawn timer
    if int(run_time) % 1 == 0:
        block_spawn_frame = False

pr.close_window()