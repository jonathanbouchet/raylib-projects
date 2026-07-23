import math
import asyncio
import pyray as pr
from .world import World

TILE_WIDTH = 64
TILE_HEIGHT = 64

class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
        tile_x: int,
        tile_y: int,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.world = World(
            grid_length_x=tile_x, grid_length_y=tile_y, width=self.width, height=self.height, 
        )
        self.TILE_SIZE = 32 # should be real TILE_SIZE / 2

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        pr.set_mouse_position(self.width//2, self.height//2) # set the mouse position at the center of the screnn to avoid the camera scrolling effect
        print(self.world.world[0], type(self.world.world[0]))
        self.world.load_textures() # textures need raylib to be init first

    def update(self) -> None:
        pass

    def recenter_iso_tile(self, tile_in: pr.Vector2) -> pr.Vector2:
        return pr.Vector2(tile_in.x + self.width // 2, tile_in.y + self.height // 4)

    def screen_to_iso(self, screen_x, screen_y):
        """Convert screen mouse coordinates to 2D isometric grid coordinates."""
        # transform to world position (removing camera scroll and offset)
        world_x = screen_x - self.width//2 - self.TILE_SIZE//2
        world_y = screen_y - self.height//4
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2*world_y - world_x)/2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // self.TILE_SIZE)
        grid_y = int(cart_y // self.TILE_SIZE)
        return grid_x, grid_y

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
            self.draw_debug()
            await asyncio.sleep(0)

    def draw(self) -> None:
        mouse = pr.get_mouse_position()
        hover_x, hover_y = self.screen_to_iso(mouse.x, mouse.y)
        # print(f"{hover_x=}, {hover_y=}")

        pr.begin_drawing()
        pr.clear_background(self.background_color)

        for x in range(0, self.world.grid_length_x):
            for y in range(0, self.world.grid_length_y):

                # 1. cartesian grid
                tile = self.world.world[x][y]["cart_rect"]
                tile_rect = pr.Rectangle(tile[0][0], tile[0][1], TILE_WIDTH, self.world.TILE_SIZE)
                pr.draw_rectangle_lines_ex(tile_rect, 0.5, pr.GRAY)

                # 2. isometric grid
                p = self.world.world[x][y]["iso_rect"]
              
                # Corner coordinate anchors for the diamond polygon face
                top = pr.Vector2(p[2][0], p[2][1])
                right = pr.Vector2(p[1][0], p[1][1])
                bottom = pr.Vector2(p[0][0], p[0][1])
                left = pr.Vector2(p[3][0], p[3][1])

                top_centered = self.recenter_iso_tile(tile_in=top)
                right_centered = self.recenter_iso_tile(tile_in=right)
                bottom_centered = self.recenter_iso_tile(tile_in=bottom)
                left_centered = self.recenter_iso_tile(tile_in=left)

                # 3. tile outline
                pr.draw_line_ex(top_centered, right_centered, 0.5, pr.YELLOW)
                pr.draw_line_ex(right_centered, bottom_centered, 0.5, pr.YELLOW)
                pr.draw_line_ex(bottom_centered, left_centered, 0.5, pr.YELLOW)
                pr.draw_line_ex(left_centered, top_centered, 0.5, pr.YELLOW)

                # 4. draw tiles: floor and props
                tile = self.world.world[x][y]["tile"]
                render_pos = self.world.world[x][y]["render_pos"]
                if tile == "sand":
                 pr.draw_texture_v(self.world.textures.get(tile), self.recenter_iso_tile(tile_in=pr.Vector2(render_pos[0], render_pos[1])), pr.WHITE)
                else:
                    pr.draw_texture_v(
                        self.world.textures.get(tile),
                        self.recenter_iso_tile(
                            tile_in=pr.Vector2(
                                render_pos[0],
                                render_pos[1]+
                                - (
                                    self.world.textures.get(tile).height // 2 ## 64x62 -> 31
                                    - self.world.TILE_SIZE // 2 # 64/2
                                ),
                            )
                        ),
                        pr.WHITE,
                    )
                # if tile == "sand":
                #     pr.draw_texture_v(self.world.textures.get(tile), self.recenter_iso_tile(tile_in=pr.Vector2(render_pos[0], render_pos[1])), pr.WHITE)

        pr.draw_text(f"[{hover_x}, {hover_y}]", 0, 20, 20, pr.GREEN)
        pr.end_drawing()

    def draw_debug(self) -> None:
        # debug
        pr.clear_background(self.background_color)
        pr.draw_fps(0, 0)
        pr.draw_line(0, self.height // 2, self.width, self.height // 2, pr.RED)
        pr.draw_line(0, self.height // 4, self.width, self.height // 4, pr.RED)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)

    def end(self) -> None:
        self.world.unload_textures()
        pr.close_window()

