from characters import CharacterAnimationManager
from world import World
from computer import agent_types
from constants import player_sprite_file_paths, game_values
from text import Text

import pygame
import pickle
import argparse

# Setup some inital pygame logic, which is needed
# regardless of the options we choose.
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Game")


def process_args() -> dict:
    """ This function takes the flags passed in by the user and
    will process them.
    """

    # This is used to define, manage and parser the command line args.
    parser = argparse.ArgumentParser()

    # define the size flag
    parser.add_argument(
        "--size",
        choices=["small", "medium", "large"],
        required=True,
        help="Choose a size: small, medium, or large"
    )

    # define the algo flag
    parser.add_argument(
        "--algo",
        choices=["dfs", "bfs", "ucs"],
        required=True,
        help="Choose a algorithm: dfs, bfs, or ucs"
    )

    # parse args from command line
    args = parser.parse_args()

    screen_width, screen_height, maze = None, None, None

    # setup the window width and height, depending on
    # the size the user specified.
    if args.size == "small":
        screen_width = 850
        screen_height = 350
        maze = "maze/maze_1"
    elif args.size == "medium":
        screen_width = 1000
        screen_height = 750
        maze = "maze/maze_2"
    elif args.size == "large":
        screen_width = 1400
        screen_height = 750
        maze = "maze/maze_3"

    return {
        "maze_path": maze,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "algo": args.algo
    }


def setup_game(config) -> dict:
    """ Initialize key variables needed for this application. """

    # This is the screen the game will be displayed
    screen = pygame.display.set_mode((config["screen_width"],
                                      config["screen_height"]))

    # Get the maze array under the maze directory
    maze_array = None
    with open(config["maze_path"], 'rb') as file:
        maze_array = pickle.load(file)

    # Initialize the player we or the agent will control
    player = CharacterAnimationManager(game_values["character_width"],
                                       game_values["character_height"],
                                       maze_array,
                                       is_controlled_by_computer=True,
                                       x=350, y=300)
    # Setup the sprite animations for the player
    player.set_char_animation("idle", player_sprite_file_paths["idle"],
                              animation_steps=4)
    player.set_char_animation("jump", player_sprite_file_paths["jump"],
                              animation_steps=8)
    player.set_char_animation("walk", player_sprite_file_paths["walk"],
                              animation_steps=6)
    player.set_char_animation("climb", player_sprite_file_paths["climb"],
                              animation_steps=4)

    # Generate the maze
    world = World(maze_array)
    world.print_walkable_maze_matrix()

    # Initialize a specific computer class and pass arguments to constructor
    computer = agent_types[config["algo"]](player,
                                           world.get_walkable_maze_matrix())

    return {
        "screen": screen,
        "player": player,
        "world": world,
        "computer": computer
    }


def start_game(screen_width, screen_height,
               screen, player, world, computer) -> None:
    """ This is the main game function, the game loop resides in here. """

    # Freeze game when game over flag is set
    game_over = 0
    tile_data = world.get_collidable_tile_list()
    diamond_positons = world.get_diamond_group()
    score_text = Text(24)

    # Background image for the game
    cave_bg = pygame.image.load(
        "assets/images/background/cave.png"
        ).convert_alpha()

    # Game loop logic
    while True:
        # We want to draw the background first, then
        # draw everuthing ontop of it.
        screen.blit(cave_bg, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                computer.stop_path_find_algo_thread()
                pygame.quit()
                quit()

        # Check for user keyboard input
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            computer.stop_path_find_algo_thread()

        # When the diamond is found we will call to regenerate
        # at a new position.
        if player.get_is_diamond_found():
            world.update_diamond_position()
            player.set_is_diamond_found_to_false()
            diamond_positons = world.get_diamond_group()
            world.print_walkable_maze_matrix()

        # Draw the maze on the screen
        world.load_world(screen)

        world.draw_grid(screen, screen_height, screen_width)

        # Move and draw the agent
        game_over = computer.move(screen, tile_data,
                                  diamond_positons, game_over)

        # score test seen on the top left of the screen
        score_text.draw(screen, f"Score {player.get_player_score()}", 20, 20)

        # Set the game refresh rate
        clock.tick(game_values["FPS"])

        # Now render all changes we made in this loop
        # iteration onto the game screen.
        pygame.display.update()


if __name__ == "__main__":
    config = process_args()
    game_data = setup_game(config)

    # Start the agent thread
    game_data["computer"].start_thread()

    start_game(config["screen_width"], config["screen_height"], **game_data)
