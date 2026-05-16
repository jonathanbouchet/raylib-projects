import pyray as pr
import raylib as rl


class MyCamera:
    def __init__(
        self, position: pr.Vector3, target: pr.Vector3, fovy: float, speed: float
    ) -> None:

        self.camera = pr.Camera3D(
            position, target, pr.Vector3(0, 1, 0), fovy, rl.CAMERA_PERSPECTIVE
        )

        self.camera_speed = speed

    def update(self, action: str) -> None:

        if action == "left":
            self.camera.position.x -= self.camera_speed

        if action == "right":
            self.camera.position.x += self.camera_speed

        if action == "up":
            self.camera.position.y -= self.camera_speed

        if action == "down":
            self.camera.position.y += self.camera_speed

        if action == "recenter":
            self.camera.position = pr.Vector3(0.0, 5.0, 10.0)
