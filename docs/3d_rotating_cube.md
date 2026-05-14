- trying 3D
```bash
uv run projects/3d_cube_camera/main.py
```
![start](img/3d_cube_camera.png)

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

```bash
Traceback (most recent call last):
  File "/Users/jonathanbouchet/WORK/RAYLIB_PROJECTS_GH/raylib-projects/projects/3d_cube_camera/main.py", line 27, in <module>
    pr.draw_cube_wires_v(position=pr.Vector3(-3,0,3), size=pr.Vector3(2,2,2), color=pr.BLUE)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: _wrap_function.<locals>.wrapped_func() got an unexpected keyword argument 'position'
```