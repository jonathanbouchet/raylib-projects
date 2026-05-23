## what is it
- a character animation script

## how it works
- animations are `png` files saved in the `player_anims` folder
- each animation contains several png files so there's a function thatloads each png and save them as a list of `Texture2D` for a given animation:

```python
for anim in ["idle", "run"]:
        anim_dir = Path(f"{THIS_DIR}/{anim}")
        file_count = sum(1 for x in anim_dir.iterdir() if x.is_file())
        textures[anim] = [
            pr.load_texture(f"{str(anim_dir)}/{i}.png") for i in range(file_count)
        ]
```
- the `character` class has an `animation_index` that runs through all the textures and draw them when it matches a given animation when the `draw` is called
::: projects.character_animation.character.Player.draw
        handler: python
        show_source: True

- this might not scale really well when there are multiple animations so a `State Machine` might be a good option

## Project structure
```bash
player_anims
├── air_attack
│   ├── 0.png
│   ├── 1.png
│   └── 2.png
├── attack
│   ├── 0.png
│   ├── 1.png
│   └── 2.png
├── fall
│   └── 0.png
├── hit
│   ├── 0.png
│   ├── 1.png
│   └── 2.png
├── idle
│   ├── 0.png
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   └── 4.png
├── jump
│   └── 0.png
├── run
│   ├── 0.png
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   └── 5.png
└── wall
    └── 0.png
```
- animations are available at [itch.io: treasure-hunters](https://pixelfrog-assets.itch.io/treasure-hunters) under a _Creative Commons Zero v1.0 Universal_ license

