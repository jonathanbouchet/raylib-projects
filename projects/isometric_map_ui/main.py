import math
from pathlib import Path
import pyray as pr
import raylib as rl

THIS_DIR = (Path(__file__).parent/"assets").resolve()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 320
TILE_WIDTH = 64
TILE_HEIGHT = 32
GRID_SIZE = 20
OFFSET_X = SCREEN_WIDTH // 2
OFFSET_Y = 50

ORIGIN = pr.Vector2(OFFSET_X, OFFSET_Y)


class UIElement:
    def __init__(
        self,
        position: pr.Vector2,
        name: str,
        width: int,
        height: int,
        texture: pr.Texture,
    ) -> None:
        self.position = position
        self.name = name
        self.width = width
        self.height = height
        self.texture = texture
        self.rect = pr.Rectangle(position.x, position.y, self.width, self.height)
        self.is_selected: bool = False

    def update(self) -> None:
        if pr.is_mouse_button_pressed(0):
            if pr.check_collision_point_rec(pr.get_mouse_position(), self.rect):
                self.is_selected = not self.is_selected
                print(f"selected tile: {self.name}, {self.is_selected}")

    def get_texture(self) -> pr.Texture:
        return self.texture

    def draw(self) -> None:
        pr.draw_texture_ex(self.texture, self.position, 0, 0.5, pr.WHITE)
        # pr.draw_texture_v(self.texture, self.position, pr.WHITE)
        if self.is_selected:
            pr.draw_rectangle_lines(
                int(self.position.x),
                int(self.position.y),
                int(self.width//2),  # for visualization purposes only
                int(self.height//2), # for visualization purposes only
                pr.SKYBLUE,
            )
        else:
            pr.draw_rectangle_lines(
                int(self.position.x),
                int(self.position.y),
                int(self.width//2),
                int(self.height//2),
                pr.RED,
            )

    def set_status(self, status: bool) -> None:
        self.is_selected = status

    def get_status(self) -> bool:
        return self.is_selected


class UIContainer:
    def __init__(self, position: pr.Vector2, el: list[UIElement]) -> None:
        self.position = position
        self.ui_elements = el

    def update_status(self) -> None:
        statuses = [x.get_status() for x in self.ui_elements]
        if any(statuses):
            index = [i for i, val in enumerate(statuses) if val]

    def get_selected(self) -> str:
        statuses = [x.get_status() for x in self.ui_elements]
        if any(statuses):
            index = [i for i, val in enumerate(statuses) if val]
            return self.ui_elements[index[0]].name
        
    def get_texture(self) -> pr.Texture:
        if self.get_selected() is not None:
            if self.get_selected() == "blue tile":
                return self.ui_elements[0].get_texture()
            if self.get_selected() == "green tile":
                return self.ui_elements[1].get_texture()

    def update(self) -> None:
        for el in self.ui_elements:
            el.update()
        self.update_status()
        # _ = [el.update() for el in self.ui_elements]

    def draw(self) -> None:
        _ = [el.draw() for el in self.ui_elements]

    def get_names(self) -> None:
        return [x.name for x in self.ui_elements]


def iso_to_screen(x, y):
    """Convert 2D grid coordinates to isometric screen coordinates."""
    screen_x = (x - y) * (TILE_WIDTH // 2) + OFFSET_X
    screen_y = (x + y) * (TILE_HEIGHT // 2) + OFFSET_Y
    return screen_x, screen_y


def screen_to_iso(screen_x, screen_y):
    """Convert screen mouse coordinates to 2D isometric grid coordinates."""
    # Inverse transformation matrix logic
    x = screen_x - OFFSET_X
    y = screen_y - OFFSET_Y

    # Solve the system of equations for (x, y) grid space
    nx = (x / (TILE_WIDTH / 2) + y / (TILE_HEIGHT / 2)) / 2
    ny = (y / (TILE_HEIGHT / 2) - x / (TILE_WIDTH / 2)) / 2
    return math.floor(nx), math.floor(ny)


def main():
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pyray Isometric Grid with Hover")
    pr.set_target_fps(60)

    blue_tile = pr.load_texture(f"{THIS_DIR}/blue_tile_64x64.png")
    green_tile = pr.load_texture(f"{THIS_DIR}/green_tile_64x64.png")
    ui_element_blue = UIElement(
        position=pr.Vector2(10, 10),
        name="blue tile",
        width=blue_tile.width,
        height=blue_tile.height,
        texture=blue_tile,
    )
    ui_element_green = UIElement(
        position=pr.Vector2(42, 10),
        name="green tile",
        width=green_tile.width,
        height=green_tile.height,
        texture=green_tile,
    )
    ui = UIContainer(position=pr.Vector2(0, 0), el=[ui_element_blue, ui_element_green])

    camera = pr.Camera2D()
    camera.offset = pr.Vector2(0, 0)
    camera.target = pr.Vector2(0, 0)
    camera.rotation = 0.0
    camera.zoom = 1.0

    zoom_mode = 0  # 0-Mouse Wheel, 1-Mouse Move

    use_camera: bool = False

    while not pr.window_should_close():
        # update
        ui.update()
        if use_camera:
            if pr.is_key_pressed(rl.KEY_ONE):
                zoom_mode = 0
            elif pr.is_key_pressed(rl.KEY_TWO):
                zoom_mode = 1

            # Translate based on mouse left click
            if pr.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
                # print("here")
                delta = pr.get_mouse_delta()
                delta = pr.vector2_scale(delta, -1.0 / camera.zoom)
                camera.target = pr.vector2_add(camera.target, delta)

        # Get mouse position and calculate hovered tile
        mouse = pr.get_mouse_position()
        hover_x, hover_y = screen_to_iso(mouse.x, mouse.y)

        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pr.begin_mode_2d(camera)

        ui.draw()

        # Draw the 10x10 grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Calculate screen coordinates for the corners of the tile
                sx, sy = iso_to_screen(col, row)

                # Check if this specific tile is currently hovered
                is_hovered = (
                    0 <= hover_x < GRID_SIZE
                    and 0 <= hover_y < GRID_SIZE
                    and hover_x == col
                    and hover_y == row
                )

                # Define the 4 corners of the isometric diamond
                p1 = pr.Vector2(sx, sy)
                p2 = pr.Vector2(sx + TILE_WIDTH // 2, sy + TILE_HEIGHT // 2)
                p3 = pr.Vector2(sx, sy + TILE_HEIGHT)
                p4 = pr.Vector2(sx - TILE_WIDTH // 2, sy + TILE_HEIGHT // 2)

                # Draw filled tile if hovered, otherwise draw basic grid lines
                if is_hovered:
                    fill_color = pr.SKYBLUE
                    pr.draw_triangle(p1, p4, p3, fill_color)  # Left half
                    pr.draw_triangle(p1, p3, p2, fill_color)  # Right half

                    if ui.get_selected() is not None:
                        current_texture: pr.Texture = ui.get_texture()
                        # print(f"{current_texture=}")

                        if pr.is_mouse_button_pressed(0):
                            print("here")
                            pr.draw_texture(current_texture, int(ORIGIN.x) + (hover_x-hover_y)*TILE_WIDTH//2, int(ORIGIN.y) + (hover_x+hover_y)*TILE_HEIGHT//4, pr.WHITE)


                # Draw the diamond outline
                pr.draw_line_v(p1, p2, pr.DARKGRAY)
                pr.draw_line_v(p2, p3, pr.DARKGRAY)
                pr.draw_line_v(p3, p4, pr.DARKGRAY)
                pr.draw_line_v(p4, p1, pr.DARKGRAY)


        pr.end_mode_2d()

        # Display hovered tile coordinates
        pr.draw_fps(SCREEN_WIDTH - 120, 0)
        pr.draw_text(f"({hover_x},{hover_y})", SCREEN_WIDTH - 120, 20, 20, pr.GREEN)
        pr.draw_text(f"{ui.get_selected()}", SCREEN_WIDTH - 120, 40, 20, pr.GREEN)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
