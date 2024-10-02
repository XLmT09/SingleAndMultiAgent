import pygame

pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# Setting size for the window/Dispaly
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

def game():
    # Game loop logic
    while True:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update() 

game()