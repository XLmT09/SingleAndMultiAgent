import pygame
import pickle
import argparse
import time

from world import World
from agent.computer import get_agent_types
from characters.character import get_character_types
from constants import player_sprite_file_paths, game_values
from text import Text
from lock import visited_and_path_data_flag

# Setup some initial pygame logic, which is needed
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
        choices=[
            "small", "medium", "large",
            "small-filled", "medium-filled", "large-filled"
        ],
        required=True,
        help="Choose a size: small, medium, or large"
    )

    # define the algo flag
    parser.add_argument(
        "--algo",
        choices=["random", "dfs", "bfs", "ucs", "astar", "greedy"],
        required=False,
        help="Choose a algorithm: random, dfs, bfs, or ucs"
    )

    parser.add_argument(
        "--weighted",
        action="store_true",
        help="Use a weighted manhattan (x2) to influence the "
             "pathfinding (only applicable to A*)."
    )

    # define the algo flag
    parser.add_argument(
        "--highlight",
        action="store_true",
        required=False,
        help="Highlights the visited grids and final path before moving the"
             " agent"
    )

    parser.add_argument(
        "--enemy_count",
        type=int,
        default=0,
        required=False,
        help="The number of enemies to appear in the game."
    )

    # parse args from command line
    args = parser.parse_args()

    screen_width, screen_height, maze, filled = None, None, None, False

    # setup the window width and height, depending on
    # the size the user specified.
    if "small" in args.size:
        screen_width = 850
        screen_height = 350
        # retrieve the small maze filled with diamonds
        if "filled" in args.size:
            maze = "maze/maze_5"
            filled = True
        else:
            maze = "maze/maze_1"
    elif "medium" in args.size:
        screen_width = 1000
        screen_height = 750
        if "filled" in args.size:
            maze = "maze/maze_6"
            filled = True
        else:
            maze = "maze/maze_2"
    elif "large" in args.size:
        screen_width = 1400
        screen_height = 750
        if "filled" in args.size:
            maze = "maze/maze_7"
            filled = True
        else:
            maze = "maze/maze_3"

    if args.weighted and args.algo != "astar":
        parser.error("--weighted is only applicable when using the "
                     "A* algorithm.")

    if ((not args.algo and args.highlight) or
       (args.algo == "random" and args.highlight)):
        parser.error(
            "--highlight is only applicable when using any algorithm but "
            "random."
        )

    filled_compatible_algos = ["greedy", "random", "astar"]
    if (args.algo and filled and not (args.algo in filled_compatible_algos)):
        parser.error(
            "Filled maze only works when user controlled or when using "
            "greedy algorithm."
        )

    # If we are in a filled maze and using astar then update astar to work in
    # a filled maze context.
    if filled and args.algo == "astar":
        args.algo = "astarFilled"

    return {
        "maze_path": maze,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "algo": args.algo,
        "enable_highlighter": args.highlight,
        "weighted": args.weighted,
        "filled": filled,
        "enemy_count": args.enemy_count
    }


def create_characters(config, maze_array) -> list:
    """ Initialise all the characters that will be used in the game """
    character_list = []

    # Initialize the player we or the agent will control
    player = get_character_types()["main"](
        game_values["character_width"],
        game_values["character_height"],
        maze_array,
        is_controlled_by_computer=True if config["algo"] else False,
        x=350, y=300,
        in_filled_maze=config["filled"]
    )

    # Setup the sprite animations for the player
    player.set_char_animation(
        "idle",
        player_sprite_file_paths["idle"],
        animation_steps=4
    )
    player.set_char_animation(
        "jump",
        player_sprite_file_paths["jump"],
        animation_steps=8
    )
    player.set_char_animation(
        "walk",
        player_sprite_file_paths["walk"],
        animation_steps=6
    )
    player.set_char_animation(
        "climb",
        player_sprite_file_paths["climb"],
        animation_steps=4
    )

    character_list.append(player)

    # Now create the enemies
    for _ in range(config["enemy_count"]):
        enemy = get_character_types()["enemy"](
            game_values["character_width"],
            game_values["character_height"],
            maze_array,
            is_controlled_by_computer=True,
            x=450, y=300,
            in_filled_maze=config["filled"]
        )

        enemy.set_char_animation(
            "idle",
            "assets/images/characters/Pink_Monster/Pink_Monster_Idle_4.png",
            animation_steps=4
        )
        enemy.set_char_animation(
            "walk",
            "assets/images/characters/Pink_Monster/Pink_Monster_Walk_6.png",
            animation_steps=6
        )
        enemy.set_char_animation(
            "climb",
            "assets/images/characters/Pink_Monster/Pink_Monster_Climb_4.png",
            animation_steps=4
        )

        character_list.append(enemy)

    return character_list


def setup_game(config) -> dict:
    """ Initialize key variables needed for this application. """

    # This variable represents the agent
    computer = None

    # This is the screen the game will be displayed
    screen = pygame.display.set_mode(
        (config["screen_width"], config["screen_height"])
    )

    # Get the maze array under the maze directory
    maze_array = None
    with open(config["maze_path"], 'rb') as file:
        maze_array = pickle.load(file)

    # Generate the maze
    world = World(maze_array)

    character_list = create_characters(config, maze_array)

    player = character_list[0]

    # If algo was specified, initialize a specific computer class and pass
    # arguments to constructor. Else, dont initialize and the user will
    # control the player.
    if config["algo"]:
        computer = get_agent_types()[config["algo"]](
            player,
            world.get_walkable_maze_matrix(),
            perform_analysis=False,
            diamond=world.get_diamond_group().sprites()[0],
            diamond_list=world.get_diamond_group(),
            is_weighted=config["weighted"]
        )

    enemy_computers = []

    for enemy in character_list[1:]:
        enemy_computer = get_agent_types()["random"](
            enemy,
            world.get_walkable_maze_matrix(),
        )
        enemy_computers.append(enemy_computer)

    return {
        "screen": screen,
        "player": player,
        "world": world,
        "computer": computer,
        # flag is indicate when to freeze the game
        "game_over": 0,
        # This object displays score on screen
        "score_text": Text(24),
        # Background image for the game
        "cave_bg": pygame.image.load(
            "assets/images/background/cave.png"
        ).convert_alpha(),
        "enemy_computers": enemy_computers
    }


