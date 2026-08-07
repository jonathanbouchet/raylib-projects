from enum import Enum
import pyray as pr

class States(Enum):
    IDLE=0
    RUN=1
    PICKUP=2

class Character:
    def __init__(
        self,
        position: pr.Vector2,
        textures: list[pr.Texture]
    ) -> None:
        self.position = position  # position of the texture
        self.animation_index: int = 0
        self.state: States = States.IDLE
        self.all_textures: dict[str, list[pr.Texture]] = textures
        self.state_to_textures_mapping = {States.IDLE: "idle_SE", States.RUN:"run_SE", States.PICKUP: "pickup_SE"} 

    def update(self, selected_value: int) -> None:
        if selected_value is not None:
            self.set_state(selected_value)

    def set_state(self, selected_value) -> None:
        self.state = States(selected_value)


    def draw(self, dt: float) -> None:
        current_textures = self.all_textures.get(self.state_to_textures_mapping.get(self.state))
        self.animation_index += len(current_textures) * dt
        pr.draw_texture_v(
            current_textures[int(self.animation_index % len(current_textures))],
            self.position,
            pr.WHITE,
        )