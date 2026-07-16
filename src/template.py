import asyncio
import pyray as pr

width, height = 600, 600


async def main() -> None:

    pr.init_window(width, height, "app")
    pr.set_target_fps(60)

    while not pr.window_should_close():
        # logic here

        # rendering
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pr.draw_fps(0, 0)

        pr.draw_line(width // 2, 0, width // 2, height, pr.RED)
        pr.draw_line(0, height // 2, width, height // 2, pr.RED)
        pr.end_drawing()
        await asyncio.sleep(0)

    pr.close_window()


if __name__ == "__main__":
    asyncio.run(main())
