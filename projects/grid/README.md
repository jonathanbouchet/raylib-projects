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

### List of algorithms

```python
import pathfinding.finder as pf
pf.__all__
# ['a_star', 'best_first', 'bi_a_star', 'bi_breadth_first', 'bi_best_first', 'bi_dijkstra', 'breadth_first', 'dijkstra', 'finder', 'ida_star']
```

- A*
- Dijkstra
- Best-First
- Bi-directional A*
- Breadth First Search (BFS)
- Bi-directional Breadth First Search (BFS)
- Iterative Deeping A* (IDA*)
- Minimum Spanning Tree (MSP)

### Output example

```bash
1 1 1 1 0 1 1 1 1 0 
1 1 1 1 0 1 1 1 1 1 
1 0 0 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 1 1 
1 1 0 1 1 1 1 1 1 1 
1 1 1 1 1 1 1 1 0 1 
1 0 1 1 1 1 0 0 1 1 
1 1 0 1 1 1 1 0 1 1 
1 1 0 1 1 1 1 1 1 1 
1 0 1 1 1 1 1 1 1 3 
Algorithm finished in 69 iterations.
Path found:
[(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (4, 4), (5, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9), (9, 9)]

Visualized Grid Map:
+----------+
|    #    #|
| sxx#     |
| ##x      |
|   x      |
|  # x     |
|     x  # |
| #   x##  |
|  #  x #  |
|  #   xx  |
| #      xe|
+----------+
```