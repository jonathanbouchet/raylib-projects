import random 
import pyray as pr


class Cell:
    def __init__(
        self,
        id: int,
        position: pr.Vector2,
        size: pr.Vector2,
        offset_x: int,
        offset_y: int,
        color: pr.Color,
    ) -> None:
        self.id = id
        self.position = position
        self.size = size
        self.color = color
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.state_changed: bool = False
        self.is_clicked: bool = False
        self.is_highlighted: bool = False
        self.is_disable: bool = False
        self.rect = pr.Rectangle(
            self.position.x + self.offset_x,
            self.position.y + self.offset_y,
            self.size.x,
            self.size.y,
        )

    def get_colored_clicked(self) -> None:
        if self.is_clicked:
            return self.color

    def update(self) -> None:
        # print(f"{pr.check_collision_point_rec(pr.get_mouse_position(), self.rect)}, {pr.is_mouse_button_pressed(0)}")
        if not self.is_disable:
            if pr.check_collision_point_rec(pr.get_mouse_position(), self.rect):
                self.is_highlighted = True
                if pr.is_mouse_button_pressed(0):
                    self.state_changed = not self.state_changed
                    self.is_clicked = True
                    self.is_disable = True
            else:
                self.is_highlighted = False

    def draw(self):
        pr.draw_rectangle_rec(self.rect, self.color)
        if self.is_highlighted:
            pr.draw_rectangle_lines_ex(self.rect, 2, pr.RAYWHITE)
        if self.is_clicked:
            pr.draw_text(
                f"{self.color.r},{self.color.g},{self.color.b}",
                int(self.rect.x) + 5,
                int(self.rect.y) + 5,
                10,
                pr.BLACK,
            )
            pr.draw_text(
                f"id={self.id}",
                int(self.rect.x) + 5,
                int(self.rect.y) + 20,
                10,
                pr.BLACK,
            )


class ColorContainer:
    def __init__(
        self,
        position: pr.Vector2,
        value: int,
        outline_color: pr.Color,
        base_color: pr.Color,
    ) -> None:
        self.position = position
        self.value = value
        self.outline_color = outline_color
        self.base_color = base_color
        self.interactive_area: list[Cell] = []#make_cells() 
        self.is_picked: bool = False
        self.colored_picked: pr.Color = None
        self.id_picked: int = None
        
    def make_cells(self) -> list[Cell]:
        # randomize the position of the true value
        l = [0,1,2,3]
        true_pos = random.choice(l)
        l.remove(true_pos) 
        print(f"{true_pos=}, {l=}")
        cells_position_offset = [
            [20, 20],
            [20 + 80, 20],
            [20, 20 + 80],
            [20 + 80, 20 + 80]
        ]

        # tmp = []
        # add true cell
        self.interactive_area.append(
            Cell(
                id=true_pos,
                position=pr.Vector2(self.position.x, self.position.y),
                size=pr.Vector2(80, 80),
                offset_x=cells_position_offset[true_pos][0],
                offset_y=cells_position_offset[true_pos][1],
                color=self.base_color,
            )) 
        # add fake cells
        for i in l:  
            self.interactive_area.append(
                Cell(
                    id=i,
                    position=pr.Vector2(self.position.x, self.position.y),
                    size=pr.Vector2(80, 80),
                    offset_x=cells_position_offset[i][0],
                    offset_y=cells_position_offset[i][1],
                    color=random.choice([pr.Color(253, 249, 0, 255), pr.Color(200, 122, 255, 255), pr.Color(255, 161, 0, 255)]),
                )
            ) 
        # return tmp
        # tmp = [
        #     Cell(
        #         id=0,
        #         position=pr.Vector2(self.position.x, self.position.y),
        #         size=pr.Vector2(80, 80),
        #         offset_x=20,
        #         offset_y=20,
        #         color=self.base_color,
        #     ),
        #     Cell(
        #         id=1,
        #         position=pr.Vector2(self.position.x, self.position.y),
        #         size=pr.Vector2(80, 80),
        #         offset_x=20 + 80,
        #         offset_y=20,
        #         color=pr.Color(253, 249, 0, 255),
        #     ),
        #     Cell(
        #         id=2,
        #         position=pr.Vector2(self.position.x, self.position.y),
        #         size=pr.Vector2(80, 80),
        #         offset_x=20,
        #         offset_y=20 + 80,
        #         color=pr.Color(200, 122, 255, 255),
        #     ),
        #     Cell(
        #         id=3,
        #         position=pr.Vector2(self.position.x, self.position.y),
        #         size=pr.Vector2(80, 80),
        #         offset_x=20 + 80,
        #         offset_y=20 + 80,
        #         color=pr.Color(255, 161, 0, 255),
        #     ),
        # ]
    # self.is_picked: bool = False
    # self.colored_picked: pr.Color = None
    # self.id_picked: int = None

    def get_colored_picked(self) -> pr.Color:
        if self.is_picked:
            return self.colored_picked

    def update(self) -> None:
        # check if any cell has been clicked
        if not any([c.is_disable for c in self.interactive_area]):
            _ = [c.update() for c in self.interactive_area]

            # find the id and color of the cell that has been clicked
            clicked_vals = [c.is_disable for c in self.interactive_area]
            current_index = clicked_vals.index(any(clicked_vals))
            current_col = self.interactive_area[current_index].get_colored_clicked()

            self.id_picked = current_index
            self.colored_picked = current_col
        else:
            pass
            # if a choice has been made, we display it
            self.is_picked = True
            # print(f"ColorContainer -> id picked: {self.id_picked}, colored picked: {self.colored_picked}")

    def draw(self) -> None:
        # outline
        rect = pr.Rectangle(self.position.x, self.position.y, 200, 200)
        pr.draw_rectangle_lines_ex(rect, 1, self.outline_color)
        _ = [c.draw() for c in self.interactive_area]

        # this works -> do not delete
        # choices: 1 is the correct value, the other are fake colors
        # tl_rect = pr.Rectangle(self.position.x + 20, self.position.y + 20, 80, 80)
        # pr.draw_rectangle_rec(tl_rect, self.base_color)

        # tr_rect = pr.Rectangle(self.position.x + 20 + 80, self.position.y + 20, 80, 80)
        # pr.draw_rectangle_rec(tr_rect, pr.GRAY)

        # bl_rect = pr.Rectangle(self.position.x + 20, self.position.y + 20 + 80, 80, 80)
        # pr.draw_rectangle_rec(bl_rect, pr.DARKGRAY)

        # br_rect = pr.Rectangle(
        #     self.position.x + 20 + 80, self.position.y + 20 + 80, 80, 80
        # )
        # pr.draw_rectangle_rec(br_rect, pr.WHITE)
