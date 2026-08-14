import asyncio
import pyray as pr
from .utils import load_textures
from .world import World
from .waypoint import WayPoints
from .agent import Agent


class Game:
    def __init__(
        self,
        width: int,  # game window width
        height: int,  # game window height
        fps_target: int,  # game fps target
        name: str,  # game name
        background_color: pr.Color,  # game background color
        tile_x: int,  # number of tiles on X-axis
        tile_y: int,  # number of tiles on Y-axis
    ):
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.name = name
        self.background_color = background_color
        self.tile_x = tile_x
        self.tile_y = tile_y

    def init(self):
        pr.init_window(self.width, self.height, self.name)
        pr.set_target_fps(self.fps_target)

        # load and add textures
        self.textures = load_textures()

        # create world
        self.world = World(
            grid_length_x=self.tile_x,
            grid_length_y=self.tile_y,
            width=self.width,
            height=self.height,
            textures=self.textures,
        )
        _ = [print(tile) for tile in self.world.ground_tiles[0:5]]

        # add markers
        self.markers = self.world.make_path()

        # create and add waypoints
        self.waypoints = WayPoints(positions=self.markers)
        print(f"number of waypoints: {self.waypoints.get_number_waypoints()}")
        for i in range(0, self.waypoints.get_number_waypoints()):
            print(i, self.waypoints.get_waypoint(idx=i))

        # create agent
        self.agent = Agent(
            position=pr.Vector2(288, 96),
            direction=pr.Vector2(1, 0),
            speed=200,
            debug=True,
            texture = self.textures.get("agent")["texture"],
            width=20,
            height=20,
            color=pr.YELLOW
        )
        self.agent.set_initial_waypoint(markers=self.markers)

    def update(self) -> None:
        dt = pr.get_frame_time()
        self.agent.update(dt=dt, waypoints=self.waypoints)

    async def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            pr.begin_drawing()
            self.draw()
            self.debug()
            pr.end_drawing()
            await asyncio.sleep(0)

    def debug(self) -> None:
        # debug
        pr.clear_background(self.background_color)
        if pr.get_frame_time():
            pr.draw_text(f"FPS: {int(1.0 / pr.get_frame_time())}", 0, 0, 20, pr.RED)
            pr.draw_text(f"GROUND: {len(self.world.ground_tiles)}", 0, 20, 20, pr.RED)

    def draw(self) -> None:
        self.world.draw_ground()
        self.world.draw_grid()
        self.world.draw_path()
        self.waypoints.draw_waypoint_index()
        self.agent.draw()

    def end(self) -> None:
        pr.close_window()
