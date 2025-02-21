import unittest
import pygame
import pickle
import time

from agent.informed_computer import GreedyComputer, AStarFilledComputer
from characters.character import get_character_types

from world import World
from constants import player_sprite_file_paths, game_values

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32

# Maze map the functions will use
maze_map = None
with open('maze/maze_5', 'rb') as file:
    maze_map = pickle.load(file)
clock = pygame.time.Clock()


class TestFilledGUIComputer():
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

    def testPathFindGUI(self):
        """ This function will run a given path finding algorithm in the
        given initialized maze environment. The test passes if it can collect
        two diamonds without errors. """

        # Max time this test will be allocated (in seconds)
        max_time = 250
        start_time = time.time()

        # Start the path finding algorithm
        self.computer.start_thread()

        # if time limit exceeds this is set to false
        running = True

        # We will stop once all diamonds have been found
        score_count = 0
        TARGET = 37

        # We will run a game loop until collision is detected
        while running:
            self.screen.blit(self.bg, (0, 0))

            # Blitting the tiles
            self.world.load_world(self.screen)

            # Moving the player
            self.game_over, remove_diamond_pos = self.computer.move(
                self.screen,
                self.tile_data,
                asset_groups=self.diamond_positions,
                game_over=self.game_over
            )

            # We have found the diamond and can begin to stop the test
            if self.player.get_is_diamond_found():
                self.world.clear_diamond(remove_diamond_pos[0],
                                         remove_diamond_pos[1])
                self.player.set_is_diamond_found_to_false()
                self.diamond_positions = self.world.get_diamond_group()
                self.computer.update_diamond_list(self.diamond_positions)
                score_count += 1

            # Can end the test once collision is detected
            if score_count == TARGET:
                self.assertTrue("Test passed as all diamonds are collected.")
                self.computer.stop_thread = True
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
        pygame.quit()


class TestGreedyGUIComputer(TestFilledGUIComputer, unittest.TestCase):
    """ This tests the greedy search algo in a filled maze environment. """
    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.computer = GreedyComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond_list=self.world.get_diamond_group()
        )


class TestAStarFilledGUIComputer(TestFilledGUIComputer, unittest.TestCase):
    """ This tests the A* search algo in a filled maze environment. """
    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.computer = AStarFilledComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond_list=self.world.get_diamond_group()
        )
