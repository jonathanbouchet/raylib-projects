import pyray as pr

pr.init_window(400, 400, "Hello World")
pr.set_target_fps(60)

ball_pos = pr.Vector2(400 / 2, 400 / 2)
while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BEIGE)

    if pr.is_key_down(pr.KEY_DOWN):
        ball_pos.y += 10
    if pr.is_key_down(pr.KEY_UP):
        ball_pos.y -= 10
    if pr.is_key_down(pr.KEY_LEFT):
        ball_pos.x -= 10
    if pr.is_key_down(pr.KEY_RIGHT):
        ball_pos.x += 10

    pr.draw_circle_v(ball_pos, 25, pr.RED)
    pr.draw_fps(0,0)
    pr.end_drawing()

pr.close_window()
