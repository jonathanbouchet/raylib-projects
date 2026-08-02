import asyncio
import pyray as pr
from .world import World, TileData, TextureData
from .camera import Camera
from .ui import UIContainer
from .resource_manager import ResourceManager
from .entity import Entity


class Game:
    def __init__(self, resource_manager) -> None:
        self.resource_manager: ResourceManager = resource_manager
        self.width = self.resource_manager.game_data().get("width") # screen width in pixels
        self.height = self.resource_manager.game_data().get("height") # screen height in pixels
        self.fps_target = self.resource_manager.game_data().get("fps_target") # game FPS
        self.name = self.resource_manager.game_data().get("name") # game name
        self.background_color = self.resource_manager.game_data().get( # background color
            "background_color"
        )
        self.grid_length_x = self.resource_manager.game_data().get("tile_x") # number of tiles on the x-axis
        self.grid_length_y = self.resource_manager.game_data().get("tile_y") # number of tiles on the y-axis
        self.debug = self.resource_manager.game_data().get("debug") # flag to show debug or not

        # add a World instance as member of the game
        self.world = World(
            grid_length_x=self.grid_length_x, # number of tiles on the x-axis
            grid_length_y=self.grid_length_y, # number of tiles on the y-axis
            width=self.width, # screen width in pixels
            height=self.height, # screen height in pixels
        )
        self.TILE_SIZE = 32  
        # half size of a tile in pixels
        # should be real size of texture TILE_SIZE / 2

        # add a Camera instance as member of the game
        self.camera = Camera(width=self.width, height=self.height)

        # add entities to the game
        self.entities: list[Entity] = []

    def init(self):
        """
        - raylib window and FPS init
        - self.world builds the isometric map and add ground_tiles textures
        - loading textures done at the very end because of requirement from raylib to be init first
        - build UI
        """
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)
        _ = [print(tile) for tile in self.world.ground_tiles[0:5]]
        print(f"TOTAL NUMBER of TILES IN WORLD: {len(self.world.ground_tiles)}")
        self.world.load_textures(
            textures_data_path=self.resource_manager.textures_data()
        )

        # add a UI instance as a member of the game
        self.ui = UIContainer(
            position=pr.Vector2(self.width - 50, 10), # position in game coordinates (pixels) of the top left corner
            el=[
                "building01",
                "building02",
                "road_top_right",
                "road_bottom_round",
                "road_bottom_right_T",
                "road_bottom_right",
                "road_crossing",
                "road_top_left_T",
                "road_bottom_left_T",
                "road_top_right_T",
                "trashcan"
            ], # list of texture names used by the UI
            world=self.world,
        )
        # add the current UI Element selected, if any
        self.ui_element_selected: int = None

        # testing to add an entity
        # entity = Entity(id=0, name="car", width=self.width, height=self.height, tile_x=0, tile_y=0, texture=self.world.textures.get("car").get_texture(), world=self.world)
        # self.entities.append(entity)

    def update(self) -> None:
        self.camera.update()
        self.ui_element_selected = self.ui.update(current_selection=self.ui_element_selected)

    def recenter_iso_tile(self, tile_in: pr.Vector2, scroll: pr.Vector2) -> pr.Vector2:
        """
        - recenter the isometric tile in the center of the game screen
        - take into account the camera srolling effect
        """
        return pr.Vector2(
            tile_in.x + self.width // 2 + scroll.x,
            tile_in.y + self.height // 4 + scroll.y,
        )

    def screen_to_iso(self, mouse: pr.Vector2, scroll: pr.Vector2):
        """
        - Convert screen mouse coordinates to 2D isometric grid coordinates.
        - Take into account the camera scrolling effect
        """
        # transform to world position (removing camera scroll and offset)
        world_x = mouse.x - self.width // 2 - self.TILE_SIZE // 2 - scroll.x
        world_y = mouse.y - self.height // 4 - scroll.y

        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x

        # transform to grid coordinates
        grid_x = int(cart_x // self.TILE_SIZE)
        grid_y = int(cart_y // self.TILE_SIZE)
        return grid_x, grid_y

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
            self.ui.draw()
            if self.debug:
                self.draw_debug()
            await asyncio.sleep(0)

    def draw(self) -> None:
        mouse = pr.get_mouse_position()
        hover_x, hover_y = self.screen_to_iso(mouse=mouse, scroll=self.camera.scroll)

        pr.begin_drawing()
        pr.clear_background(self.background_color)

        # draw floor only once
        self.world.draw(scroll=self.camera.scroll)

        for x in range(0, self.world.grid_length_x):
            for y in range(0, self.world.grid_length_y):
                # tile highlight
                is_hovered = (
                    0 <= hover_x < self.grid_length_x
                    and 0 <= hover_y < self.grid_length_y
                    and hover_x == x
                    and hover_y == y
                )

                p = self.world.ground_tiles[x*self.grid_length_x + y].get_iso_rect()

                # Corner coordinate anchors for the diamond polygon face
                top = pr.Vector2(p[2][0], p[2][1])
                right = pr.Vector2(p[1][0], p[1][1])
                bottom = pr.Vector2(p[0][0], p[0][1])
                left = pr.Vector2(p[3][0], p[3][1])

                top_centered = self.recenter_iso_tile(
                    tile_in=top,
                    scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y),
                )
                right_centered = self.recenter_iso_tile(
                    tile_in=right,
                    scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y),
                )
                bottom_centered = self.recenter_iso_tile(
                    tile_in=bottom,
                    scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y),
                )
                left_centered = self.recenter_iso_tile(
                    tile_in=left,
                    scroll=pr.Vector2(self.camera.scroll.x, self.camera.scroll.y),
                )

                # 3. tile outline
                if self.debug:
                    pr.draw_line_ex(top_centered, right_centered, 0.5, pr.YELLOW)
                    pr.draw_line_ex(right_centered, bottom_centered, 0.5, pr.YELLOW)
                    pr.draw_line_ex(bottom_centered, left_centered, 0.5, pr.YELLOW)
                    pr.draw_line_ex(left_centered, top_centered, 0.5, pr.YELLOW)

                # Draw filled tile if hovered, otherwise draw basic grid lines
                if is_hovered:
                    # print(f"{x=}, {y=}, id:{x*self.grid_length_x + y}")
                    current_tile: TileData = self.world.ground_tiles[x*self.grid_length_x + y]
                    current_tile_name = current_tile.get_tile_name()
                    current_tile_texture: TextureData = self.world.textures.get(current_tile_name)
                    current_tile_texture_is_buildable = current_tile_texture.get_buildable()

                    # checking if there are building
                    if len(self.world.additional_tiles) > 0:
                        for tile in self.world.additional_tiles:
                            if x == tile.get_grid_pos_x() and y == tile.get_grid_pos_y():
                                current_tile_name = tile.get_tile_name()
                                current_tile_texture: TextureData = self.world.textures.get(current_tile_name)
                                current_tile_texture_is_buildable = current_tile_texture.get_buildable()
                                break

                    if current_tile_texture_is_buildable:
                        pr.draw_triangle(
                            top_centered, right_centered, bottom_centered, pr.Color(255, 255, 0, 100)
                        )  # Left half
                        pr.draw_triangle(
                            bottom_centered, left_centered, top_centered, pr.Color(255, 255, 0, 100)
                        )  # Right half
                    else:
                        pr.draw_triangle(
                            top_centered, right_centered, bottom_centered, pr.Color(255, 0, 0, 100)
                        )  # Left half
                        pr.draw_triangle(
                            bottom_centered, left_centered, top_centered, pr.Color(255, 0, 0, 100)
                        )  # Right half
                    if (
                        pr.is_mouse_button_pressed(0) and 
                        self.ui_element_selected is not None and 
                        current_tile_texture_is_buildable is True 
                        and self.ui.ui_elements[self.ui_element_selected].name != "trashcan"
                    ):
                        
                        print(f"{x=}, {y=}, id:{x*self.grid_length_x + y}")
                        self.world.add_to_world(
                            ui_element_name=str(
                                self.ui.ui_elements[self.ui_element_selected].name
                            ),
                            tile_x=hover_x,
                            tile_y=hover_y,
                        )
        # _ = [ent.draw(tile_x=0, tile_y=0, scroll=self.camera.scroll) for ent in self.entities]
        pr.draw_text(f"tile X:{hover_x}, tile Y:{hover_y}", 0, 20, 20, pr.GREEN)
        pr.end_drawing()

    def draw_debug(self) -> None:
        # debug
        pr.clear_background(self.background_color)
        pr.draw_fps(0, 0)
        pr.draw_text(f"GROUND TILES: {len(self.world.ground_tiles)}, BUILDING TILES: {len(self.world.additional_tiles)}", 0, 40, 20, pr.GREEN)
        if self.ui_element_selected is not None:
            pr.draw_text(
                f"UI ID: {str(self.ui.ui_elements[self.ui_element_selected].id)}, TYPE: {str(self.ui.ui_elements[self.ui_element_selected].name)}",
                0,
                60,
                20,
                pr.GREEN,
            )
        pr.draw_line(0, self.height // 2, self.width, self.height // 2, pr.RED)
        pr.draw_line(0, self.height // 4, self.width, self.height // 4, pr.RED)
        pr.draw_line(self.width // 2, 0, self.width // 2, self.height, pr.RED)

    def end(self) -> None:
        self.world.unload_textures()
        pr.close_window()
