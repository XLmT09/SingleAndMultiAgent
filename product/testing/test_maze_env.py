from product.characters import CharacterAnimationManager
from product.world import World
from product.constants import player_sprint_file_paths

import pygame
import unittest
import pickle

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
# Test cases will generate the maze map
maze_map = None


class TestMazeEnviorment(unittest.TestCase):
    with open('maze_1', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1), 0, 32)
        self.player = CharacterAnimationManager(CHARACTER_WIDTH,
                                                CHARACTER_HEIGHT,
                                                self.maze_map,
                                                True, 500, 700)
        self.player.set_char_animation("idle",
                                       player_sprint_file_paths["idle"], 4)
        self.player.set_char_animation("jump",
                                       player_sprint_file_paths["jump"], 8)
        self.player.set_char_animation("walk",
                                       player_sprint_file_paths["walk"], 6)
        self.player.set_char_animation("climb",
                                       player_sprint_file_paths["climb"], 4)

        self.world = World(self.maze_map)

    def tearDown(self):
        pygame.quit()

    def test_maze_has_diamond(self):
        diamond_found = False
        for i in range(len(self.maze_map)):
            for j in range(len(self.maze_map[0])):
                if (self.maze_map[i][j] == 2):
                    diamond_found = True
                    break
        self.assertEqual(True, diamond_found)


if __name__ == '__main__':
    unittest.main()
