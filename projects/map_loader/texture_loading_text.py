import pyray as pr
pr.init_window(1,1,'t')
tex = pr.load_texture('projects/map_loader/assets/terrain_32x32.png')
print(f"{tex.width=}, {tex.height=}")
pr.close_window()