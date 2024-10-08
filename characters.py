import pygame

BLACK = (0, 0, 0)

class Player:
    def __init__(self, sprite_sheet, width, height, animation_steps):
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.width = width
        self.height = height
        self.steps = animation_steps
        # List of animation images to cycle through
        self.animation_list = [self.load_image(step, 2) for step in range(self.steps)]
        self.frame_counter = 0

    def load_image(self, frame, scale):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), ((frame * self.width), 0, self.width, self.height))
        image = pygame.transform.scale(image, (self.width * scale, self.height * scale))
        image.set_colorkey(BLACK)
        
        return image

    def draw_animation(self, screen, rect, update_frame):
        # Update the frame once frame rate reached
        # Once recah the end of the animation steps go back to the beggining
        if update_frame: 
            self.frame_counter = (self.frame_counter + 1) % self.steps
    
        screen.blit(self.animation_list[self.frame_counter], rect)   

class CharacterAnimationManager:
    def __init__(self, width, height, x = 0, y = 0):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.animation_actions = {}
        self.requested_animation = "idle"

    def set_char_animation(self, animation_desciption, sprite_sheet, animation_steps):
        self.animation_actions[animation_desciption] = Player(sprite_sheet, self.width, self.height, animation_steps)
    
    def draw_animation(self, screen, update_frame):
        dx = 0 

        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            dx += 1
        if key[pygame.K_LEFT]:
            dx -= 1
        
        self.rect.x += dx

        self.animation_actions[self.requested_animation].draw_animation(screen, self.rect, update_frame)
        
