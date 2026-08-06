import asyncio
import math
import pyray as pr
import raylib as rl
from .world import World
from .camera import Camera
from .entity import Entity


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
        tile_x: int,
        tile_y: int
    ):
        self.width = width
        self.height = height

        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.origin = pr.Vector2(0, 0)#self.width // 2, 10)
        self.world = World(
            grid_length_x=tile_x, grid_length_y=tile_y, width=self.width, height=self.height, origin=self.origin
        )
        _ = [print(tile) for tile in self.world.ground_tiles[0:5]]
        self.TILE_SIZE = 64 # should be real TILE_SIZE_WIDTH / 2
        # camera
        self.camera = Camera(width=self.width, height=self.height)
        # entities
        self.entities: list[Entity] = []

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        pr.set_mouse_position(self.width//2, self.height//2) # set the mouse position at the center of the screen to avoid the camera scrolling effect 
        self.world.load_textures()
        # testing to add an entity
        entity = Entity(id=0, name="test", width=self.width, height=self.height, tile_x=0, tile_y=0, texture=self.world.textures.get("Male_4_Idle0"), world=self.world)
        self.entities.append(entity)

    def update(self) -> None:
        self.camera.update()
        _ = [entity.update() for entity in self.entities]
        if pr.gui_button(pr.Rectangle(0, 60, 100, 20), "RANDOMIZE"):
            print("generating new map")
            self.world.clear_world()
            self.world.create_world()
            self.world.add_props_world()
            self.world.print_props_grid()
  
    def debug(self) -> None:
        # debug
        pr.clear_background(self.background_color)
        pr.draw_fps(0, 0)
        pr.draw_text(f"GROUND: {len(self.world.ground_tiles)}, PROPS: {len([tile for tile in self.world.props_tiles if tile.tile_name is not None])}", 0, 40, 20, pr.GREEN)
        pr.draw_line(0, self.height // 2, self.width, self.height // 2, pr.RED)
        pr.draw_line(0, self.height // 4, self.width, self.height // 4, pr.RED)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            pr.begin_drawing()
            self.draw()
            self.debug()
            pr.end_drawing()
            await asyncio.sleep(0)

    def recenter_iso_tile(self, tile_in: pr.Vector2, scroll: pr.Vector2) -> pr.Vector2:
        return pr.Vector2(
            self.origin.x + tile_in.x + self.width // 2 + scroll.x, 
            self.origin.y + tile_in.y + self.height // 4 + scroll.y
        )

    def screen_to_iso(self, screen_x, screen_y, scroll: pr.Vector2):
        """Convert screen mouse coordinates to 2D isometric grid coordinates."""
        # transform to world position (removing camera scroll and offset)
        world_x = screen_x - self.width//2 - self.TILE_SIZE//2 - scroll.x
        world_y = screen_y - self.height//4 - scroll.y

        # transform to cart (inverse of cart_to_iso)
        cart_y = (2*world_y - world_x)/2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = math.floor(cart_x // self.TILE_SIZE)
        grid_y = math.floor(cart_y // self.TILE_SIZE)
        return grid_x, grid_y


    def draw(self) -> None:
        # recenter
        if pr.is_key_pressed(rl.KEY_SPACE):
            self.camera.scroll = pr.Vector2(0, -self.height//2)
        # Get mouse position and calculate hovered tile
        mouse = pr.get_mouse_position()
        hover_x, hover_y = self.screen_to_iso(screen_x=mouse.x, screen_y=mouse.y, scroll=self.camera.scroll)
        pr.draw_text(f"[{hover_x}, {hover_y}]", 0, 20, 20, pr.GREEN)

        # rendering
        pr.clear_background(self.background_color)

        # draw floor
        self.world.draw_floor(scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y))

        # draw props
        self.world.draw_props(scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y))

        # draw entity
        # _ = [entity.draw(tile_x=0, tile_y=0, scroll=self.camera.scroll) for entity in self.entities]

        for x in range(0, self.world.grid_length_x):
            for y in range(0, self.world.grid_length_y):

                # tile highlight
                is_hovered = (
                    0 <= hover_x < self.tile_x
                    and 0 <= hover_y < self.tile_y
                    and hover_x == x
                    and hover_y == y
                )

                # isometric grid
                p = self.world.ground_tiles[x * self.tile_x + y].get_iso_rect()
                # print(p)
                # Corner coordinate anchors for the diamond polygon face
                top = pr.Vector2(p[2][0], p[2][1])
                right = pr.Vector2(p[1][0], p[1][1])
                bottom = pr.Vector2(p[0][0], p[0][1])
                left = pr.Vector2(p[3][0], p[3][1])

                top_centered = self.recenter_iso_tile(tile_in=top, scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y))
                right_centered = self.recenter_iso_tile(tile_in=right, scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y))
                bottom_centered = self.recenter_iso_tile(tile_in=bottom, scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y))
                left_centered = self.recenter_iso_tile(tile_in=left, scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y))

                # tile outline
                pr.draw_line_ex(top_centered, right_centered, 1.0, pr.YELLOW)
                pr.draw_line_ex(right_centered, bottom_centered, 1.0, pr.YELLOW)
                pr.draw_line_ex(bottom_centered, left_centered, 1.0, pr.YELLOW)
                pr.draw_line_ex(left_centered, top_centered, 1.0, pr.YELLOW)

                # Draw filled tile if hovered, otherwise draw basic grid lines
                if is_hovered:
                    # print(f"{top_centered.x=}, {top_centered.y=}")
                    pr.draw_triangle(top_centered, right_centered, bottom_centered, pr.Color(255,255,0,100))  # Left half
                    pr.draw_triangle(bottom_centered, left_centered, top_centered, pr.Color(255,255,0,100) ) # Right half
                    if pr.is_mouse_button_pressed(0):
                        pr.draw_text("mouse clicked", 0, 40, 20, pr.GREEN)
                        self.world.find_path(grid_x=hover_x, grid_y=hover_y)  # runs pathfinder algorithm


    def end(self) -> None:
        # unload textures
        self.world.unload_textures()
        pr.close_window()
