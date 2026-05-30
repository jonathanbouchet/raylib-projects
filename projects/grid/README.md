## Motivation
- often times a game or app will require to have an underlying grid system
- this repo is providing a base class to split a game screen (`width`, `height`) according a tile_width (that will be the size of a cell of the grid)

## application
- Pathfinding demo: idea is from a start cell, end cell and some obstacles, to show the optimum path

### Python-pathfinder

ref: https://github.com/MichalKacprzak99/pathfinding-pygame/blob/main/pathfinding-pygame/pathfinder.py

```python
# 1. Define the grid matrix map
# 0 = Obstacle/Wall (unwalkable)
# 1 = Empty space (walkable, movement cost = 1)
# Values > 1 can be used to weight harder terrain (e.g., mud, hills)
matrix = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1]
]
```

- since a walkable tile is defined as 1, I need to initialize the grid with `1`
- a block will be defined as `0`
- we can define the starting and ending tile as `2` and `3`: choice of the user by mouse-clicking