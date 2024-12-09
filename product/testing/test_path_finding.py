from computer import DFSComputer, BFSComputer, UCSComputer
from characters import CharacterAnimationManager
from world import World
from constants import player_sprite_file_paths

import unittest
import pygame
import pickle

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
# Test cases will generate the maze map
maze_map = None


class TestComputer(unittest.TestCase):
    """ Setup class which the other tests classes in this
    file will inherit from. """
    def setUp(self, pos_x, pos_y):
        """
        Args:
            pos_x (int): x position of the agent.
            pos_y (int): y position of the agent.
        """
        pygame.init()
        pygame.display.set_mode((1, 1), 0, 32)
        self.player = CharacterAnimationManager(CHARACTER_WIDTH,
                                                CHARACTER_HEIGHT,
                                                self.maze_map, True,
                                                pos_x, pos_y)
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


class TestComputerSmallMaze(TestComputer, unittest.TestCase):
    """ Test path finding algorithms can work on a small maze. """

    with open('maze/maze_1', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(pos_x=300, pos_y=300)

    def test_bfs_can_find_path_in_small_maze(self):
        computer = BFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path,
                         [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (4, 9),
                          (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14)])
        computer.stop_thread = True

    def test_dfs_can_find_path_in_small_maze(self):
        computer = DFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (4, 9),
                          (3, 9), (3, 8), (3, 7), (3, 6), (3, 5), (3, 4),
                          (2, 4), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
                          (1, 9), (1, 10), (1, 11), (1, 12), (1, 13),
                          (1, 14), (1, 15), (2, 15), (3, 15), (3, 14)])
        computer.stop_thread = True

    def test_ucs_can_find_path_in_small_maze(self):
        computer = UCSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (4, 9),
                          (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14)])
        computer.stop_thread = True


class TestComputerMidMaze(TestComputer, unittest.TestCase):
    """ Test path finding algorithms can work on a mid size maze. """

    with open('maze/maze_2', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)

    def test_bfs_can_find_path_in_mid_maze(self):
        computer = BFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path,
                         [(5, 6), (5, 7), (5, 8), (5, 9), (6, 9), (7, 9),
                          (7, 10), (7, 11), (7, 12), (7, 13), (7, 14),
                          (7, 15), (7, 16), (7, 17), (7, 18)])
        computer.stop_thread = True

    def test_dfs_can_find_path_in_mid_maze(self):
        computer = DFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(5, 6), (5, 5), (5, 4), (4, 4), (3, 4), (3, 5),
                          (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11),
                          (3, 12), (4, 12), (5, 12), (5, 11), (5, 10), (5, 9),
                          (6, 9), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13),
                          (7, 14), (7, 15), (7, 16), (7, 17), (7, 18)])
        computer.stop_thread = True

    def test_ucs_can_find_path_in_mid_maze(self):
        computer = UCSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(5, 6), (5, 7), (5, 8), (5, 9), (6, 9), (7, 9),
                          (7, 10), (7, 11), (7, 12), (7, 13), (7, 14), (7, 15),
                          (7, 16), (7, 17), (7, 18)])
        computer.stop_thread = True


class TestComputerLargeMaze(TestComputer, unittest.TestCase):
    """ Test path finding algorithms can work on a large maze. """

    with open('maze/maze_3', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(pos_x=480, pos_y=600)

    def test_bfs_can_find_path_in_large_maze(self):
        computer = BFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path,
                         [(11, 9), (11, 8), (11, 7), (11, 6), (11, 5), (11, 4),
                          (10, 4), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8),
                          (9, 9), (8, 9), (7, 9), (7, 10), (7, 11), (7, 12),
                          (7, 13), (7, 14), (7, 15), (7, 16), (7, 17),
                          (7, 18)])
        computer.stop_thread = True

    def test_dfs_can_find_path_in_large_maze(self):
        computer = DFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(11, 9), (11, 8), (11, 7), (11, 6), (11, 5), (11, 4),
                          (10, 4), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8),
                          (9, 9), (8, 9), (7, 9), (6, 9), (5, 9), (5, 8),
                          (5, 7), (5, 6), (5, 5), (5, 4), (4, 4), (3, 4),
                          (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
                          (3, 11), (3, 12), (4, 12), (5, 12), (5, 13),
                          (5, 14), (5, 15), (5, 16), (5, 17), (6, 17),
                          (7, 17), (7, 18)])
        computer.stop_thread = True

    def test_ucs_can_find_path_in_large_maze(self):
        computer = UCSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(11, 9), (11, 8), (11, 7), (11, 6), (11, 5), (11, 4),
                          (10, 4), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8),
                          (9, 9), (8, 9), (7, 9), (7, 10), (7, 11), (7, 12),
                          (7, 13), (7, 14), (7, 15), (7, 16), (7, 17),
                          (7, 18)])
        computer.stop_thread = True


