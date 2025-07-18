import unittest
import pygame
import pickle
import time

from agent.competitive_computer import (
    MinimaxComputer,
    AlphaBetaComputer,
    ExpectimaxComputer
)
from characters.character import get_character_types

from world import World
from constants import (
    player_sprite_file_paths,
    game_values,
    pink_enemy_file_sprite_paths,
    MAX_PATH_TEST_TIME
)

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32

# Maze map the functions will use
maze_map = None
with open('maze/maze_8_test', 'rb') as file:
    maze_map = pickle.load(file)
clock = pygame.time.Clock()


class TestCompFilledGUIComputer():
    """ Setup class which the other tests classes in this
    file will inherit from.

    Format is similar to main.py, anything not commented here would
    likely be commented ove.r there.
    """
    def setUp(self, pos_x, pos_y):
        """
        Args:
            pos_x (int): x position of the agent.
            pos_y (int): y position of the agent.
        """

        # To avoid frozen screen between tests we will init the display
        # instead of the whole pygame module.
        pygame.display.init()
        self.screen = pygame.display.set_mode((850, 350))

        self.player = get_character_types()["main"](
            CHARACTER_WIDTH,
            CHARACTER_HEIGHT,
            maze_map,
            True,
            pos_x,
            pos_y,
            in_filled_maze=True
        )

        self.player.set_char_animation(
            "idle",
            player_sprite_file_paths["idle"],
            animation_steps=4
        )
        self.player.set_char_animation(
            "jump",
            player_sprite_file_paths["jump"],
            animation_steps=8
        )
        self.player.set_char_animation(
            "walk",
            player_sprite_file_paths["walk"],
            animation_steps=6
        )
        self.player.set_char_animation(
            "climb",
            player_sprite_file_paths["climb"],
            animation_steps=4
        )

        self.world = World(maze_map)
        self.game_over = 0
        self.tile_data = self.world.get_collidable_tile_list()
        self.diamond_positions = self.world.get_diamond_group()

        self.bg = pygame.image.load(
            "assets/images/background/cave.png"
        ).convert_alpha()

        self.enemy_list = []

        enemy_pos = [
            (300, 300),
            (275, 300),
            (450, 300)
        ]

        for enemy_index in range(3):
            x, y = enemy_pos[enemy_index]

            enemy = get_character_types()["enemy"](
                CHARACTER_WIDTH,
                CHARACTER_HEIGHT,
                maze_map,
                is_controlled_by_computer=True,
                x=x, y=y
            )

            enemy.set_char_animation(
                "idle",
                pink_enemy_file_sprite_paths["idle"],
                animation_steps=4
            )
            enemy.set_char_animation(
                "walk",
                pink_enemy_file_sprite_paths["walk"],
                animation_steps=6
            )
            enemy.set_char_animation(
                "climb",
                pink_enemy_file_sprite_paths["climb"],
                animation_steps=4
            )
            enemy.set_char_animation(
                "jump",
                pink_enemy_file_sprite_paths["jump"],
                animation_steps=8
            )

            self.enemy_list.append(enemy)

        enemy_positions = []

        for enemy in self.enemy_list:
            enemy_positions.append(enemy.get_player_grid_coordinates())

        self.enemy = self.enemy_list[0]

        diamond_pos = []

        for dmd in self.world.get_diamond_group():
            diamond_pos.append((dmd.grid_y, dmd.grid_x))

        self.state = {
            "main_agent": self.player.get_player_grid_coordinates(),
            "enemies": enemy_positions,
            "diamond_coords": diamond_pos,
            "score": 0,
            "win": False,
            "lose": False,
            "diamond_count": 0
        }

    def testPathFindGUI(self):
        """ This function will run a given path finding algorithm in the
        given initialized maze environment. The test passes if the enemy
        agents are able to catch the main agent. """

        # Max time this test will be allocated (in seconds)
        max_time = MAX_PATH_TEST_TIME
        start_time = time.time()

        # Start the path finding algorithm
        self.main_computer.start_thread()
        for enemy_computer in self.enemy_computers:
            enemy_computer.start_thread()

        # if time limit exceeds this is set to false
        running = True

        # We will run a game loop until collision is detected
        while running:
            self.screen.blit(self.bg, (0, 0))

            # Blitting the tiles
            self.world.load_world(self.screen)

            # Update diamond list present, as some may have been collected
            dmd_list = []
            for dmd in self.world.get_diamond_group():
                dmd_list.append((dmd.grid_y, dmd.grid_x))

            enemy_positions = []

            for enemy in self.enemy_list:
                enemy_positions.append(enemy.get_player_grid_coordinates())

            # Update the state of the game
            new_state = {
                "main_agent": self.player.get_player_grid_coordinates(),
                "enemies": enemy_positions,
                "diamond_coords": dmd_list,
                "score": 0,
                "win": False,
                "lose": False,
                "diamond_count": 0
            }

            for enemy_computer in self.enemy_computers:
                enemy_computer.update_state(new_state)

                # Moving the enemy
                enemy_computer.move(
                    self.screen,
                    self.tile_data
                )

            self.main_computer.update_state(new_state)

            # Moving the player
            self.game_over, remove_diamond_pos = self.main_computer.move(
                self.screen,
                self.tile_data,
                asset_groups=self.diamond_positions,
                game_over=self.game_over,
                enemy_computers=self.enemy_computers
            )

            # We have found the diamond and can begin to stop the test
            if self.player.get_is_diamond_found():
                self.world.clear_diamond(remove_diamond_pos[0],
                                         remove_diamond_pos[1])
                self.player.set_is_diamond_found_to_false()
                self.diamond_positions = self.world.get_diamond_group()
                self.main_computer.update_diamond_list(self.diamond_positions)

            # End test once enemy collision was detected.
            if self.game_over:
                self.assertTrue(
                    "Test passed as collision with enemy was detected."
                )
                break

            if time.time() - start_time > max_time:
                running = False
                self.assertFalse(f"Time limit of {max_time} seconds exceeded.")

            # Set the game refresh rate
            clock.tick(game_values["FPS"])

            # Now render all changes we made in this loop
            # iteration onto the game screen.
            pygame.display.update()

    def tearDown(self):
        self.main_computer.stop_thread = True
        for enemy_computer in self.enemy_computers:
            enemy_computer.stop_thread = True
        pygame.quit()