def highlight_visited_and_final_path(enable_highlight, world, screen,
                                     computer):
    """ This function highlights the visited grids and final path, if
    collision with diamond is detected AND the visited/path lists have been
    generated. Otherwise we check again on the next iteration. """
    if enable_highlight and not visited_and_path_data_flag.is_set():

        was_executed = world.highlight_grids_visited_by_algo(
            screen,
            *(computer.get_visited_grids_and_path_to_goal())
        )

        # Only set to false if the highlight animation ran, if it didn't it
        # means the algorithm is still generating the final path.
        if was_executed:
            enable_highlight = False
            visited_and_path_data_flag.set()


def start_game_agent(
        screen_width, screen_height, enable_highlighter,
        screen, player, world, computer, game_over, score_text,
        cave_bg, enemy_computers) -> None:
    """ This is the main game function when the computer controls the player,
    the game loop resides in here. """

    tile_data = world.get_collidable_tile_list()
    diamond_positions = world.get_diamond_group()

    enable_highlight = True

    # Wait until final path is found so we can highlight it, if the
    # highlighter flag was set.
    if enable_highlighter:
        while not computer._path_generated:
            print("waiting")

    # Measure run time of the application
    start = time.time()

    # Game loop logic
    while True:
        # We want to draw the background first, then
        # draw everything on top of it.
        screen.blit(cave_bg, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_over:
                computer.stop_path_find_algo_thread()

                for enemy_computer in game_data["enemy_computers"]:
                    enemy_computer.stop_path_find_algo_thread()

                pygame.quit()
                quit()

        # Check for user keyboard input
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            computer.stop_path_find_algo_thread()

        # Draw the maze on the screen
        world.load_world(screen)

        world.draw_grid(screen, screen_height, screen_width)

        for enemy_computer in enemy_computers:
            enemy_computer.move(
                screen,
                tile_data
            )

        # Move and draw the agent
        game_over, remove_diamond_pos = computer.move(
            screen,
            tile_data,
            asset_groups=diamond_positions,
            game_over=game_over,
            enemy_computers=enemy_computers
        )

        # When the diamond is found we will call to regenerate
        # at a new position.
        if player.get_is_diamond_found():
            if computer.perform_analysis:
                end = time.time()
                print(f"Time ran is: {abs(start - end)}")
                start = end

            if not player.in_filled_maze:
                if world.update_diamond_position(
                   are_locations_defined=False) == 2:
                    game_over = 1
                    computer.stop_path_find_algo_thread()
            else:
                world.clear_diamond(remove_diamond_pos[0],
                                    remove_diamond_pos[1])

            player.set_is_diamond_found_to_false()
            diamond_positions = world.get_diamond_group()
            computer.update_diamond_list(diamond_positions)
            enable_highlight = True

        if enable_highlighter:
            highlight_visited_and_final_path(
                enable_highlight,
                world,
                screen,
                computer
            )

        # score test seen on the top left of the screen
        score_text.draw(screen, f"Score {player.get_player_score()}", 20, 20)

        # Set the game refresh rate
        clock.tick(game_values["FPS"])

        # Now render all changes we made in this loop
        # iteration onto the game screen.
        pygame.display.update()


def start_game_player(screen_width, screen_height, screen, player, world,
                      computer, game_over, score_text, cave_bg) -> None:
    """ This is the main game function when the user controls the player, the
    game loop resides in here. """

    tile_data = world.get_collidable_tile_list()
    diamond_positions = world.get_diamond_group()
    remove_diamond_pos = None

    # Game loop logic
    while True:
        # We want to draw the background first, then
        # draw everything on top of it.
        screen.blit(cave_bg, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Draw the maze on the screen
        world.load_world(screen)

        world.draw_grid(screen, screen_height, screen_width)

        # Move and draw the agent
        game_over, remove_diamond_pos = player.draw_animation(
            screen,
            tile_data,
            diamond_positions,
            game_over
        )

        # When the diamond is found we will call to regenerate
        # at a new position.
        if player.get_is_diamond_found():
            if not player.in_filled_maze:
                if world.update_diamond_position(
                   are_locations_defined=False) == 2:
                    game_over = 1
            else:
                world.clear_diamond(remove_diamond_pos[0],
                                    remove_diamond_pos[1])
            player.set_is_diamond_found_to_false()
            diamond_positions = world.get_diamond_group()

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

    if config["algo"]:
        # Start the agent thread
        game_data["computer"].start_thread()

        for enemy_computer in game_data["enemy_computers"]:
            enemy_computer.start_thread()

        start_game_agent(
            config["screen_width"],
            config["screen_height"],
            config["enable_highlighter"],
            **game_data
        )
    else:
        start_game_player(
            config["screen_width"],
            config["screen_height"],
            **game_data
        )
