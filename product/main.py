import pygame
import pickle
import time
import os

from world import World
from agent.computer import get_agent_types
from characters.character import get_character_types
from text import Text
from lock import visited_and_path_data_flag
from cli import process_args

import constants as C

# Setup some initial pygame logic, which is needed
# regardless of the options we choose.
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Game")


def create_characters(config, maze_array) -> list:
    """ Initialise all the characters that will be used in the game """
    character_list = []

    # Initialize the player we or the agent will control
    player = get_character_types()["main"](
        C.game_values["character_width"],
        C.game_values["character_height"],
        maze_array,
        is_controlled_by_computer=True if config["algo"] else False,
        x=350, y=300,
        in_filled_maze=config["filled"]
    )

    # Setup the sprite animations for the player
    player.set_char_animation(
        "idle",
        C.player_sprite_file_paths["idle"],
        animation_steps=4
    )
    player.set_char_animation(
        "jump",
        C.player_sprite_file_paths["jump"],
        animation_steps=8
    )
    player.set_char_animation(
        "walk",
        C.player_sprite_file_paths["walk"],
        animation_steps=6
    )
    player.set_char_animation(
        "climb",
        C.player_sprite_file_paths["climb"],
        animation_steps=4
    )

    character_list.append(player)

    enemy_positions = [
        (500, 100),
        (700, 200),
        (100, 300)
    ]

    # Now create the enemies
    for enemy_index in range(config["enemy_count"]):
        x, y = enemy_positions[enemy_index]

        enemy = get_character_types()["enemy"](
            C.game_values["character_width"],
            C.game_values["character_height"],
            maze_array,
            is_controlled_by_computer=True,
            x=x, y=y,
            in_filled_maze=config["filled"]
        )

        enemy.set_char_animation(
            "idle",
            C.pink_enemy_file_sprite_paths["idle"],
            animation_steps=4
        )
        enemy.set_char_animation(
            "walk",
            C.pink_enemy_file_sprite_paths["walk"],
            animation_steps=6
        )
        enemy.set_char_animation(
            "climb",
            C.pink_enemy_file_sprite_paths["climb"],
            animation_steps=4
        )
        enemy.set_char_animation(
            "jump",
            C.pink_enemy_file_sprite_paths["jump"],
            animation_steps=8
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

    enemy_list = []

    is_comp = config["is_comp"]

    state = None

    if len(character_list) > 1:
        enemy_list = character_list[1:]
        enemy_coords = []

        for enemy in character_list[1:]:
            enemy_coords.append(enemy.get_player_grid_coordinates())

        # If both the agent and enemy are intelligent we need to set up a state
        # for both agent types to use.
        state = {
            "main_agent": player.get_player_grid_coordinates(),
            "enemies": enemy_coords,
            "diamond_coords": [
                (dmd.grid_y, dmd.grid_x) for dmd in world.get_diamond_group()
            ],
            "score": 0,
            "win": False,
            "lose": False,
            "diamond_count": 0
        }

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
            is_weighted=config["weighted"],
            enemy_list=character_list[1:] if len(character_list) > 1 else [],
            state=state,
            agent_type=0,  # 0 is the main agent
            num_characters=len(character_list)
        )

    enemy_computers = []

    enemy_algo = "random"
    if is_comp:
        enemy_algo = config["algo"]

    for enemy_index, enemy in enumerate(character_list[1:]):
        enemy_computer = get_agent_types()[enemy_algo](
            enemy,
            world.get_walkable_maze_matrix(),
            state=state,
            agent_type=enemy_index + 1,  # 1 is the first enemy
            num_characters=len(character_list)
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
        "enemy_computers": enemy_computers,
        "enemy_list": enemy_list,
        "is_comp": is_comp
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
        cave_bg, enemy_computers, enemy_list, is_comp) -> None:
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

    state = None

    # Game loop logic
    while True:
        # We want to draw the background first, then
        # draw everything on top of it.
        screen.blit(cave_bg, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_over:
                print(C.GAME_OVER)
                print(f"Score: {player.get_player_score()}")
                os._exit(0)

        if game_over:
            print(C.GAME_OVER)
            print(f"Score: {player.get_player_score()}")
            os._exit(0)

        # Check for user keyboard input
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            computer.stop_path_find_algo_thread()

        # Draw the maze on the screen
        world.load_world(screen)

        world.draw_grid(screen, screen_height, screen_width)

        if enemy_computers:
            if is_comp:
                enemy_coords = []
                # Before updating the state we need to gather all the enemy
                # coords
                for enemy in enemy_list:
                    enemy_coords.append(enemy.get_player_grid_coordinates())

                state = {
                    "main_agent": player.get_player_grid_coordinates(),
                    "enemies": enemy_coords,
                    "diamond_coords": world.get_diamond_coords(),
                    "score": 0,
                    "win": False,
                    "lose": False,
                    "diamond_count": 0
                }

                computer.update_state(state)

            for enemy_computer in enemy_computers:
                if is_comp:
                    enemy_computer.update_state(state)

                enemy_computer.move(
                    screen,
                    tile_data,
                )

        # Move and draw the agent
        game_over, remove_diamond_pos = computer.move(
            screen,
            tile_data,
            asset_groups=diamond_positions,
            game_over=game_over,
            enemy_computers=enemy_computers
        )

        player.draw_outline(screen)

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
        clock.tick(C.game_values["FPS"])

        # Now render all changes we made in this loop
        # iteration onto the game screen.
        pygame.display.update()


def start_game_player(screen_width, screen_height,
                      screen, player, world, computer, game_over, score_text,
                      cave_bg, enemy_computers, enemy_list, is_comp) -> None:
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
            if event.type == pygame.QUIT or game_over:
                print(C.GAME_OVER)
                print(f"Score: {player.get_player_score()}")
                os._exit(0)

        if game_over:
            print(C.GAME_OVER)
            print(f"Score: {player.get_player_score()}")
            os._exit(0)

        # Draw the maze on the screen
        world.load_world(screen)

        world.draw_grid(screen, screen_height, screen_width)

        # Move and draw the agent
        game_over, remove_diamond_pos = player.draw_animation(
            screen=screen,
            world_tile_data=tile_data,
            asset_groups=diamond_positions,
            game_over=game_over,
            enemy_computers=enemy_computers
        )

        for enemy_computer in enemy_computers:
            enemy_computer.move(
                screen,
                tile_data,
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
        clock.tick(C.game_values["FPS"])

        # Now render all changes we made in this loop
        # iteration onto the game screen.
        pygame.display.update()


if __name__ == "__main__":
    config = process_args()
    game_data = setup_game(config)

    # start enemy agents if they exist
    for enemy_computer in game_data["enemy_computers"]:
        enemy_computer.start_thread()

    if config["algo"]:
        # Start the agent thread
        game_data["computer"].start_thread()

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
