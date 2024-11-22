import pygame
from characters import CharacterAnimationManager
from world import World
from computer import *
from text import Text
import pickle

pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750
CHARACTER_WIDTH = 32 
CHARACTER_HEIGHT = 32
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Maze Game")

# Background image for the game
cave_bg = pygame.image.load("product/assets/images/background/cave.png").convert_alpha()

data = None
with open('maze_3', 'rb') as file:
    data = pickle.load(file)

player = CharacterAnimationManager(CHARACTER_WIDTH, CHARACTER_HEIGHT, data, True, 480, 600)
player.set_char_animation("idle", "product/assets/images/characters/Dude_Monster/Dude_Monster_Idle_4.png", 4)  
player.set_char_animation("jump", "product/assets/images/characters/Dude_Monster/Dude_Monster_Jump_8.png", 8)
player.set_char_animation("walk", "product/assets/images/characters/Dude_Monster/Dude_Monster_Walk_6.png", 6)
player.set_char_animation("climb", "product/assets/images/characters/Dude_Monster/Dude_Monster_Climb_4.png", 4)

world = World(data)
world.print_walkable_maze_matrix()
computer = UCSComputer(player, world.get_walkable_maze_matrix())
computer.start_thread()
#computer.bfs_path_find()

def game():
    game_over = 0
    tile_data = world.get_collidable_tile_list()
    diamond_positons = world.get_diamond_group()
    score_text = Text(24)
    # Game loop logic
    while True:
        screen.blit(cave_bg, (0,0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                computer.stop_path_find_algo_thread()
                pygame.quit()
                quit()
        
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            computer.stop_path_find_algo_thread()
        
        if player.get_is_diamond_found():
            world.update_diamond_position()
            player.set_is_diamond_found_to_false()
            diamond_positons = world.get_diamond_group()
            world.print_walkable_maze_matrix()
        
        #player.draw_outline(screen)

        world.load_world(screen)

        world.draw_grid(screen, SCREEN_HEIGHT, SCREEN_WIDTH)
        #game_over = player.draw_animation(screen, tile_data, diamond_positons, game_over)
        game_over = computer.move(screen, tile_data, diamond_positons, game_over)

        score_text.draw(screen, f"Score {player.get_player_score()}", 20, 20)

        clock.tick(FPS)
        pygame.display.update() 

game()