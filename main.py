import pygame

pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Maze Game")

character_image_sheet = pygame.image.load("assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png").convert_alpha()

# Background image for the game
cave_bg = pygame.image.load(r"assets\images\background\cave.png").convert_alpha()

def game():
    # Game loop logic
    while True:
        screen.blit(cave_bg, (0,0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(character_image_sheet, (0, 10))

        clock.tick(FPS)
        pygame.display.update() 

game()