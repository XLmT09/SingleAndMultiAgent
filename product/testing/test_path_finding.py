from product.computer import DFSComputer, BFSComputer, UCSComputer
from product.characters import CharacterAnimationManager
from product.world import World
from product.constants import player_sprite_file_paths

import unittest
import pygame
import pickle

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
# Test cases will generate the maze map
maze_map = None


class TestComputer(unittest.TestCase):
    def setUp(self, pos_x, pos_y):
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
    with open('maze_1', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(500, 700)

    def test_bfs_can_find_path_in_small_maze(self):
        computer = BFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path,
                         [(13, 9), (12, 9), (12, 10), (12, 11),
                          (12, 12), (12, 13), (12, 14)])
        computer.stop_thread = True

    def test_dfs_can_find_path_in_small_maze(self):
        computer = DFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(13, 9), (12, 9), (12, 10), (12, 11),
                          (12, 12), (12, 13), (12, 14)])
        computer.stop_thread = True

    def test_ucs_can_find_path_in_small_maze(self):
        computer = UCSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(13, 9), (12, 9), (12, 10), (12, 11),
                          (12, 12), (12, 13), (12, 14)])
        computer.stop_thread = True


class TestComputerMidMaze(TestComputer, unittest.TestCase):
    """ Test path finding algorithms can work on a mid size maze. """
    with open('maze_2', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(500, 700)

    def test_bfs_can_find_path_in_mid_maze(self):
        computer = BFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path,
                         [(13, 9), (12, 9), (12, 8), (12, 7), (12, 6), (12, 5),
                          (12, 4), (11, 4), (10, 4), (10, 5), (10, 6), (10, 7),
                          (10, 8), (10, 9), (9, 9), (8, 9), (8, 10), (8, 11),
                          (8, 12), (8, 13), (8, 14), (8, 15), (8, 16),
                          (8, 17), (8, 18)])
        computer.stop_thread = True

    def test_dfs_can_find_path_in_mid_maze(self):
        computer = DFSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(13, 9), (12, 9), (12, 8), (12, 7), (12, 6), (12, 5),
                          (12, 4), (11, 4), (10, 4), (10, 5), (10, 6), (10, 7),
                          (10, 8), (10, 9), (9, 9), (8, 9), (7, 9), (6, 9),
                          (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (5, 4),
                          (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                          (4, 10), (4, 11), (4, 12), (5, 12), (6, 12), (6, 13),
                          (6, 14), (6, 15), (6, 16), (6, 17), (7, 17),
                          (8, 17), (8, 18)])
        computer.stop_thread = True

    def test_ucs_can_find_path_in_mid_maze(self):
        computer = UCSComputer(self.player,
                               self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path,
                         [(13, 9), (12, 9), (12, 8), (12, 7), (12, 6), (12, 5),
                          (12, 4), (11, 4), (10, 4), (10, 5), (10, 6), (10, 7),
                          (10, 8), (10, 9), (9, 9), (8, 9), (8, 10), (8, 11),
                          (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17),
                          (8, 18)])
        computer.stop_thread = True


class TestComputerLargeMaze(TestComputer, unittest.TestCase):
    """ Test path finding algorithms can work on a large maze. """
    with open('maze_3', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(480, 600)

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
    with open('maze_4', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(480, 600)

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
    with open('maze_3', 'rb') as file:
        maze_map = pickle.load(file)

    def setUp(self):
        super().setUp(950, 400)


if __name__ == '__main__':
    unittest.main()