class TestExtraUCSPathFinding(TestComputer, unittest.TestCase):
    """ Test to see if the UCS algorithm will actually choose the most
    optimal path and not the shortest one. """

    with open('maze/maze_4', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(pos_x=480, pos_y=600)

    def test_ucs_chooses_low_cost_path_over_a_high_cost_one(self):
        """ The map given has two routes the player can take, one path is
        shorter but with slow tiles and the other path is longer but with
        normal tiles. The UCS algo is expected to take the later path.
        """
        computer = UCSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(
            path,
            [(11, 9), (11, 10), (11, 11), (11, 12), (11, 13), (11, 14),
             (11, 15), (11, 16), (11, 17), (11, 18)])
        computer.stop_thread = True


class TestComputerStartIsGoalState(TestComputer, unittest.TestCase):
    """ This class has tests to see that a path is still generated for
    different algos when the start stae equals the end state."""

    with open('maze/maze_3', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        # Position of the player is in the same grid as the diamond
        super().setUp(pos_x=950, pos_y=400)

    def test_bfs_algo_when_start_is_goal(self):
        computer = BFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path, [(7, 18)])
        computer.stop_thread = True

    def test_dfs_algo_when_start_is_goal(self):
        computer = DFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path, [(7, 18)])
        computer.stop_thread = True

    def test_ucs_algo_when_start_is_goal(self):
        computer = UCSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path, [(7, 18)])
        computer.stop_thread = True


