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
    player = Player("assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png", CHARACTER_WIDTH, CHARACTER_HEIGHT, 4)
    player_jump = Player("assets\images\characters\Dude_Monster\Dude_Monster_Jump_8.png", CHARACTER_WIDTH, CHARACTER_HEIGHT, 8)
    player_walk = Player("assets\images\characters\Dude_Monster\Dude_Monster_Walk_6.png", CHARACTER_WIDTH, CHARACTER_HEIGHT, 6)

    last_update = pygame.time.get_ticks()
    cooldown = 120

    # Game loop logic
    while True:
        update_frame = False

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= cooldown:
            last_update = current_time
            update_frame = True

        screen.blit(cave_bg, (0,0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        player_walk.draw_animation(screen, update_frame)

        clock.tick(FPS)
        pygame.display.update() 

game()