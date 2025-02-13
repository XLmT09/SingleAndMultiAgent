import pygame
import unittest
import pickle

from characters.character import get_character_types
from world import World
from constants import player_sprite_file_paths
from agent.informed_computer import GreedyComputer

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
# Test cases will generate the maze map
maze_map = None


class TestGreedyTools(unittest.TestCase):
    """ Test tools (functions) in the A star computer class is
    working properly. """

    # Load up a default map for use if child class does not load a maze
    default_maze_map = None
    with open('maze/maze_5', 'rb') as file:
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

        self.player = get_character_types()["main"](
            CHARACTER_WIDTH,
            CHARACTER_HEIGHT,
            self.maze_map if self.maze_map else self.default_maze_map,
            True, player_pos_x,
            player_pos_y
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

        self.world = World(
            self.maze_map if self.maze_map else self.default_maze_map
        )

        # We need to know the goal state for these tests so get the
        # diamond object.
        self.diamond = self.world.get_diamond_group().sprites()[0]

        self.computer = GreedyComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond_list=self.world.get_diamond_group()
        )

    def test_all_manhattan_function_in_small_maze(self):
        """ This function should give the correct coord of the closet diamond
        using the manhattan distance based on the location of the player.
        """
        coord = self.computer.get_manhattan_distance_of_all_diamonds()

        self.assertEqual(coord, (5, 5))

    def tearDown(self):
        pygame.quit()
