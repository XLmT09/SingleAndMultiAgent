from characters import CharacterAnimationManager
from world import World
from agent.informed_computer import AStarFilledComputer
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


class TestMazeEnvironment(unittest.TestCase):
    """ Test if the maze environment and attributes functions as expected. """

    # Load up a default map for use if child class does not load a maze
    default_maze_map = None
    with open('maze/maze_1', 'rb') as file:
        default_maze_map = pickle.load(file)
    maze_map = None

    def setUp(self, player_pos_x, player_pos_y, in_filled_maze=False):
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
            player_pos_y,
            in_filled_maze=in_filled_maze
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


class TestSmallMazeEnvironment(TestMazeEnvironment, unittest.TestCase):
    """ This class will test functions and attributes for the small maze
    environment. """

    # Load up the small maze
    with open('maze/maze_1', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300)

    def test_small_get_maze_size(self):
        """ When we call get_maze_size() on a small maze it should output
        as small."""

        self.assertEqual("small", self.world.get_maze_size())

    def test_small_get_walkable_locations(self):
        """ Check get_walkable_locations() outputs the correct list of
        vertices for a small maze."""
        self.assertEqual([(1, 1), (1, 2), (1, 3), (1, 5), (1, 6), (1, 7),
                          (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13),
                          (1, 14), (3, 1), (3, 2), (3, 3), (3, 5), (3, 6),
                          (3, 7), (3, 8), (3, 10), (3, 11), (3, 12), (3, 13),
                          (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                          (5, 7), (5, 8), (5, 10), (5, 11), (5, 12), (5, 13),
                          (5, 14)], self.world.get_walkable_locations())


class TestMidMazeEnvironment(TestMazeEnvironment, unittest.TestCase):
    """ This class will test functions and attributes for the medium maze
    environment. """

    # Load up the medium maze
    with open('maze/maze_2', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300)

    def test_mid_get_maze_size(self):
        """ When we call get_maze_size() on a medium maze it should output
        as medium."""

        self.assertEqual("medium", self.world.get_maze_size())

    def test_mid_get_walkable_locations(self):
        """ Check get_walkable_locations() outputs the correct list of
        vertices for a mid maze."""
        self.assertEqual(
            [(1, 3), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
             (1, 10), (1, 11), (1, 15), (1, 16), (1, 17), (1, 18),
             (3, 1), (3, 2), (3, 7), (3, 8), (3, 9), (3, 10),
             (3, 11), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17),
             (3, 18), (5, 1), (5, 2), (5, 3), (5, 5), (5, 6),
             (5, 7), (5, 8), (5, 10), (5, 11), (5, 15), (5, 16),
             (5, 18), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5),
             (7, 6), (7, 7), (7, 8), (7, 10), (7, 11), (7, 12),
             (7, 13), (7, 14), (7, 15), (7, 16), (9, 1), (9, 2),
             (9, 3), (9, 5), (9, 6), (9, 7), (9, 8), (9, 10),
             (9, 11), (9, 12), (9, 13), (9, 14), (9, 16), (9, 17),
             (9, 18), (11, 1), (11, 2), (11, 3), (11, 5), (11, 6),
             (11, 7), (11, 8), (11, 10), (13, 1), (13, 2),
             (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8),
             (13, 10), (13, 11), (13, 12), (13, 13), (13, 14),
             (13, 15), (13, 16), (13, 17), (13, 18)],
            self.world.get_walkable_locations()
        )


