import unittest
import sys, os
import pygame 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from computer import *
from characters import CharacterAnimationManager
from world import World

CHARACTER_WIDTH = 32 
CHARACTER_HEIGHT = 32
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
class TestComputer(unittest.TestCase):
    maze_map = [
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0 , 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1 , 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0 , 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0 , 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1,1), 0, 32)
        self.player = CharacterAnimationManager(CHARACTER_WIDTH, CHARACTER_HEIGHT, self.maze_map, True, 500, 700)
        self.player.set_char_animation("idle", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png", 4)  
        self.player.set_char_animation("jump", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Jump_8.png", 8)
        self.player.set_char_animation("walk", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Walk_6.png", 6)
        self.player.set_char_animation("climb", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Climb_4.png", 4)

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
                

    def test_bfs_can_find_path_in_small_maze(self):
        computer = BFSComputer(self.player, self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path, 
                        [(13, 9), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14)])        
        computer.stop_thread = True
    
    def test_dfs_can_find_path_in_small_maze(self):
        computer = DFSComputer(self.player, self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path, 
                        [(13, 9), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14)])        
        computer.stop_thread = True
    
    def test_ucs_can_find_path_in_small_maze(self):
        computer = UCSComputer(self.player, self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path, 
                        [(13, 9), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14)])        
        computer.stop_thread = True

class TestComputerMidMaze(unittest.TestCase):
    maze_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 4, 1, 3, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 4, 3, 4, 4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 4, 4, 4, 1, 1, 3, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 4, 4, 4, 4, 4, 4, 4, 4, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1,1), 0, 32)
        self.player = CharacterAnimationManager(CHARACTER_WIDTH, CHARACTER_HEIGHT, self.maze_map, True, 500, 700)
        self.player.set_char_animation("idle", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png", 4)  
        self.player.set_char_animation("jump", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Jump_8.png", 8)
        self.player.set_char_animation("walk", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Walk_6.png", 6)
        self.player.set_char_animation("climb", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Climb_4.png", 4)

        self.world = World(self.maze_map)
    
    def tearDown(self):
        pygame.quit()

    def test_bfs_can_find_path_in_mid_maze(self):
        computer = BFSComputer(self.player, self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path, 
                        [(13, 9), (12, 9), (12, 8), (12, 7), (12, 6), (12, 5), (12, 4), 
                         (11, 4), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), 
                         (9, 9), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), 
                         (8, 15), (8, 16), (8, 17), (8, 18)])        
        computer.stop_thread = True
    
    def test_dfs_can_find_path_in_mid_maze(self):
        computer = DFSComputer(self.player, self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path, 
                        [(13, 9), (12, 9), (12, 8), (12, 7), (12, 6), (12, 5), 
                         (12, 4), (11, 4), (10, 4), (10, 5), (10, 6), (10, 7), 
                         (10, 8), (10, 9), (9, 9), (8, 9), (7, 9), (6, 9), (6, 8), 
                         (6, 7), (6, 6), (6, 5), (6, 4), (5, 4), (4, 4), (4, 5), 
                         (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), 
                         (5, 12), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), 
                         (6, 17), (7, 17), (8, 17), (8, 18)])        
        computer.stop_thread = True
    
    def test_ucs_can_find_path_in_mid_maze(self):
        computer = UCSComputer(self.player, self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path, 
                        [(13, 9), (12, 9), (12, 8), (12, 7), (12, 6), (12, 5), (12, 4), 
                         (11, 4), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), 
                         (9, 9), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), 
                         (8, 14), (8, 15), (8, 16), (8, 17), (8, 18)])        
        computer.stop_thread = True

class TestComputerLargeMaze(unittest.TestCase):
    maze_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 4, 1, 3, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 4, 3, 4, 4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 3, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 4, 4, 4, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 3, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1,1), 0, 32)
        # The player will start at a different postion in this test dure to its size
        self.player = CharacterAnimationManager(CHARACTER_WIDTH, CHARACTER_HEIGHT, self.maze_map, True, 480, 600)
        self.player.set_char_animation("idle", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png", 4)  
        self.player.set_char_animation("jump", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Jump_8.png", 8)
        self.player.set_char_animation("walk", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Walk_6.png", 6)
        self.player.set_char_animation("climb", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Climb_4.png", 4)

        self.world = World(self.maze_map)
    
    def tearDown(self):
        pygame.quit()

    def test_bfs_can_find_path_in_large_maze(self):
        computer = BFSComputer(self.player, self.world.get_walkable_maze_matrix())
        path = computer.generate_path()
        computer.stop_thread = True
        self.assertEqual(path, 
                        [(11, 9), (11, 8), (11, 7), (11, 6), (11, 5), (11, 4), (10, 4),
                         (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (8, 9), (7, 9),
                         (7, 10), (7, 11), (7, 12), (7, 13), (7, 14), (7, 15), (7, 16),
                         (7, 17), (7, 18)])        
        computer.stop_thread = True
    
    def test_dfs_can_find_path_in_large_maze(self):
        computer = DFSComputer(self.player, self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path, 
                        [(11, 9), (11, 8), (11, 7), (11, 6), (11, 5), (11, 4), 
                         (10, 4), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), 
                         (8, 9), (7, 9), (6, 9), (5, 9), (5, 8), (5, 7), (5, 6), 
                         (5, 5), (5, 4), (4, 4), (3, 4), (3, 5), (3, 6), (3, 7), 
                         (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (4, 12), (5, 12), 
                         (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (6, 17), 
                         (7, 17), (7, 18)])        
        computer.stop_thread = True
    
    def test_ucs_can_find_path_in_large_maze(self):
        computer = UCSComputer(self.player, self.world.get_walkable_maze_matrix())
        computer.stop_thread = True
        path = computer.generate_path()
        self.assertEqual(path, 
                        [(11, 9), (11, 8), (11, 7), (11, 6), (11, 5), (11, 4), 
                         (10, 4), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), 
                         (8, 9), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13), (7, 14), 
                         (7, 15), (7, 16), (7, 17), (7, 18)])        
        computer.stop_thread = True

if __name__ == '__main__':
    unittest.main()


