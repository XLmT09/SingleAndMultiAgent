import pygame

BLACK = (0, 0, 0)

class Player:
    def __init__(self):
        self.sprite_sheet = pygame.image.load("assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png").convert_alpha()


    def load_image(self, scale, frame, width, height):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(BLACK)
        
        return image