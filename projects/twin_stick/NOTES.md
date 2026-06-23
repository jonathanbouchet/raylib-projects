# Notes
This file is to document the day to day development

## 2026-06-20
- game idea: twin stick
    - game window: no collisions so that player re-appear on the other of the screen
    - player has thrust and drag to "simulate" space physics
    - gameplay: 
        1) either the time of each round is fixed but number of enemies increase
        2) the time decreases at each round but # of enemies remain fixed
    - game systems goal achievement: game manager, State Machine, animations 
    - nice to have: scrolling space background, shader to give a "tron" aesthetic  
 
## 2026-06-21
- prototype idea

<img src="../../images/ts_proto.png" alt="" width="200">

- not decided yet on either to use a simple triangle shape or use a texture
- experimented with contols: 2 choices:
    1. mouse to click on the destination and `<-`, `->` for rotation, `space` to shoot
    2. `^`, `<-`, `->` for player control and `space` to shoot 
- worked on improving the separation of concerns for the game manager: the idea is to have to have the `GameManager` to take care only of the `game` variables, and have a `ResourceMAnager` to take care of the resources (textures, sounds)
    - in that case, I don't end up with an ever growing `GameManager` class

```python
resources_manager = ResourceManager(assets_path="./resources.json", image_loader=lambda p: pr.load_texture(p))
    player_texture = resources_manager.get_image("player_idle")
    game = GameManager(
        width=600, height=600, fps_target=60, name="app", background_color=pr.BLACK
    )

class ResourceManager:
    def __init__(self, assets_path: str, image_loader):
        self.assets_path = assets_path
        self.image_loader = image_loader
        with open(self.assets_path, 'r') as f:
            self.asset_cfg = json.load(f)
        self.images = {}   # key -> texture
        self.sounds = {}   # key -> sound

class GameManager:
    def __init__(
        self,
        width: int,
        height: int,
        fps_target: int,
        name: str,
        background_color: pr.Color,
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
``` 