import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ANIMATION_COOLDOWN = 120


class Player:
    def __init__(self, sprite_sheet, width, height, animation_steps):
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.width = width
        self.height = height
        self.steps = animation_steps
        # List of animation images to cycle through
        self.animation_list = [self.load_image(step, 1.7, False) for step in range(self.steps)]
        self.animation_list_left = [self.load_image(step, 1.7, True) for step in range(self.steps)]
        self.frame_counter = 0

    def load_image(self, frame, scale, look_left):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), ((frame * self.width), 0, self.width, self.height))
        image = pygame.transform.scale(image, (self.width * scale, self.height * scale))

        if look_left:
            image = pygame.transform.flip(image, True, False)

        image.set_colorkey(BLACK)
        return image

    def draw_animation(self, screen, rect, update_frame, look_left):
        # Update the frame once frame rate reached
        # Once recah the end of the animation steps go back to the beggining
        if update_frame: 
            self.frame_counter = (self.frame_counter + 1) % self.steps
        
        if look_left:
            screen.blit(self.animation_list_left[self.frame_counter], rect)
            return
    
        screen.blit(self.animation_list[self.frame_counter], rect)   

class CharacterAnimationManager:
    def __init__(self, width, height, maze_data, is_controlled_by_computer, x = 0, y = 0):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width * 1.8, height * 1.8)

        # character hitbox
        # add offset to width and height to make hitbox smaller
        self.hitbox_width = width
        self.hitbox_height = height + 14
        self.hitbox_rect = pygame.Rect(x + 10, 
                                       y + 9, 
                                       self.hitbox_width, 
                                       self.hitbox_height)

        self.animation_actions = {}
        self.requested_animation = "idle"
        self.last_update = pygame.time.get_ticks()
        self.vel_y, self.dx, self.dy = 0, 0, 0
        self.look_left = False
        self.jumped = False
        self.is_controlled_by_computer = is_controlled_by_computer
        self.grid_x = self.hitbox_rect.x // 50
        self.grid_y = self.hitbox_rect.y // 50
        self.maze_data = maze_data
        self._is_diamond_found = False
        self._score = 0

    def set_char_animation(self, animation_desciption, sprite_sheet, animation_steps):
        self.animation_actions[animation_desciption] = Player(sprite_sheet, self.width, self.height, animation_steps)

    def draw_outline(self, screen):
        #pygame.draw.rect(screen, WHITE, self.rect, 2)
        pygame.draw.rect(screen, WHITE, self.hitbox_rect, 2)

    def human_player_movement(self, world_tile_data):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.requested_animation = "walk"
            self.look_left = False
            self.dx += 1
        if key[pygame.K_LEFT]:
            self.requested_animation = "walk"
            self.look_left = True
            self.dx -= 1
        if key[pygame.K_UP] and self.maze_data[self.grid_y][self.grid_x] == 3:
            self.requested_animation = "climb"
            self.dy -= 1
        if key[pygame.K_SPACE] and self.jumped == False:
            self.requested_animation = "jump"
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
    
    def computer_player_movement(self, direction):
        if direction == "RIGHT":
            self.requested_animation = "walk"
            self.look_left = False
            self.dx += 1
        if direction == "LEFT":
            self.requested_animation = "walk"
            self.look_left = True
            self.dx -= 1
        if direction == "UP":
            self.requested_animation = "climb"
            self.dy -= 1
        if direction == "UP RIGHT":
            self.requested_animation = "climb"
            self.dy -= 1
            self.dx += 1
        if direction == "UP LEFT":
            self.requested_animation = "climb"
            self.dy -= 1
            self.dx -= 1
        if direction == "None":
            self.dx, self.dy = 0, 0
            self.requested_animation = "idle"
    
    def draw_animation(self, screen, world_tile_data, world_assets, game_over, direction = None):
        self.requested_animation = "idle"
        update_frame = False
        current_time = pygame.time.get_ticks()
        self.dx = 0
        self.dy = 0

        if game_over != 0:
            self.animation_actions[self.requested_animation].draw_animation(screen, self.rect, update_frame, self.look_left)
            return game_over

        if current_time - self.last_update >= ANIMATION_COOLDOWN:
            self.last_update = current_time
            update_frame = True
        
        # Stick with jump animation while still in air
        if self.vel_y != 0:
            self.requested_animation = "jump"

        if self.is_controlled_by_computer: 
            self.computer_player_movement(direction)
        else:
            self.human_player_movement(world_tile_data)

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        if self.requested_animation != "climb":
            self.dy += self.vel_y

        # check for maze collisons
        for tile in world_tile_data:
            # check for collision in x direction
            if tile[1].colliderect(self.hitbox_rect.x + self.dx, self.hitbox_rect.y, self.hitbox_width, self.hitbox_height):
                self.dx = 0
            # check for y direction collisons
            if tile[1].colliderect(self.hitbox_rect.x, self.hitbox_rect.y + self.dy, self.hitbox_width, self.hitbox_height):
                # check if below the ground
                if self.vel_y < 0 or self.requested_animation == "climb":
                    self.dy = tile[1].bottom - self.hitbox_rect.top
                    self.vel_y = 0
                # check if above the ground 
                elif self.vel_y >= 0:
                    self.dy = tile[1].top - self.hitbox_rect.bottom
                    self.vel_y = 0
        
        if self.look_left:
            self.grid_x = (self.hitbox_rect.x + self.width) // 50
        else:
            self.grid_x = self.hitbox_rect.x // 50
        self.grid_y = self.hitbox_rect.y // 50

        #print(f"grid {self.grid_x}, {self.grid_y}")
        #check for collision with diamond
        if pygame.sprite.spritecollide(self, world_assets, False, pygame.sprite.collide_rect_ratio(0.5)):
            self._is_diamond_found = True
            self._score += 1
            print(self._score)

        self.rect.x += self.dx
        self.rect.y += self.dy
        self.hitbox_rect.x += self.dx
        self.hitbox_rect.y += self.dy

        self.animation_actions[self.requested_animation].draw_animation(screen, self.rect, update_frame, self.look_left)

        return game_over

    def get_is_diamond_found(self) -> bool:
        return self._is_diamond_found
    
    def set_is_diamond_found_to_false(self) -> None:
        self._is_diamond_found = False
    
    def get_player_score(self) -> int:
        return self._score

    def get_player_grid_coordinates(self) -> int:
        return (self.grid_y, self.grid_x)
        