class TestMinimaxEnemyGUIComputer(TestCompFilledGUIComputer,
                                  unittest.TestCase):
    """ This tests the minimax computer class. It will test game environments
    with more than one enemy."""

    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.main_computer = MinimaxComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond_list=self.world.get_diamond_group(),
            is_weighted=True,
            state=self.state,
            is_main=True,
            num_characters=4,
            agent_type=0  # 0 = main agent
        )

        self.enemy_computers = []
        for enemy_index in range(3):
            self.enemy_computers.append(
                MinimaxComputer(
                    self.enemy_list[enemy_index],
                    self.world.get_walkable_maze_matrix(),
                    state=self.state,
                    num_characters=4,
                    # 0 is main agent, 1-3 are enemies
                    agent_type=enemy_index + 1
                )
            )


class TestAlphaBetaEnemyGUIComputer(TestCompFilledGUIComputer,
                                    unittest.TestCase):
    """ This tests the alphabeta computer class. It will test game environments
    with more than one enemy."""

    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.main_computer = AlphaBetaComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond_list=self.world.get_diamond_group(),
            is_weighted=True,
            state=self.state,
            is_main=True,
            num_characters=4,
            agent_type=0  # 0 = main agent
        )

        self.enemy_computers = []
        for enemy_index in range(3):
            self.enemy_computers.append(
                AlphaBetaComputer(
                    self.enemy_list[enemy_index],
                    self.world.get_walkable_maze_matrix(),
                    state=self.state,
                    num_characters=4,
                    # 0 is main agent, 1-3 are enemies
                    agent_type=enemy_index + 1
                )
            )


class TestExpectimaxEnemyGUIComputer(TestCompFilledGUIComputer,
                                     unittest.TestCase):
    """ This tests the expectimax computer class. It will test game
     environment with more than one enemy. This should be 100% guarantee as
     the main agent is cornered. The only way this fails if the enemy agents
     make a bad mistake, like walking away from the main agent. Meaning there
     is something wrong with the algorithm."""

    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.main_computer = ExpectimaxComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond_list=self.world.get_diamond_group(),
            is_weighted=True,
            state=self.state,
            is_main=True,
            num_characters=4,
            agent_type=0  # 0 = main agent
        )

        self.enemy_computers = []
        for enemy_index in range(3):
            self.enemy_computers.append(
                ExpectimaxComputer(
                    self.enemy_list[enemy_index],
                    self.world.get_walkable_maze_matrix(),
                    state=self.state,
                    num_characters=4,
                    # 0 is main agent, 1-3 are enemies
                    agent_type=enemy_index + 1
                )
            )
