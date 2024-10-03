import pygame
from characters import Player

pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
FPS = 60
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Maze Game")

# Background image for the game
cave_bg = pygame.image.load(r"assets\images\background\cave.png").convert_alpha()


def game():
    player = Player()
    animation_list = []
    steps = 4
    last_update = pygame.time.get_ticks()
    cooldown = 120
    frame = 0

    for step in range(steps):
        animation_list.append(player.load_image(2, step, 32, 32))

    # Game loop logic
    while True:
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= cooldown:
            frame += 1
            last_update = current_time
            if frame == 4:
                frame = 0

        screen.blit(cave_bg, (0,0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(animation_list[frame], (0, 0))

        clock.tick(FPS)
        pygame.display.update() 

game()