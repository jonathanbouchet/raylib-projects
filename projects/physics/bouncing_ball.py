import pymunk
import pyray as rl

# 1. Initialize Raylib window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"Pymunk + Raylib Physics")
rl.set_target_fps(60)

# Thickness / offset parameters
FLOOR_THICKNESS = 20
WALL_THICKNESS = 20
WALL_X_OFFSET = 10  # unused for polys but kept if needed later

# 2. Setup Pymunk Physics Space
space = pymunk.Space()
space.gravity = (0.0, 900.0)

# Create static body for boundaries
static_body = pymunk.Body(body_type=pymunk.Body.STATIC)

# Floor as a static box polygon: top at SCREEN_HEIGHT, height = FLOOR_THICKNESS
# If you want the floor top to be exactly at SCREEN_HEIGHT - 0, use:
floor_top = SCREEN_HEIGHT
floor_bottom = floor_top - FLOOR_THICKNESS
floor_verts = [(0, floor_bottom), (SCREEN_WIDTH, floor_bottom), (SCREEN_WIDTH, floor_top), (0, floor_top)]
print(f"{floor_verts=}")
floor_shape = pymunk.Poly(static_body, floor_verts)
floor_shape.elasticity = 0.5
floor_shape.friction = 0.9

# Left wall as polygon (x from 0 to WALL_THICKNESS)
left_wall_verts = [(0, 0), (WALL_THICKNESS, 0), (WALL_THICKNESS, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)]
left_wall = pymunk.Poly(static_body, left_wall_verts)
left_wall.elasticity = 0.8
left_wall.friction = 0.9
print(f"{left_wall_verts=}")

# Right wall as polygon (x from SCREEN_WIDTH - WALL_THICKNESS to SCREEN_WIDTH)
right_wall_verts = [
    (SCREEN_WIDTH - WALL_THICKNESS, 0),
    (SCREEN_WIDTH, 0),
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    (SCREEN_WIDTH - WALL_THICKNESS, SCREEN_HEIGHT),
]
right_wall = pymunk.Poly(static_body, right_wall_verts)
right_wall.elasticity = 0.8
right_wall.friction = 0.9
print(f"{right_wall_verts=}")

space.add(static_body, floor_shape, left_wall, right_wall)

# Create a dynamic bouncing ball
circle_radius = 25
ball_body = pymunk.Body(1.0, 100)
ball_body.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # start mid-screen
ball_body.velocity = (600, 0)
ball_shape = pymunk.Circle(ball_body, circle_radius)
ball_shape.elasticity = 0.8
ball_shape.friction = 0.5
space.add(ball_body, ball_shape)

# 3. Main Game Loop
while not rl.window_should_close():
    # Update physics
    dt = 1.0 / 60.0
    space.step(dt)

    # 4. Rendering
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # Draw Floor
    rl.draw_rectangle_v(
        rl.Vector2(0, int(floor_bottom)),
        rl.Vector2(SCREEN_WIDTH, FLOOR_THICKNESS),
        rl.DARKGRAY
    )

    # Draw Left Wall
    rl.draw_rectangle_v(
        rl.Vector2(0, 0),
        rl.Vector2(WALL_THICKNESS, SCREEN_HEIGHT),
        rl.GRAY
    )

    # Draw Right Wall
    rl.draw_rectangle_v(
        rl.Vector2(int(SCREEN_WIDTH - WALL_THICKNESS), 0),
        rl.Vector2(WALL_THICKNESS, SCREEN_HEIGHT),
        rl.GRAY
    )

    # Optional: draw red guideline at floor top
    rl.draw_line(0, SCREEN_HEIGHT - FLOOR_THICKNESS, SCREEN_WIDTH, SCREEN_HEIGHT - FLOOR_THICKNESS, rl.RED)

    # Draw Ball
    ball_pos = ball_body.position
    rl.draw_circle(
        int(ball_pos.x),
        int(ball_pos.y),
        circle_radius,
        rl.BLUE
    )

    rl.end_drawing()

rl.close_window()