class TestLargeMazeEnvironment(TestMazeEnvironment, unittest.TestCase):
    """ This class will test functions and attributes for the large maze
    environment. """

    # Load up the large maze
    with open('maze/maze_3', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300)

    def test_large_get_maze_size(self):
        """ When we call get_maze_size() on a large maze it should output
        as large."""

        self.assertEqual("large", self.world.get_maze_size())

    def test_large_get_walkable_locations(self):
        """ Check get_walkable_locations() outputs the correct list of
        vertices for a large maze."""
        self.assertEqual(
            [(1, 3), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11),
             (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 23),
             (1, 24), (1, 25), (1, 26), (3, 1), (3, 2), (3, 7), (3, 8), (3, 9),
             (3, 10), (3, 11), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17),
             (3, 18), (3, 19), (3, 20), (3, 21), (5, 1), (5, 2), (5, 3),
             (5, 5), (5, 6), (5, 7), (5, 8), (5, 10), (5, 11), (5, 15),
             (5, 16), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23),
             (5, 24), (5, 25), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
             (7, 7), (7, 8), (7, 10), (7, 11), (7, 12), (7, 13), (7, 14),
             (7, 15), (7, 16), (7, 19), (7, 20), (7, 21), (7, 22), (7, 23),
             (7, 24), (7, 25), (9, 1), (9, 2), (9, 3), (9, 5), (9, 6), (9, 7),
             (9, 8), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 16),
             (9, 17), (9, 18), (9, 19), (9, 20), (9, 21), (9, 22), (9, 25),
             (11, 1), (11, 2), (11, 3), (11, 5), (11, 6), (11, 7), (11, 8),
             (11, 10), (11, 19), (11, 20), (11, 21), (11, 22), (11, 23),
             (11, 24), (11, 25), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5),
             (13, 6), (13, 7), (13, 8), (13, 10), (13, 11), (13, 12), (13, 13),
             (13, 14), (13, 15), (13, 16), (13, 17), (13, 18), (13, 19),
             (13, 20), (13, 21), (13, 22), (13, 23), (13, 24), (13, 25),
             (13, 26)],
            self.world.get_walkable_locations()
        )


class TestEveryMazeEnvironmentSize(TestMazeEnvironment, unittest.TestCase):
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


class TestSmallFilledMazeEnvironment(TestMazeEnvironment, unittest.TestCase):
    """ This class will test a small maze where all diamonds are
    in a free space. """

    # Load up the small filled maze
    with open('maze/maze_5', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300, in_filled_maze=True)

    def test_filled_small_get_maze_size(self):
        """ When we call get_maze_size() on a small filled maze it should
        output the  'small' string."""

        self.assertEqual("small", self.world.get_maze_size())

    def test_filled_small_get_walkable_locations(self):
        """ Check get_walkable_locations() outputs the correct list of
        vertices for a small maze. The start pos should be the only walkable
        coord as there is no diamond initialized here."""
        self.assertEqual([(5, 6)], self.world.get_walkable_locations())

    def test_small_filled_maze_diamond_regeneration(self):
        """ This test will remove all the diamonds in the maze and then we
        will check if the regeneration function will fill all the cells with
        diamonds again.
        """

        self.world._diamond_group.empty()
        # When the diamonds are cleared, regenerate them in every cell
        self.world.fill_maze_with_diamonds()
        # No walkable grids now that the diamonds are in every grid
        self.assertEqual([], self.world.get_walkable_locations())


class TestMidFilledMazeEnvironment(TestMazeEnvironment, unittest.TestCase):
    """ This class will test a medium maze where all diamonds are
    in a free space. """

    # Load up the medium filled maze
    with open('maze/maze_6', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300, in_filled_maze=True)

    def test_filled_mid_get_maze_size(self):
        """ When we call get_maze_size() on a medium filled maze it should
        output the  'medium' string."""

        self.assertEqual("medium", self.world.get_maze_size())

    def test_filled_medium_get_walkable_locations(self):
        """ Check get_walkable_locations() outputs the correct list of
        vertices for a medium maze. The start pos should be the only walkable
        coord as there is no diamond initialized here."""
        self.assertEqual([(5, 6)], self.world.get_walkable_locations())

    def test_medium_filled_maze_diamond_regeneration(self):
        """ This test will remove all the diamonds in the maze and then we
        will check if the regeneration function will fill all the cells with
        diamonds again.
        """

        self.world._diamond_group.empty()
        # When the diamonds are cleared, regenerate them in every cell
        self.world.fill_maze_with_diamonds()
        # No walkable grids now that the diamonds are in every grid
        self.assertEqual([], self.world.get_walkable_locations())


class TestLargeFilledMazeEnvironment(TestMazeEnvironment, unittest.TestCase):
    """ This class will test a large maze where all diamonds are
    in a free space. """

    # Load up the large filled maze
    with open('maze/maze_7', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=300, player_pos_y=300, in_filled_maze=True)

    def test_filled_large_get_maze_size(self):
        """ When we call get_maze_size() on a large filled maze it should
        output the 'large' string."""

        self.assertEqual("large", self.world.get_maze_size())

    def test_filled_large_get_walkable_locations(self):
        """ Check get_walkable_locations() outputs the correct list of
        vertices for a large maze. The start pos should be the only walkable
        coord as there is no diamond initialized here."""
        self.assertEqual([(5, 6)], self.world.get_walkable_locations())

    def test_large_filled_maze_diamond_regeneration(self):
        """ This test will remove all the diamonds in the maze and then we
        will check if the regeneration function will fill all the cells with
        diamonds again.
        """

        self.world._diamond_group.empty()
        # When the diamonds are cleared, regenerate them in every cell
        self.world.fill_maze_with_diamonds()
        # No walkable grids now that the diamonds are in every grid
        self.assertEqual([], self.world.get_walkable_locations())


