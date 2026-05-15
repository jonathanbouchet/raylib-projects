from pathlib import Path
import pyray as pr
import raylib as rl

THIS_DIR = (Path(__file__).parent / "models").resolve()


class Model:
    def __init__(
        self, position: pr.Vector3, rotation_axis: pr.Vector3, rotation: float
    ) -> None:
        self.id: int = None
        self.is_selected: bool = False
        self.model: pr.Model = None
        self.position: pr.Vector3 = position
        self.rotation_axis: pr.Vector3 = rotation_axis
        self.rotation: float = rotation

    def draw(self) -> None:
        pr.draw_model_ex(
            self.blender_model,
            self.position,
            self.rotation_axis,
            self.rotation,
            pr.Vector3(1, 1, 1),
            rl.WHITE,
        )

    def update(self) -> None:
        pass

    def load(self, choice: int) -> None:
        if choice == 1:
            self.id = choice
            self.blender_model = pr.load_model(str(THIS_DIR / "cube.glb"))
            path: str = str(str(THIS_DIR / "cube.glb"))
            print(f"{path}")
            self.is_selected = True
        elif choice == 2:
            self.id = choice
            path: str = str(str(THIS_DIR / "cube.glb"))
            print(f"{path}")
            self.blender_model = pr.load_model(str(THIS_DIR / "sphere.glb"))
            self.is_selected = True
        elif choice == 3:
            self.id = choice
            path: str = str(str(THIS_DIR / "cube.glb"))
            print(f"{path}")
            self.blender_model = pr.load_model(str(THIS_DIR / "torus.glb"))
            self.is_selected = True
        elif choice == 4:
            self.id = choice
            path: str = str(str(THIS_DIR / "cube.glb"))
            print(f"{path}")
            self.blender_model = pr.load_model(str(THIS_DIR / "cube_colored.glb"))
            self.is_selected = True
        else:
            self.is_selected = False
            self.blender_model = None
