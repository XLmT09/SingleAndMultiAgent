import unittest
import pygame
import pickle
import time

from agent.competitive_computer import MinimaxComputer, AlphaBetaComputer
from characters.character import get_character_types

from world import World, Diamond
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
            (200, 200),
            (100, 200),
            (400, 400)
        ]

        for enemy_index in range(1):
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
            "diamond_positions": diamond_pos,
            "score": 0,
            "win": False,
            "lose": False,
            "diamond_count": 0
        }

    def testPathFindGUI(self):
        """ This function will run a given path finding algorithm in the
        given initialized maze environment. The test passes if it can collect
        two diamonds without errors. """

        # Max time this test will be allocated (in seconds)
        max_time = MAX_PATH_TEST_TIME
        start_time = time.time()

        # Start the path finding algorithm
        self.main_computer.start_thread()
        self.enemy_computer.start_thread()

        # if time limit exceeds this is set to false
        running = True

        # On every test iterations load diamonds on these specific areas for
        # the test.
        diamond = Diamond(11, 5)
        self.world._diamond_group.add(diamond)

        diamond = Diamond(12, 5)
        self.world._diamond_group.add(diamond)

        diamond = Diamond(13, 5)
        self.world._diamond_group.add(diamond)

        # We will stop once all diamonds have been found
        score_count = 0

        # The game state will have more than 3 diamonds, but for the algo to
        # pass it just needs to collect 3.
        TARGET = 3

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
                "diamond_positions": dmd_list,
                "score": 0,
                "win": False,
                "lose": False,
                "diamond_count": 0
            }

            # Moving the enemy
            self.enemy_computer.move(
                self.screen,
                self.tile_data
            )

            self.enemy_computer.update_state(new_state)
            self.main_computer.update_state(new_state)

            # Moving the player
            self.game_over, remove_diamond_pos = self.main_computer.move(
                self.screen,
                self.tile_data,
                asset_groups=self.diamond_positions,
                game_over=self.game_over,
                enemy_computers=[self.enemy_computer]
            )

            # We have found the diamond and can begin to stop the test
            if self.player.get_is_diamond_found():
                self.world.clear_diamond(remove_diamond_pos[0],
                                         remove_diamond_pos[1])
                self.player.set_is_diamond_found_to_false()
                self.diamond_positions = self.world.get_diamond_group()
                self.main_computer.update_diamond_list(self.diamond_positions)
                score_count += 1

            # Can end the test once collision is detected
            if score_count == TARGET:
                self.assertTrue("Test passed as all diamonds are collected.")
                self.main_computer.stop_thread = True
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
        self.enemy_computer.stop_thread = True
        pygame.quit()


class TestMinimaxGUIComputer(TestCompFilledGUIComputer, unittest.TestCase):
    """ This tests the minimax computer class. It will check the main agent is
    able to collect at least 3 diamonds in the maze, this should be possible
    as there are no dead ends in the game."""

    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.main_computer = MinimaxComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond_list=self.world.get_diamond_group(),
            is_weighted=True,
            state=self.state,
            agent_type=0,
            num_characters=2
        )

        self.enemy_computer = MinimaxComputer(
            self.enemy_list[0],
            self.world.get_walkable_maze_matrix(),
            state=self.state,
            num_characters=2,
            agent_type=1
        )


class TestAlphaBetaGUIComputer(TestCompFilledGUIComputer, unittest.TestCase):
    """ This tests the alphabeta computer class. It will check the main agent
    is able to collect at least 3 diamonds in the maze, this should be
    possible as there are no dead ends in the game."""

    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.main_computer = AlphaBetaComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond_list=self.world.get_diamond_group(),
            is_weighted=True,
            state=self.state,
            agent_type=0,
            num_characters=2
        )

        self.enemy_computer = AlphaBetaComputer(
            self.enemy_list[0],
            self.world.get_walkable_maze_matrix(),
            state=self.state,
            num_characters=2,
            agent_type=1
        )
