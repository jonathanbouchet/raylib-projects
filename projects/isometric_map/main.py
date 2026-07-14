from pathlib import Path
import pyray as pr
import math
width, height = 600, 600

THIS_DIR = (Path(__file__).parent).resolve()

def cart_to_iso(i: int, j: int, tile_width: int, tile_height: int):
    x_iso = (i - j) * (tile_width/2)
    y_iso = (i + j) * (tile_height/4) 
    return int(x_iso), int(y_iso)

pr.init_window(width, height, "isometric map")
pr.set_target_fps(60)

test_tile = pr.load_texture(f"{THIS_DIR}/tile_blue_test_68x68.png")

TILE_WIDTH = test_tile.width
TILE_HEIGHT = test_tile.height

print(f"{TILE_WIDTH}, {TILE_HEIGHT}")

origin = pr.Vector2(250, 250) # top of the map

while not pr.window_should_close():

    mouse_pos = pr.get_mouse_position()
    # Calculate screen offset relative to the rendering origin
    dx = mouse_pos.x - origin.x
    dy = mouse_pos.y - origin.y

    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    # Invert the math matching your render layout (i+j)*TILE_HEIGHT/4 and (i-j)*TILE_WIDTH/2
    hover_i = math.floor((dx / TILE_WIDTH) + (2 * dy / TILE_HEIGHT))
    hover_j = math.floor((2 * dy / TILE_HEIGHT) - (dx / TILE_WIDTH))

    for j in range(0, 5):
        for i in range(0, 5):
            # testing
            x, y = cart_to_iso(i=i, j=j, tile_width=TILE_WIDTH, tile_height=TILE_HEIGHT)
            pr.draw_texture(test_tile, int(origin.x) + x, int(origin.y) + y, pr.WHITE)
            # pr.draw_texture(test_tile, int(origin.x) + (i-j)*TILE_WIDTH//2, int(origin.y) + (i+j)*TILE_HEIGHT//4, pr.WHITE)

            screen_x = int(origin.x) + (i - j) * TILE_WIDTH // 2
            screen_y = int(origin.y) + (i + j) * TILE_HEIGHT // 4

            # if i == hover_i and j == hover_j:
            if 0 <= hover_i < 5 and 0 <= hover_j < 5:
                if i == hover_i and j == hover_j:

                    half_w = TILE_WIDTH // 2
                    half_h = TILE_HEIGHT // 4 # Diamond height is half of the asset step system
                    
                    # Corner coordinate anchors for the diamond polygon face
                    top    = pr.Vector2(screen_x + half_w, screen_y)
                    right  = pr.Vector2(screen_x + TILE_WIDTH, screen_y + half_h)
                    bottom = pr.Vector2(screen_x + half_w, screen_y + half_h * 2)
                    left   = pr.Vector2(screen_x, screen_y + half_h)
                    
                    # tile top
                    highlight_color = pr.Color(0, 255, 0, 100)
                    pr.draw_triangle(top, left, right, highlight_color)
                    pr.draw_triangle(left, bottom, right, highlight_color)
                    
                    # tile outline
                    pr.draw_line_ex(top, right, 2.0, pr.YELLOW)
                    pr.draw_line_ex(right, bottom, 2.0, pr.YELLOW)
                    pr.draw_line_ex(bottom, left, 2.0, pr.YELLOW)
                    pr.draw_line_ex(left, top, 2.0, pr.YELLOW)

                    # text debug
                    pr.draw_text(f"TILE i:{i}, j:{j}", 0, 20, 20, pr.GREEN)
                    pr.draw_text(f"HOVER i:{hover_i}, :{hover_j}", 0, 40, 20, pr.GREEN)
    pr.draw_fps(0,0)
    pr.end_drawing()

pr.close_window()