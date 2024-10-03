import pygame

pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Maze Game")

character_image_sheet = pygame.image.load("assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png").convert_alpha()

# Background image for the game
cave_bg = pygame.image.load(r"assets\images\background\cave.png").convert_alpha()

def load_image(character_image_sheet, scale):
    image = pygame.Surface((CHARACTER_WIDTH, CHARACTER_HEIGHT)).convert_alpha()
    image.blit(character_image_sheet, (0, 0), (0, 0, CHARACTER_WIDTH, SCREEN_HEIGHT))
    image = pygame.transform.scale(image, (CHARACTER_WIDTH * scale, CHARACTER_HEIGHT * scale))

    return image


def game():
    # Game loop logic
    while True:
        screen.blit(cave_bg, (0,0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(load_image(character_image_sheet, 2), (0,0))
        clock.tick(FPS)
        pygame.display.update() 

game()