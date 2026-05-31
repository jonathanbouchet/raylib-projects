import json
import numpy as np
import pyray as pr


class MapLoader:
    def __init__(
        self,
        window_width: int,
        window_height: int,
        tile_size: int,
        texture_path: str,
        map_path: str,
    ) -> None:
        self.window_width: int = window_width
        self.window_height: int = window_height
        self.window_tile_size: int = tile_size
        self.texture_path: str = texture_path
        self.map_path: int = map_path
        self.map: dict = {}
        self.map_data: dict = {}
        self.texture = None
        self.texture_num_row: int  #  = int(terrain_texture.height / TILE_WIDTH)
        self.texture_num_col: int  # = int(terrain_texture.width / TILE_WIDTH)
        self.mapdata_to_texture: list[dict[str, int]] = []

    def load_map(self) -> dict:
        with open(self.map_path, "r") as f:
            self.map = json.load(f)

    def load_texture(self) -> pr.Texture:
        self.texture = pr.load_texture(self.texture_path)
        self.texture_num_row = int(self.texture.height / self.window_tile_size)
        self.texture_num_col = int(self.texture.width / self.window_tile_size)
        print(f"{self.texture_num_row=}, {self.texture_num_col=}")

    def decode_map(self) -> list[dict[str, int]]:
        tiles = self.map.get("layers", "")
        tiles_data = tiles[0].get("data", "")
        num_tiles_y = self.map.get("height", "")
        num_tiles_x = self.map.get("width", "")

        val = np.array(tiles_data)
        res = val.reshape((num_tiles_y, num_tiles_x))
        print(f"{res=}")
        non_zero_vals = res[res != 0]  # tiles with data are !=0
        # [[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        #  [ 0,  0,  0, 73,  0,  0,  0,  0,  0,  0],

        found = np.nonzero(res)
        self.map_data = []
        for tile_id, row_id, col_id in zip(non_zero_vals, found[0], found[1]):
            self.map_data.append(
                {"tile_id": int(tile_id), "col_id": int(col_id), "row_id": int(row_id)}
            )

        print(f"{self.map_data=}")

    def map_data_to_texture(self):
        res = []
        for tile_data in self.map_data[:]:
            print(tile_data)
            tile_id_to_texture_y = int(
                tile_data.get("tile_id") / (self.texture_num_col - 1)
            )
            tile_id_to_texture_x = tile_data.get("tile_id") % self.texture_num_col - 1
            pos_texture_x = tile_data.get("col_id")
            pos_texture_y = tile_data.get("row_id")
            print(
                f"{tile_id_to_texture_x=}, {tile_id_to_texture_y=}, {pos_texture_x=}, {pos_texture_y=}"
            )
            res.append(
                {
                    "tile_id_to_texture_x": tile_id_to_texture_x,
                    "tile_id_to_texture_y": tile_id_to_texture_y,
                    "pos_texture_x": pos_texture_x,
                    "pos_texture_y": pos_texture_y,
                }
            )
        self.mapdata_to_texture = res

    def make_map(self) -> None:
        self.load_map()
        self.load_texture()
        self.decode_map()
        self.map_data_to_texture()
        print(f"loaded {len(self.mapdata_to_texture)} tiles")

    def draw(self):
        for tile in self.mapdata_to_texture:
            tile_col = tile.get("tile_id_to_texture_x")
            tile_row = tile.get("tile_id_to_texture_y")

            # print(f"{selected_col=}, {selected_row=}")

            # Calculate the X and Y pixel positions on the spritesheet
            tile_x = tile_col * self.window_tile_size
            tile_y = tile_row * self.window_tile_size

            source_rec = pr.Rectangle(
                tile_x, tile_y, self.window_tile_size, self.window_tile_size
            )
            pr.draw_texture_rec(
                self.texture,
                source_rec,
                pr.Vector2(
                    tile.get("pos_texture_x") * self.window_tile_size,
                    tile.get("pos_texture_y") * self.window_tile_size,
                ),
                pr.WHITE,
            )

    def draw_grid(self) -> None:
        for i in range(int(self.window_height / self.window_tile_size)):
            for j in range(int(self.window_width / self.window_tile_size)):
                pr.draw_rectangle_lines(
                    j * self.window_tile_size + 1,
                    i * self.window_tile_size + 1,
                    self.window_tile_size - 1,
                    self.window_tile_size - 1,
                    pr.RED,
                )
