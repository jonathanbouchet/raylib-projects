# raylib-projects
a collection of raylib app

This repo is meant to gather some of `raylib` scripts I've been doing as I'm still discovering this framework: https://www.raylib.com/

I'm using the `pyray python` bindings: https://electronstudio.github.io/raylib-python-cffi/pyray.html

## Projects
- `Simple Window`: a simple window display
- `Moving ball`: trying keyboard input
- `3D Rotating cube`: trying 3D
- `Instantiate Rings`: trying some bouncing physics
- `3d collisions check`: motivation: collision detection for 3d objects
- `raygui icons`: gui icons manipulation / raygui
- `tsoding`: reproduce [tsoding's video](https://www.youtube.com/watch?v=qjWkNZ0SXfo&t=7s) where a cube is rendering with simple math tools (amazing video)
- `Raycast`: idea is to display when a raycast hits an object. 
- `Solar System`: a 3D view of the Soalr System

# tests
- from the `projects` folder
- right now only `solar_system` has classes that can be tests
```bash
python -m pytest -rA
```

# Documentation
```bash
mkdocs build
mkdocs serve -a localhost:8001
```