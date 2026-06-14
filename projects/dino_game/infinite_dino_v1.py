import random
import pyray as pr
import raylib as rl
width, height = 800, 300
floor_y_pos = 30

class Sprite:
    def __init__(self, position: pr.Vector2, texture: pr.Texture, color: pr.Color, debug_color: pr.Color):
        self.position = position
        self.texture: pr.Texture = texture
        self.color = color
        self.debug_color = debug_color

    def get_rectangle(self) -> pr.Rectangle:
        return pr.Rectangle(self.position.x, self.position.y, self.texture.width, self.texture.height)
    
    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        pass
    
    def draw(self, dt: float) -> None:
        pr.draw_texture_v(self.texture, self.position, self.color)
        pr.draw_rectangle_lines(int(self.position.x), int(self.position.y), int(self.texture.width), int(self.texture.height), self.debug_color)


class Player(Sprite):
    def __init__(self, position: pr.Vector2, texture: pr.Texture, color: pr.Color, debug_color: pr.Color):
        super().__init__(position=position, texture=texture, color=color, debug_color=debug_color)
        # Physics state
        self.vy: float = 0.0  # vertical velocity (px/s)
        self.gravity: float = 1500.0  # gravity (px/s^2) — tune to taste
        self.jump_speed: float = 500.0  # initial jump impulse (px/s)
        self.is_grounded: bool = False
        self.dead = False
    
    def update(self, dt: float, other: pr.Rectangle) -> None:
        self.move(dt=dt, other=other)

    def check_collision(self, other: pr.Rectangle) -> bool:
        return pr.check_collision_recs(self.get_rectangle(), other)

    def check_collisions_enemies(self, enemies: list[pr.Rectangle]):
        for enemy in enemies:
            # print(f"{enemy.width}, {enemy.height}, {enemy.x, enemy.y}")
            if pr.check_collision_recs(self.get_rectangle(), enemy):
                print(f"{enemy.width}, {enemy.height}, {type(enemy)}")
                print("COLLISION")
                # quick hack to test the dead texture when a collision happens
                dead_texture = pr.load_texture("assets/dino/dino_dead_64x64.png")
                self.texture = dead_texture
                self.dead = True

    def move(self, dt: float,  other: pr.Rectangle):
        # Jump input (use is_key_pressed for single press)
        if pr.is_key_pressed(rl.KEY_SPACE) and self.is_grounded:
            self.vy = -self.jump_speed
            self.is_grounded = False

        # Apply gravity
        self.vy += self.gravity * dt

        # Integrate vertical velocity
        self.position.y += self.vy * dt

        # Simple collision resolution (vertical only)
        if self.check_collision(other):
            # If we hit the platform from above, snap on top and stop vertical velocity
            if self.vy >= 0 and self.position.y + self.texture.height > other.y:
                self.position.y = other.y - self.texture.height
                self.vy = 0.0
                self.is_grounded = True
            else:
                # Basic fallback: prevent penetrating from below (optional improvement)
                self.position.y = other.y + other.tecture.height
                self.vy = 0.0
                self.is_grounded = False
        else:
            self.is_grounded = False

class Cactus(Sprite):
    def __init__(self, position: pr.Vector2, texture: pr.Texture, color: pr.Color, speed: float, scale: float, debug_color: pr.Color):
        super().__init__(position=position, texture=texture, color=color, debug_color=debug_color)
        self.speed = speed
        self.direction = pr.Vector2(-1, 0)
        self.scale = scale
        self.disable = False

    # tuning because rectangle from sprite is too wide
    def get_rectangle(self) -> pr.Rectangle:
        return pr.Rectangle(self.position.x, self.position.y, self.texture.width, self.texture.height)
    
    def update(self, dt: float) -> None:
        # update velocity
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        if self.position.x < 0:
            self.disable = True
    
    def draw(self, dt: float) -> None:
        # reposition the texture after scaling, if necessary
        tmp_pos = pr.Vector2(self.position.x, self.position.y - (self.scale - 1)*self.texture.height)
        pr.draw_texture_ex(self.texture, tmp_pos, 0, self.scale, self.color)
        pr.draw_rectangle_lines(int(tmp_pos.x), int(tmp_pos.y), int(self.texture.width * self.scale), int(self.texture.height*self.scale), self.debug_color)


