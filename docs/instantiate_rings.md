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

```bash
uv run projects/instantiate_rings/main.py   
```

| Start | running |
| :---: | :---: |
| ![start](img/instantiate_rings_0.png) | ![running](img/instantiate_rings_1.png) |
