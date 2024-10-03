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

    def draw_animation(self, screen, update_frame):
        # Update the frame once frame rate reached
        # Once recah the end of the animation steps go back to the beggining
        if update_frame: 
            self.frame_counter = (self.frame_counter + 1) % self.steps
    
        screen.blit(self.animation_list[self.frame_counter], (0, 0))