class TestSmallFilledMazeEnvironmentAStar(TestMazeEnvironment,
                                          unittest.TestCase):
    """ This class will test the min span tree function output for a small
    filled maze. """

    # Load up the large filled maze
    with open('maze/maze_5', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=350, player_pos_y=300, in_filled_maze=True)
        self.diamond = self.world.get_diamond_group().sprites()[0]
        self.computer = AStarFilledComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.diamond,
            diamond_list=self.world.get_diamond_group()
        )

    def test_min_span_tree_on_small_maze(self):
        self.assertEqual([
            ((5, 6), (5, 5)), ((5, 5), (5, 4)), ((5, 4), (5, 3)),
            ((5, 3), (5, 2)), ((5, 2), (5, 1)), ((5, 1), (5, 7)),
            ((5, 7), (5, 8)), ((5, 8), (5, 10)), ((5, 10), (5, 11)),
            ((5, 11), (5, 12)), ((5, 12), (5, 13)), ((5, 13), (5, 14)),
            ((5, 14), (3, 14)), ((3, 14), (3, 13)), ((3, 13), (3, 12)),
            ((3, 12), (3, 11)), ((3, 11), (3, 10)), ((3, 10), (3, 8)),
            ((3, 8), (3, 7)), ((3, 7), (3, 6)), ((3, 6), (3, 5)),
            ((3, 5), (3, 3)), ((3, 3), (3, 2)), ((3, 2), (3, 1)),
            ((3, 1), (1, 1)), ((1, 1), (1, 2)), ((1, 2), (1, 3)),
            ((1, 3), (1, 5)), ((1, 5), (1, 6)), ((1, 6), (1, 7)),
            ((1, 7), (1, 8)), ((1, 8), (1, 9)), ((1, 9), (1, 10)),
            ((1, 10), (1, 11)), ((1, 11), (1, 12)), ((1, 12), (1, 13)),
            ((1, 13), (1, 14))], self.computer.generate_mst()
        )


