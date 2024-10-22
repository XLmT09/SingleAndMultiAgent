import pygame
from characters import CharacterAnimationManager
from world import World
from computer import Computer
from text import Text

pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
CHARACTER_WIDTH = 32 
CHARACTER_HEIGHT = 32
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Maze Game")

# Background image for the game
cave_bg = pygame.image.load(r"product\assets\images\background\cave.png").convert_alpha()

data = [
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 0, 0 , 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 1, 1, 1 , 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 0, 0 , 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 0, 0 , 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = CharacterAnimationManager(CHARACTER_WIDTH, CHARACTER_HEIGHT, data, True, 500, 700)
player.set_char_animation("idle", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png", 4)
player.set_char_animation("jump", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Jump_8.png", 8)
player.set_char_animation("walk", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Walk_6.png", 6)
player.set_char_animation("climb", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Climb_4.png", 4)

world = World(data)
# world.print_walkable_maze_matrix()
computer = Computer(player, world.get_walkable_maze_matrix())
computer.bfs_path_find()

def game():
    game_over = 0
    tile_data = world.get_collidable_tile_list()
    diamond_positons = world.get_diamond_group()
    score_text = Text(24)
    computer.set_movement_thread_to_bfs()
    # Game loop logic
    while True:
        screen.blit(cave_bg, (0,0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if player.get_is_diamond_found():
            world.update_diamond_position()
            player.set_is_diamond_found_to_false()
            diamond_positons = world.get_diamond_group()
            world.print_walkable_maze_matrix()

        world.load_world(screen)

        world.draw_grid(screen, SCREEN_HEIGHT, SCREEN_WIDTH)
        #game_over = player.draw_animation(screen, tile_data, diamond_positons, game_over)
        game_over = computer.move(screen, tile_data, diamond_positons, game_over)

        score_text.draw(screen, f"Score {player.get_player_score()}", 20, 20)

        clock.tick(FPS)
        pygame.display.update() 

game()