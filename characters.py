import pygame

BLACK = (0, 0, 0)

class Player:
    def __init__(self, sprite_sheet, width, height, animation_steps):
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.width = width
        self.height = height
        self.steps = animation_steps
        # List of animation images to cycle through
        self.animation_list = [self.load_image(step, 2, False) for step in range(self.steps)]
        self.animation_list_left = [self.load_image(step, 2, True) for step in range(self.steps)]
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
    def __init__(self, width, height, x = 0, y = 0):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        # character hitbox
        # add offset to width and height to make hitbox smaller
        self.hitbox_width = width + 4
        self.hitbox_height = height + 23
        self.hitbox_rect = pygame.Rect(x + 13, 
                                       y + 10, 
                                       self.hitbox_width, 
                                       self.hitbox_height)

        self.animation_actions = {}
        self.requested_animation = "idle"
        self.vel_y = 0
        self.look_left = False
        self.jumped = False

    def set_char_animation(self, animation_desciption, sprite_sheet, animation_steps):
        self.animation_actions[animation_desciption] = Player(sprite_sheet, self.width, self.height, animation_steps)
    
    def draw_animation(self, screen, world_tile_data, update_frame):
        self.requested_animation = "idle"
        dx, dy = 0, 0 

        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.requested_animation = "walk"
            self.look_left = False
            dx += 1
        if key[pygame.K_LEFT]:
            self.requested_animation = "walk"
            self.look_left = True
            dx -= 1
        if key[pygame.K_SPACE] and self.jumped == False:
            self.requested_animation = "jump"
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for maze collisons
        for tile in world_tile_data:
            # check for collision in x direction
            if tile[1].colliderect(self.hitbox_rect.x + dx, self.hitbox_rect.y, self.hitbox_width, self.hitbox_height):
                dx = 0
            # check for y direction collisons
            if tile[1].colliderect(self.hitbox_rect.x, self.hitbox_rect.y + dy, self.hitbox_width, self.hitbox_height):
                # check if below the ground
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.hitbox_rect.top
                    self.vel_y = 0
                # check if above the ground 
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.hitbox_rect.bottom
                    self.vel_y = 0

        # Stick with jump animation while still in air
        if self.vel_y != 0:
            self.requested_animation = "jump"

        self.rect.x += dx
        self.rect.y += dy
        self.hitbox_rect.x += dx
        self.hitbox_rect.y += dy

        self.animation_actions[self.requested_animation].draw_animation(screen, self.rect, update_frame, self.look_left)
        
