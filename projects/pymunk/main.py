import asyncio
import pymunk
import pyray as pr
from src.pymunk_body import Static, Dynamic

# 1. Initialize Raylib window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Thickness / offset parameters
FLOOR_THICKNESS = 20
WALL_THICKNESS = 20
WALL_X_OFFSET = 10  # unused for polys but kept if needed later
FLOOR_Y_OFFSET = 0


async def main() -> None:

    pr.init_window(SCREEN_WIDTH, SCREEN_WIDTH, "app")
    pr.set_target_fps(60)

    # create a space and add properties
    space = pymunk.Space()
    space.gravity = (0.0, 500.0)

    floor = Static(
        position=pr.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - FLOOR_THICKNESS // 2),
        body_size=pr.Vector2(SCREEN_WIDTH, FLOOR_THICKNESS),
        elasticity=1.0,
        friction=1.0,
        color=pr.RAYWHITE,
    )
    left_wall = Static(
        position=pr.Vector2(
            FLOOR_THICKNESS // 2, (SCREEN_HEIGHT - FLOOR_THICKNESS) // 2
        ),
        body_size=pr.Vector2(FLOOR_THICKNESS, SCREEN_HEIGHT - FLOOR_THICKNESS),
        elasticity=1.0,
        friction=1.0,
        color=pr.ORANGE,
    )
    right_wall = Static(
        position=pr.Vector2(
            SCREEN_WIDTH - FLOOR_THICKNESS // 2, (SCREEN_HEIGHT - FLOOR_THICKNESS) // 2
        ),
        body_size=pr.Vector2(FLOOR_THICKNESS, SCREEN_HEIGHT - FLOOR_THICKNESS),
        elasticity=1.0,
        friction=1.0,
        color=pr.MAGENTA,
    )
    ball = Dynamic(
        position=pr.Vector2(SCREEN_WIDTH // 2, 100),
        radius=20,
        velocity=pr.Vector2(1000, 100),
        elasticity=1,
        friction=0.5,
        color=pr.Color(57, 255, 20, 255),
    )

    space.add(floor.static_body, floor.shape)
    space.add(left_wall.static_body, left_wall.shape)
    space.add(right_wall.static_body, right_wall.shape)
    space.add(ball.body, ball.shape)

    while not pr.window_should_close():
        # logic here
        dt = pr.get_frame_time()

        # rendering
        pr.begin_drawing()
        pr.clear_background(pr.Color(0, 0, 28, 255))

        floor.draw()
        left_wall.draw()
        right_wall.draw()
        ball.draw()

        pr.draw_fps(0, 0)
        pr.draw_line(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT, pr.RED)
        pr.draw_line(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2, pr.RED)
        pr.end_drawing()
        # update pymunk
        space.step(dt)
        await asyncio.sleep(0)

    pr.close_window()


if __name__ == "__main__":
    asyncio.run(main())
