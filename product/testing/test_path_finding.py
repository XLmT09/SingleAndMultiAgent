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
    """ Setup class which the other tests classes in this file will inherit
    from. """
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
                         [(5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11),
                          (5, 12), (5, 13), (5, 14), (5, 15), (5, 16),
                          (5, 17), (6, 17), (7, 17), (7, 18)])
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
        self.assertEqual(path,
                         [(11, 9), (11, 8), (11, 7), (11, 6), (11, 5),
                          (11, 4), (10, 4), (9, 4), (9, 5), (9, 6), (9, 7),
                          (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13),
                          (9, 14), (9, 15), (10, 15), (11, 15), (11, 16),
                          (11, 17), (11, 18)])
        computer.stop_thread = True


class TestComputerStartIsGoalState(TestComputer, unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