class Cloud(Sprite):
    def __init__(self, position: pr.Vector2, texture: pr.Texture, speed: float, color: pr.Color,  debug_color: pr.Color):
        super().__init__(position=position, texture=texture, color=color, debug_color=debug_color)
        self.speed = speed
        self.direction = pr.Vector2(-1, 0)
        self.disable = False
    
    def update(self, dt: float) -> None:
        # update velocity
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        if self.position.x < 0:
            self.disable = True


pr.init_window(width, height, "app")
pr.set_target_fps(60)
floor_rect = pr.Rectangle(0, height - floor_y_pos, width, height - floor_y_pos)

cactus_list: list[Cactus] = []
cactus_rect: list[pr.Rectangle] = []

# cloud
cloud_texture = pr.load_texture("assets/dino/cloud_64x64.png")
print(f"{cloud_texture.width}, {cloud_texture.height}")
cloud = Cloud(position = pr.Vector2(width, 20), texture=cloud_texture, color=pr.DARKGRAY, debug_color=pr.YELLOW, speed=20)

#cactus
cactus_texture = pr.load_texture("assets/dino/cactus_12x32.png")
print(f"{cactus_texture.width}, {cactus_texture.height}")

# dino
dino_texture = pr.load_texture("assets/dino/dino_idle_64x64.png")
print(f"{dino_texture.width}, {dino_texture.height}")
player = Player(position=pr.Vector2(100, height - int(dino_texture.height) - 20), texture=dino_texture, color=pr.WHITE, debug_color=pr.BLUE) # spawn on floor
# player = Player(position=pr.Vector2(100, 0), texture=dino_texture, color=pr.WHITE, debug_color=pr.BLUE)

run_time = 0
frame_counter = 0
block_spawn_frame: bool = False

while not pr.window_should_close():
    # logic
    dt = pr.get_frame_time()
    frame_counter += 1
    run_time = pr.get_time()
    if frame_counter % 60 == 0: # spawn a block every frame
        if random.random() < 0.75 and not player.dead:
            cactus = Cactus(
                texture=cactus_texture, 
                position = pr.Vector2(width, height - int(cactus_texture.height) - 20), 
                speed=200, 
                color=pr.WHITE,
                scale=random.uniform(0.8, 1.4),
                debug_color=pr.PINK)
            cactus_list.append(cactus)

    if not player.dead:
        # updates all cactuses
        _ = [cactus.update(dt=dt) for cactus in cactus_list]

        # update player
        player.update(dt=dt, other=floor_rect)
        player.check_collisions_enemies(enemies=[x.get_rectangle() for x in cactus_list])

        # update cloud
        cloud.update(dt=dt)

        # clean list of blocks
        cactus_list = [x for x in cactus_list if x.position.x>0]

    # rendering
    pr.begin_drawing()
    pr.clear_background(pr.Color(211, 211, 211, 255))

    # draw cloud
    cloud.draw(dt=dt)

    # draw floor
    pr.draw_line_v(pr.Vector2(0, height - floor_y_pos), pr.Vector2(width, height - floor_y_pos), pr.BLACK)
    pr.draw_line_v(pr.Vector2(0, int(height/2)), pr.Vector2(width, int(height/2)), pr.RED)

    pr.draw_rectangle_rec(floor_rect, pr.YELLOW)

    # draw cactus
    _ = [cactus.draw(dt=dt) for cactus in cactus_list if not cactus.disable]

    # draw player
    player.draw(dt=dt)

    pr.draw_fps(0,0)
    pr.draw_text(f"time ellapsed:{int(run_time)}",0 ,20, 20, pr.GREEN)
    pr.draw_text(f"frame count:{(int(frame_counter))}",0, 40, 20, pr.GREEN)
    pr.draw_text(f"blocks:{(len(cactus_list))}",0, 60, 20, pr.GREEN)
    pr.end_drawing()

    # reset block spawn timer
    if int(run_time) % 1 == 0:
        block_spawn_frame = False

pr.close_window()