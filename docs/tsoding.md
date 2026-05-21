- goal is to recreate [Tsoding's demo](https://www.youtube.com/watch?v=qjWkNZ0SXfo) where he showed how to project 3D point on the screen coordinates to illustrate 3D graphics

```python
(x, y ,z) : in 3D space
x' = x/z
y' = y/z
```

```bash
uv run projects/tsoding/main.py 
```

| only vertices | wireframes | both |
| :---: | :---: | :---: |
| ![](img/tsoding_recording_0.png) | ![](img/tsoding_recording_1.png)  | ![](img/tsoding_recording_2.png)  |


::: projects.tsoding.main.get_point
    options:
      show_source: true
      show_root_heading: true

::: projects.tsoding.main.project
    options:
      show_source: true
      show_root_heading: true