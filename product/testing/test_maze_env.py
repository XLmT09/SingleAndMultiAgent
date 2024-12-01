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
    """ Test if the maze enviorment is setup as expected. """
    with open('maze/maze_1', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1), 0, 32)
        self.player = CharacterAnimationManager(CHARACTER_WIDTH,
                                                CHARACTER_HEIGHT,
                                                self.maze_map,
                                                True, 500, 700)
        self.player.set_char_animation("idle",
                                       player_sprite_file_paths["idle"], 4)
        self.player.set_char_animation("jump",
                                       player_sprite_file_paths["jump"], 8)
        self.player.set_char_animation("walk",
                                       player_sprite_file_paths["walk"], 6)
        self.player.set_char_animation("climb",
                                       player_sprite_file_paths["climb"], 4)

        self.world = World(self.maze_map)

    def tearDown(self):
        pygame.quit()

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
