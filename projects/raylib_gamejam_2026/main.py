import asyncio
import random
import pyray as pr

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

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        generate_color = pr.Rectangle(90, 90, 210, 40)
        pr.draw_rectangle_rec(generate_color, pr.GREEN)
        pr.draw_text("GENERATE COLOR", 100, 100, 20, pr.BLACK)

        if pr.check_collision_point_rec(pr.get_mouse_position(), generate_color):
            pr.draw_rectangle_rec(generate_color, pr.DARKGREEN)
            pr.draw_text("GENERATE COLOR", 100, 100, 20, pr.BLACK)

            if pr.is_mouse_button_pressed(0):
                is_generated = True
                current_hex: str = random_hex_color()
                current_col = hex_to_rgb(current_hex)  # gen_new_color()
                current_rgb = ",".join([str(i) for i in current_col])
                current_col.append(255)

        if is_generated:
            # pr.draw_text("CLICKED", 300, 100, 20, current_col)
            rect = pr.Rectangle(325, 90, 100, 40)
            pr.draw_rectangle_rounded(rect, 0.1, 100, current_col)
            pr.draw_text(current_hex, 300, 90, 20, pr.BLACK)
            pr.draw_text(current_rgb, 450, 90, 20, current_col)

        pr.end_drawing()
        pr.draw_fps(0, 0)
        await asyncio.sleep(0)

    pr.close_window()


if __name__ == "__main__":
    asyncio.run(main())
