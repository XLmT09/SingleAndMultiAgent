from characters import CharacterAnimationManager
from world import World
from constants import player_sprite_file_paths

import pygame
import unittest
import pickle
import os

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
# Test cases will generate the maze map
maze_map = None
# The directory all the mazes have been generated into
maze_dir = "maze"


class TestMazeEnviorment(unittest.TestCase):
    """ Test if the maze enviorment and attributes functions as expected. """

    # Load up a default map for use if child class does not load a maze
    default_maze_map = None
    with open('maze/maze_1', 'rb') as file:
        default_maze_map = pickle.load(file)
    maze_map = None

    def setUp(self, player_pos_x, player_pos_y):
        """
        Args:
            pos_x (int): x position of the agent.
            pos_y (int): y position of the agent.
        """
        pygame.init()
        pygame.display.set_mode((1, 1), 0, 32)

        self.player = CharacterAnimationManager(
            CHARACTER_WIDTH,
            CHARACTER_HEIGHT,
            self.maze_map if self.maze_map else self.default_maze_map,
            True, player_pos_x,
            player_pos_y
        )
        self.player.set_char_animation("idle",
                                       player_sprite_file_paths["idle"], 4)
        self.player.set_char_animation("jump",
                                       player_sprite_file_paths["jump"], 8)
        self.player.set_char_animation("walk",
                                       player_sprite_file_paths["walk"], 6)
        self.player.set_char_animation("climb",
                                       player_sprite_file_paths["climb"], 4)

        self.world = World(
            self.maze_map if self.maze_map else self.default_maze_map
        )

    def tearDown(self):
        pygame.quit()


class TestSmallMazeEnviorment(TestMazeEnviorment, unittest.TestCase):
    """ This class will test functions and attributes for the small maze
    enviorment. """

    # Load up the small maze
    with open('maze/maze_1', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300)

    def test_small_get_maze_size(self):
        """ When we call get_maze_size() on a small maze it should output
        as small."""

        self.assertEqual("small", self.world.get_maze_size())

    def test_get_walkable_locations(self):
        self.assertEqual([(1, 1), (1, 2), (1, 3), (1, 5), (1, 6), (1, 7),
                          (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13),
                          (1, 14), (3, 1), (3, 2), (3, 3), (3, 5), (3, 6),
                          (3, 7), (3, 8), (3, 10), (3, 11), (3, 12), (3, 13),
                          (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                          (5, 7), (5, 8), (5, 10), (5, 11), (5, 12), (5, 13),
                          (5, 14)], self.world.get_walkable_locations())


class TestMidMazeEnviorment(TestMazeEnviorment, unittest.TestCase):
    """ This class will test functions and attributes for the medium maze
    enviorment. """

    # Load up the medium maze
    with open('maze/maze_2', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300)

    def test_mid_get_maze_size(self):
        """ When we call get_maze_size() on a medium maze it should output
        as medium."""

        self.assertEqual("medium", self.world.get_maze_size())


class TestLargeMazeEnviorment(TestMazeEnviorment, unittest.TestCase):
    """ This class will test functions and attributes for the large maze
    enviorment. """

    # Load up the large maze
    with open('maze/maze_3', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300)

    def test_large_get_maze_size(self):
        """ When we call get_maze_size() on a large maze it should output
        as large."""

        self.assertEqual("large", self.world.get_maze_size())


class TestEveryMazeEnviormentSize(TestMazeEnviorment, unittest.TestCase):
    """ This class in every test case will loop through every maze size and
    test if common values and functions work as expected."""
    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300)

    def test_every_maze_generated_has_a_diamond(self):
        """ If a maze does not contain an diamond then the algos programmed
        will not behave as expected, so we need to sure every maze generated
        contains an diamond."""

        # loop through every maze file in the maze directory
        for file in os.listdir(maze_dir):
            # get the path of the maze file so we can open the it
            maze_path = os.path.join(maze_dir, file)

            with open(maze_path, "rb") as maze_file:
                # load up the maze matrix
                temp_maze = pickle.load(maze_file)
                diamond_found = False

                # Now loop through the maze and check it contains a diamond
                for i in range(len(temp_maze)):
                    for j in range(len(temp_maze[0])):
                        if (temp_maze[i][j] == 2):
                            diamond_found = True
                            break

                self.assertEqual(True, diamond_found)


if __name__ == '__main__':
    unittest.main()