class TestMidFilledMazeEnvironmentAStar(TestMazeEnvironment,
                                        unittest.TestCase):
    """ This class will test the min span tree function output for a mid
    filled maze. """

    # Load up the large filled maze
    with open('maze/maze_6', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=350, player_pos_y=300, in_filled_maze=True)
        self.diamond = self.world.get_diamond_group().sprites()[0]
        self.computer = AStarFilledComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.diamond,
            diamond_list=self.world.get_diamond_group()
        )

    def test_min_span_tree_on_mid_maze(self):
        self.assertEqual([
            ((5, 6), (5, 5)), ((5, 5), (5, 3)), ((5, 3), (5, 2)),
            ((5, 2), (5, 1)), ((5, 1), (5, 7)), ((5, 7), (5, 8)),
            ((5, 8), (5, 10)), ((5, 10), (5, 11)), ((5, 11), (5, 13)),
            ((5, 13), (5, 14)), ((5, 14), (5, 15)), ((5, 15), (5, 16)),
            ((5, 16), (5, 18)), ((5, 18), (3, 18)), ((3, 18), (3, 17)),
            ((3, 17), (3, 16)), ((3, 16), (3, 15)), ((3, 15), (3, 14)),
            ((3, 14), (3, 13)), ((3, 13), (3, 11)), ((3, 11), (3, 10)),
            ((3, 10), (3, 9)), ((3, 9), (3, 8)), ((3, 8), (3, 7)),
            ((3, 7), (3, 6)), ((3, 6), (3, 5)), ((3, 5), (3, 3)),
            ((3, 3), (3, 2)), ((3, 2), (3, 1)), ((3, 1), (1, 1)),
            ((1, 1), (1, 2)), ((1, 2), (1, 3)), ((1, 3), (1, 5)),
            ((1, 5), (1, 6)), ((1, 6), (1, 7)), ((1, 7), (1, 8)),
            ((1, 8), (1, 9)), ((1, 9), (1, 10)), ((1, 10), (1, 11)),
            ((1, 11), (1, 12)), ((1, 12), (1, 13)), ((1, 13), (1, 14)),
            ((1, 14), (1, 15)), ((1, 15), (1, 16)), ((1, 16), (1, 17)),
            ((1, 17), (1, 18)), ((1, 18), (7, 18)), ((7, 18), (7, 16)),
            ((7, 16), (7, 15)), ((7, 15), (7, 14)), ((7, 14), (7, 13)),
            ((7, 13), (7, 12)), ((7, 12), (7, 11)), ((7, 11), (7, 10)),
            ((7, 10), (7, 8)), ((7, 8), (7, 7)), ((7, 7), (7, 6)),
            ((7, 6), (7, 5)), ((7, 5), (7, 4)), ((7, 4), (7, 3)),
            ((7, 3), (7, 2)), ((7, 2), (7, 1)), ((7, 1), (9, 1)),
            ((9, 1), (9, 2)), ((9, 2), (9, 3)), ((9, 3), (9, 5)),
            ((9, 5), (9, 6)), ((9, 6), (9, 7)), ((9, 7), (9, 8)),
            ((9, 8), (9, 10)), ((9, 10), (9, 11)), ((9, 11), (9, 12)),
            ((9, 12), (9, 13)), ((9, 13), (9, 14)), ((9, 14), (9, 16)),
            ((9, 16), (9, 17)), ((9, 17), (9, 18)), ((9, 18), (11, 18)),
            ((11, 18), (11, 17)), ((11, 17), (11, 16)), ((11, 16), (11, 14)),
            ((11, 14), (11, 13)), ((11, 13), (11, 12)), ((11, 12), (11, 11)),
            ((11, 11), (11, 10)), ((11, 10), (11, 8)), ((11, 8), (11, 7)),
            ((11, 7), (11, 6)), ((11, 6), (11, 5)), ((11, 5), (11, 3)),
            ((11, 3), (11, 2)), ((11, 2), (11, 1)), ((11, 1), (13, 1)),
            ((13, 1), (13, 2)), ((13, 2), (13, 3)), ((13, 3), (13, 4)),
            ((13, 4), (13, 5)), ((13, 5), (13, 6)), ((13, 6), (13, 7)),
            ((13, 7), (13, 8)), ((13, 8), (13, 10)), ((13, 10), (13, 11)),
            ((13, 11), (13, 12)), ((13, 12), (13, 13)), ((13, 13), (13, 14)),
            ((13, 14), (13, 15)), ((13, 15), (13, 16)), ((13, 16), (13, 17)),
            ((13, 17), (13, 18))], self.computer.generate_mst()
        )


