# raylib-projects
a collection of raylib app

This repo is meant to gather some of `raylib` scripts I've been doing as I'm still discovering this framework: https://www.raylib.com/

I'm using the `pyray python` bindings: https://electronstudio.github.io/raylib-python-cffi/pyray.html


## Simple Window
- a simple window display
```console
uv run projects/simple_window/main.py
```

!["docs/simple_window.png"](docs/simple_window.png)

## Moving ball
- trying keyboard input
```console
uv run projects/move_ball/main.py
```

!["docs/moving_ball.png"](docs/moving_ball.png)

## 3D Rotating cube

- trying 3D
```console
uv run projects/3d_cube_camera/main.py
```

!["docs/3d_cube_camera.png"](docs/3d_cube_camera.png)

- looks like to apply a `rotation` to an object, I should use `pr.draw_model_ex` function so the `mesh` needs to be define before
- the (high level) structure of a `raylib` app :
1. define window
2. loop (= 1 frame):
    - define the app logic
    - start drawing
    - start camera
    - draw elements of your app
    - clear the frame buffer
    - close camera
    - close drawing
3. close window
- I still don't understand why the bindings do not allow for type hints. For example, highlighting `pr.draw_cube_wires_v` shows the following definition:

```python
(function) def draw_cube_wires_v(
    position: Vector3 | list | tuple,
    size: Vector3 | list | tuple,
    color: Color | list | tuple
) -> None
Draw cube wires (Vector version).
```

so it's natural to instantiate this object like this in the script:

```python
pr.draw_cube_wires_v(position=pr.Vector3(-3,0,3), size=pr.Vector3(2,2,2), color=pr.BLUE) # not working
```

However it's returning the following error:

```console
Traceback (most recent call last):
  File "/Users/jonathanbouchet/WORK/RAYLIB_PROJECTS_GH/raylib-projects/projects/3d_cube_camera/main.py", line 27, in <module>
    pr.draw_cube_wires_v(position=pr.Vector3(-3,0,3), size=pr.Vector3(2,2,2), color=pr.BLUE)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: _wrap_function.<locals>.wrapped_func() got an unexpected keyword argument 'position'
```

## Instantiate Rings
- trying some bouncing physics
- click anywhere within the window and it spawns a ring (random direction, random speed, inner and outer radius, random color)
    - the red line shows the direction (was for debugging but I left it)
- the bouncing part is done but checking the position of the ring with the screen borders: if true, the direction are reversed
```python
if (
    self.pos.x >= (setting.WINDOW_WIDTH - self.outer_radius)
        or self.pos.x <= self.outer_radius
    ):
        self.direction.x *= -1
    if (
        self.pos.y >= (setting.WINDOW_HEIGHT - self.outer_radius)
        or self.pos.y <= self.outer_radius
    ):
        self.direction.y *= -1
```
- organize the code into classes; `Game` is its own class so when calling `game.run`, the full `raylib` process is done
- the top left counter keeps track of the number of rings instantiated

```console
uv run projects/instantiate_rings/main.py   
```

| Start | running |
| :---: | :---: |
| ![start](docs/instantiate_rings_0.png) | ![running](docs/instantiate_rings_1.png) |

## 3d collisions check
- motivation: collision detection for 3d objects
- raygui: [https://github.com/raysan5/raygui](https://github.com/raysan5/raygui)
- both player and the obstacle to collide with are `cube mesh`
- the collision is checked using the `pr.check_collision_boxes` function
- when true, a `raygui textbox` is drawn and color of the obstacle changes

```console
uv run projects/3d_collisions_check/main.py   
```

| no collision | collision |
| :---: | :---: |
| ![no_coll](docs/3d_collision_check_no.png) | ![coll](docs/3d_collision_check_yes.png) |


## `raygui` icons
- motivation: gui icons manipulation / raygui
- raygui: [https://github.com/raysan5/raygui](https://github.com/raysan5/raygui)

```console
uv run projects/raygui_icons/main.py   
```

| all icons | icon pressed |
| :---: | :---: |
| ![all icons](docs/raygui_icons_all.png) | ![icon pressed](docs/raygui_icons_pressed.png) |

## tsoding
- motivation: reproduce [tsoding's video](https://www.youtube.com/watch?v=qjWkNZ0SXfo&t=7s) where a cube is rendering with simple math tools (amazing video)

```console
uv run projects/tsoding/main.py   
```

| rotation | rotation with wireframe |
| :---: | :---: |
| ![rotation](docs/tsoding_recording.png ) | TO DO|

<!-- [![Watch the video](https://github.com/jonathanbouchet/raylib-projects/blob/main/docs/tsoding_recording.mov)](https://github.com/jonathanbouchet/raylib-projects/blob/main/docs/tsoding_recording.mov) -->


# Project Tree

```console
├── LICENSE
├── README.md
├── docs
│   ├── 3d_collision_check_no.png
│   ├── 3d_collision_check_yes.png
│   ├── 3d_cube_camera.png
│   ├── instantiate_rings_0.png
│   ├── instantiate_rings_1.png
│   ├── moving_ball.png
│   ├── raygui_icons_all.png
│   ├── raygui_icons_pressed.png
│   └── simple_window.png
├── main.py
├── projects
│   ├── 3d_collisions_check
│   │   ├── __init__.py
│   │   └── main.py
│   ├── 3d_cube_camera
│   │   ├── __init__.py
│   │   └── main.py
│   ├── instantiate_rings
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── settings.cpython-313.pyc
│   │   │   └── sprite.cpython-313.pyc
│   │   ├── main.py
│   │   ├── settings.py
│   │   └── sprite.py
│   ├── move_ball
│   │   ├── __init__.py
│   │   └── main.py
│   ├── raygui_icons
│   │   ├── __init__.py
│   │   ├── assets
│   │   │   └── icon.json
│   │   └── main.py
│   └── simple_window
│       ├── __init__.py
│       └── main.py
├── pyproject.toml
└── uv.lock
```