from characters import CharacterAnimationManager
from world import World
from constants import player_sprite_file_paths
from computer import AStarComputer

import pygame
import unittest
import pickle

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
# Test cases will generate the maze map
maze_map = None


class TestAstarTools(unittest.TestCase):
    """ Test tools (functions) in the A star computer class is
    working properly. """

    # Load up a default map for use if child class does not load a maze
    default_maze_map = None
    with open('maze/maze_1', 'rb') as file:
        default_maze_map = pickle.load(file)
    maze_map = None

    def setUp(self, player_pos_x=350, player_pos_y=300):
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

        # We need to know the goal state for these tests so get the
        # diamond object.
        self.diamond = self.world.get_diamond_group().sprites()[0]

        self.computer = AStarComputer(self.player,
                                      self.world.get_walkable_maze_matrix(),
                                      self.diamond)

    def test_manhattan_function_in_small_maze(self):
        """ Distance should be 10 because:
        player_pos = (6, 5) and goal = (14, 3)

        distance = |6 - 14| + |5 - 3| = 10
        """
        distance = self.computer.get_manhattan_distance()
        self.assertEqual(distance, 10)

    def test_manhattan_function_start_and_goal_at_same_pos(self):
        self.player.grid_x = self.diamond.grid_x
        self.player.grid_y = self.diamond.grid_y
        distance = self.computer.get_manhattan_distance()
        self.assertEqual(distance, 0)

    def test_manhattan_horizontal_move(self):
        """ Distance should be |player.grid_x - diamond_grid_x| because
        difference in y values are 0.
        """
        self.player.grid_y = self.diamond.grid_y
        distance = self.computer.get_manhattan_distance()
        self.assertEqual(distance,
                         abs(self.player.grid_x - self.diamond.grid_x))

    def test_manhattan_vertical_move(self):
        """ Distance should be |player.grid_y - diamond_grid_y| because
        difference in x values are 0.
        """
        self.player.grid_x = self.diamond.grid_x
        distance = self.computer.get_manhattan_distance()
        self.assertEqual(distance,
                         abs(self.player.grid_y - self.diamond.grid_y))

    def tearDown(self):
        pygame.quit()