class TestLargeFilledMazeEnvironmentAStar(TestMazeEnvironment,
                                          unittest.TestCase):
    """ This class will test the min span tree function output for a large
    filled maze. """

    # Load up the large filled maze
    with open('maze/maze_7', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(player_pos_x=350, player_pos_y=300, in_filled_maze=True)
        self.diamond = self.world.get_diamond_group().sprites()[0]
        self.computer = AStarFilledComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.diamond,
            diamond_list=self.world.get_diamond_group()
        )

    def test_min_span_tree_on_large_maze(self):
        self.assertEqual([
            ((5, 6), (5, 5)), ((5, 5), (5, 3)), ((5, 3), (5, 2)),
            ((5, 2), (5, 1)), ((5, 1), (5, 7)), ((5, 7), (5, 8)),
            ((5, 8), (5, 10)), ((5, 10), (5, 11)), ((5, 11), (5, 13)),
            ((5, 13), (5, 14)), ((5, 14), (5, 15)), ((5, 15), (5, 16)),
            ((5, 16), (5, 18)), ((5, 18), (5, 19)), ((5, 19), (5, 20)),
            ((5, 20), (5, 21)), ((5, 21), (5, 22)), ((5, 22), (5, 23)),
            ((5, 23), (5, 24)), ((5, 24), (5, 25)), ((5, 25), (3, 25)),
            ((3, 25), (3, 24)), ((3, 24), (3, 23)), ((3, 23), (3, 22)),
            ((3, 22), (3, 21)), ((3, 21), (3, 20)), ((3, 20), (3, 19)),
            ((3, 19), (3, 18)), ((3, 18), (3, 17)), ((3, 17), (3, 16)),
            ((3, 16), (3, 15)), ((3, 15), (3, 14)), ((3, 14), (3, 13)),
            ((3, 13), (3, 11)), ((3, 11), (3, 10)), ((3, 10), (3, 9)),
            ((3, 9), (3, 8)), ((3, 8), (3, 7)), ((3, 7), (3, 6)),
            ((3, 6), (3, 5)), ((3, 5), (3, 3)), ((3, 3), (3, 2)),
            ((3, 2), (3, 1)), ((3, 1), (1, 1)), ((1, 1), (1, 2)),
            ((1, 2), (1, 3)), ((1, 3), (1, 5)), ((1, 5), (1, 6)),
            ((1, 6), (1, 7)), ((1, 7), (1, 8)), ((1, 8), (1, 9)),
            ((1, 9), (1, 10)), ((1, 10), (1, 11)), ((1, 11), (1, 12)),
            ((1, 12), (1, 13)), ((1, 13), (1, 14)), ((1, 14), (1, 15)),
            ((1, 15), (1, 16)), ((1, 16), (1, 17)), ((1, 17), (1, 18)),
            ((1, 18), (1, 19)), ((1, 19), (1, 20)), ((1, 20), (1, 21)),
            ((1, 21), (1, 22)), ((1, 22), (1, 23)), ((1, 23), (1, 24)),
            ((1, 24), (1, 25)), ((1, 25), (1, 26)), ((1, 26), (7, 25)),
            ((7, 25), (7, 24)), ((7, 24), (7, 23)), ((7, 23), (7, 22)),
            ((7, 22), (7, 21)), ((7, 21), (7, 20)), ((7, 20), (7, 19)),
            ((7, 19), (7, 18)), ((7, 18), (7, 16)), ((7, 16), (7, 15)),
            ((7, 15), (7, 14)), ((7, 14), (7, 13)), ((7, 13), (7, 12)),
            ((7, 12), (7, 11)), ((7, 11), (7, 10)), ((7, 10), (7, 8)),
            ((7, 8), (7, 7)), ((7, 7), (7, 6)), ((7, 6), (7, 5)),
            ((7, 5), (7, 4)), ((7, 4), (7, 3)), ((7, 3), (7, 2)),
            ((7, 2), (7, 1)), ((7, 1), (9, 1)), ((9, 1), (9, 2)),
            ((9, 2), (9, 3)), ((9, 3), (9, 5)), ((9, 5), (9, 6)),
            ((9, 6), (9, 7)), ((9, 7), (9, 8)), ((9, 8), (9, 10)),
            ((9, 10), (9, 11)), ((9, 11), (9, 12)), ((9, 12), (9, 13)),
            ((9, 13), (9, 14)), ((9, 14), (9, 16)), ((9, 16), (9, 17)),
            ((9, 17), (9, 18)), ((9, 18), (9, 19)), ((9, 19), (9, 20)),
            ((9, 20), (9, 21)), ((9, 21), (9, 22)), ((9, 22), (9, 23)),
            ((9, 23), (9, 24)), ((9, 24), (9, 25)), ((9, 25), (11, 25)),
            ((11, 25), (11, 24)), ((11, 24), (11, 23)), ((11, 23), (11, 22)),
            ((11, 22), (11, 21)), ((11, 21), (11, 20)), ((11, 20), (11, 19)),
            ((11, 19), (11, 18)), ((11, 18), (11, 17)), ((11, 17), (11, 16)),
            ((11, 16), (11, 14)), ((11, 14), (11, 13)), ((11, 13), (11, 12)),
            ((11, 12), (11, 11)), ((11, 11), (11, 10)), ((11, 10), (11, 8)),
            ((11, 8), (11, 7)), ((11, 7), (11, 6)), ((11, 6), (11, 5)),
            ((11, 5), (11, 3)), ((11, 3), (11, 2)), ((11, 2), (11, 1)),
            ((11, 1), (13, 1)), ((13, 1), (13, 2)), ((13, 2), (13, 3)),
            ((13, 3), (13, 4)), ((13, 4), (13, 5)), ((13, 5), (13, 6)),
            ((13, 6), (13, 7)), ((13, 7), (13, 8)), ((13, 8), (13, 10)),
            ((13, 10), (13, 11)), ((13, 11), (13, 12)), ((13, 12), (13, 13)),
            ((13, 13), (13, 14)), ((13, 14), (13, 15)), ((13, 15), (13, 16)),
            ((13, 16), (13, 17)), ((13, 17), (13, 18)), ((13, 18), (13, 19)),
            ((13, 19), (13, 20)), ((13, 20), (13, 21)), ((13, 21), (13, 22)),
            ((13, 22), (13, 23)), ((13, 23), (13, 24)), ((13, 24), (13, 25)),
            ((13, 25), (13, 26))], self.computer.generate_mst()
        )


if __name__ == '__main__':
    unittest.main()
