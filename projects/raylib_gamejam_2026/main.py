import asyncio
import random
import pyray as pr
from candidate import ChoiceContainer
from color_candidate import ColorContainer

width, height = 720, 720


def random_hex_color() -> str:
    # Generate a random integer between 0 and 16,777,215 (0xFFFFFF)
    # Format it as a 6-digit hex string with leading zeros
    return f"#{random.randint(0, 0xFFFFFF):06x}"


def hex_to_rgb(hex_str) -> list[int]:
    hex_str = hex_str.lstrip("#")
    # Convert pairs of hex characters to integers
    # return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return [int(hex_str[i : i + 2], 16) for i in (0, 2, 4)]


def hex_int_to_rgb(hex_num):
    r = (hex_num >> 16) & 0xFF
    g = (hex_num >> 8) & 0xFF
    b = hex_num & 0xFF
    return (r, g, b)


def gen_new_color():
    return random.choice([pr.RED, pr.BLUE, pr.GRAY, pr.GREEN, pr.PURPLE, pr.YELLOW])


async def main():

    pr.init_window(width, height, "raylib jam: hex+merge")
    pr.set_target_fps(60)

    is_generated: bool = False
    current_col: pr.Color = None
    current_hex: str = ""
    current_rgb: str = ""

    candidate = ChoiceContainer(
        position=pr.Vector2(180, 250), red_value=0, blue_value=0, green_value=0
    )
    red_container = ColorContainer(
        position=pr.Vector2(40, 400),
        value=100,
        outline_color=pr.WHITE,
        base_color=pr.RED,
    )
    green_container = ColorContainer(
        position=pr.Vector2(260, 400),
        value=100,
        outline_color=pr.WHITE,
        base_color=pr.GREEN,
    )

    blue_container = ColorContainer(
        position=pr.Vector2(480, 400),
        value=100,
        outline_color=pr.WHITE,
        base_color=pr.BLUE,
    )

    while not pr.window_should_close():
        # logic
        dt = pr.get_frame_time()
        red_container.update()
        green_container.update()
        blue_container.update()

        # rendering
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        generate_color = pr.Rectangle(width//2 - 100, 10, 200, 40)
        pr.draw_rectangle_rec(generate_color, pr.GREEN)
        pr.draw_text("GENERATE COLOR", width//2 - 100 + 5, 20, 20, pr.BLACK)

        if pr.check_collision_point_rec(pr.get_mouse_position(), generate_color):
            pr.draw_rectangle_rec(generate_color, pr.DARKGREEN)
            pr.draw_text("GENERATE COLOR", 100, 100, 20, pr.BLACK)

            if pr.is_mouse_button_pressed(0):
                is_generated = True
                current_hex: str = random_hex_color()
                current_col = hex_to_rgb(current_hex)  # gen_new_color()
                current_rgb = ",".join([str(i) for i in current_col])
                print(f"{current_hex=}, {current_col=}, {current_rgb=}")
                current_col.append(255)

        if is_generated:
            rect = pr.Rectangle(200, 90, 150, 150)
            pr.draw_rectangle_rounded(rect, 0.1, 100, current_col)
            pr.draw_text(current_hex, 240, 160, 20, pr.BLACK)

            rect2 = pr.Rectangle(370, 90, 150, 150)
            pr.draw_rectangle_rounded(rect2, 0.1, 100, current_col)
            pr.draw_text(current_rgb, 390, 160, 20, pr.BLACK)

            candidate.update(r=current_col[0], g=current_col[1], b=current_col[2],red_container=red_container, green_container=green_container, blue_container=blue_container)

        # draw candidate container
        candidate.draw()
        red_container.draw()
        green_container.draw()
        blue_container.draw()

        # draw axis
        pr.draw_line(0, height // 2, width, height // 2, pr.RED)
        pr.draw_line(width // 2, 0, width // 2, height, pr.RED)

        pr.end_drawing()
        pr.draw_fps(0, 0)
        await asyncio.sleep(0)

    pr.close_window()


if __name__ == "__main__":
    asyncio.run(main())