class TestVisitedGrids(TestComputer, unittest.TestCase):
    """ This class will test the get visited grids fucntion with the context
    of a large maze on multiple algorithms."""

    with open('maze/maze_3', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        # Position of the player is in the same grid as the diamond
        super().setUp(pos_x=350, pos_y=300)

    def test_get_visited_grids_on_dfs(self):
        """ This function will test the list of visted grids generated matches
        the data set we expect for dfs in a large maze.
        """
        computer = DFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.start_thread()
        visited_grids_generated = (
            computer.get_visited_grids_and_path_to_goal()[0]
        )
        computer.stop_thread = True
        self.assertEqual(visited_grids_generated,
                         [(5, 6), (5, 5), (5, 4), (4, 4), (3, 4), (2, 4),
                          (1, 4), (1, 3), (1, 2), (1, 1), (1, 5), (1, 6),
                          (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12),
                          (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18),
                          (1, 19), (1, 20), (1, 21), (1, 22), (1, 23), (1, 24),
                          (1, 25), (1, 26), (3, 3), (3, 2), (3, 1), (3, 5),
                          (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11),
                          (3, 12), (4, 12), (5, 12), (5, 11), (5, 10), (5, 9),
                          (5, 8), (5, 7), (6, 9), (7, 9), (7, 8), (7, 7),
                          (7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1),
                          (8, 9), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5),
                          (9, 4), (9, 3), (9, 2), (9, 1), (10, 4), (11, 4),
                          (11, 3), (11, 2), (11, 1), (11, 5), (11, 6), (11, 7),
                          (11, 8), (11, 9), (12, 9), (13, 9), (13, 8), (13, 7),
                          (13, 6), (13, 5), (13, 4), (13, 3), (13, 2), (13, 1),
                          (13, 10), (13, 11), (13, 12), (13, 13), (13, 14),
                          (13, 15), (13, 16), (13, 17), (13, 18), (13, 19),
                          (13, 20), (13, 21), (13, 22), (13, 23), (13, 24),
                          (13, 25), (13, 26), (11, 10), (11, 11), (11, 12),
                          (11, 13), (11, 14), (11, 15), (10, 15), (9, 15),
                          (9, 14), (9, 13), (9, 12), (9, 11), (9, 10), (9, 16),
                          (9, 17), (9, 18), (9, 19), (9, 20), (9, 21), (9, 22),
                          (9, 23), (9, 24), (9, 25), (9, 26), (8, 26), (7, 26),
                          (6, 26), (5, 26), (4, 26), (3, 26), (3, 25), (3, 24),
                          (3, 23), (3, 22), (3, 21), (3, 20), (3, 19), (3, 18),
                          (3, 17), (3, 16), (3, 15), (3, 14), (3, 13), (5, 25),
                          (5, 24), (5, 23), (5, 22), (5, 21), (5, 20), (5, 19),
                          (5, 18), (5, 17), (5, 16), (5, 15), (5, 14), (5, 13),
                          (6, 17), (7, 17), (7, 16), (7, 15), (7, 14), (7, 13),
                          (7, 12), (7, 11), (7, 10), (7, 18)])
        computer.stop_thread = True

    def test_get_visited_grids_on_bfs(self):
        """ This function will test the list of visted grids generated matches
        the data set we expect for bfs in a large maze.
        """
        computer = BFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.start_thread()
        visited_grids_generated = (
            computer.get_visited_grids_and_path_to_goal()[0]
        )
        computer.stop_thread = True
        self.assertEqual(visited_grids_generated,
                         [(5, 6), (5, 7), (5, 5), (5, 8), (5, 4),
                          (5, 9), (5, 3), (4, 4), (5, 10), (6, 9),
                          (5, 2), (3, 4), (5, 11), (7, 9), (5, 1),
                          (3, 5), (3, 3), (2, 4), (5, 12), (7, 10),
                          (8, 9), (7, 8), (3, 6), (3, 2), (1, 4),
                          (5, 13), (4, 12), (7, 11), (9, 9), (7, 7),
                          (3, 7), (3, 1), (1, 5), (1, 3), (5, 14),
                          (3, 12), (7, 12), (9, 10), (9, 8), (7, 6),
                          (3, 8), (1, 6), (1, 2), (5, 15), (3, 13),
                          (3, 11), (7, 13), (9, 11), (9, 7), (7, 5),
                          (3, 9), (1, 7), (1, 1), (5, 16), (3, 14),
                          (3, 10), (7, 14), (9, 12), (9, 6), (7, 4),
                          (3, 10), (1, 8), (5, 17), (3, 15), (7, 15),
                          (9, 13), (9, 5), (7, 3), (1, 9), (5, 18),
                          (6, 17), (3, 16), (7, 16), (9, 14), (9, 4),
                          (7, 2), (1, 10), (5, 19), (7, 17), (3, 17),
                          (7, 17), (9, 15), (10, 4), (9, 3), (7, 1),
                          (1, 11), (5, 20), (7, 18)])
        computer.stop_thread = True

    def test_get_visited_grids_on_ucs(self):
        """ This function will test the list of visted grids generated matches
        the data set we expect for ucs in a large maze.
        """
        computer = UCSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.start_thread()
        visited_grids_generated = (
            computer.get_visited_grids_and_path_to_goal()[0]
        )
        computer.stop_thread = True
        self.assertEqual(visited_grids_generated,
                         [(5, 6), (5, 5), (5, 7), (5, 4), (5, 8), (4, 4),
                          (5, 3), (5, 9), (3, 4), (5, 2), (5, 10), (6, 9),
                          (2, 4), (5, 1), (5, 11), (7, 9), (1, 4), (5, 12),
                          (7, 8), (7, 10), (8, 9), (1, 3), (1, 5), (3, 3),
                          (3, 5), (4, 12), (7, 7), (7, 11), (9, 9), (1, 6),
                          (3, 2), (3, 12), (7, 6), (7, 12), (9, 8), (9, 10),
                          (1, 7), (3, 1), (3, 11), (3, 13), (5, 13), (7, 5),
                          (7, 13), (9, 7), (9, 11), (1, 2), (1, 8), (3, 6),
                          (3, 10), (3, 14), (7, 4), (7, 14), (9, 6), (9, 12),
                          (1, 9), (3, 7), (3, 9), (3, 15), (7, 3), (7, 15),
                          (9, 5), (9, 13), (1, 10), (3, 8), (3, 16), (5, 14),
                          (7, 2), (7, 16), (9, 4), (9, 14), (1, 1), (1, 11),
                          (3, 17), (5, 15), (7, 1), (7, 17), (7, 18)])
        computer.stop_thread = True


if __name__ == '__main__':
    unittest.main()
