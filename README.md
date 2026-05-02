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

# Project Tree

```console
├── LICENSE
├── README.md
├── docs
│   ├── 3d_cube_camera.png
│   ├── moving_ball.png
│   └── simple_window.png
├── main.py
├── projects
│   ├── 3d_cube_camera
│   │   ├── __init__.py
│   │   └── main.py
│   ├── move_ball
│   │   ├── __init__.py
│   │   └── main.py
│   └── simple_window
│       ├── __init__.py
│       └── main.py
├── pyproject.toml
└── uv.lock
```