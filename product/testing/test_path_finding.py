import unittest
import sys, os
import pygame 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from computer import BFSComputer 
from characters import CharacterAnimationManager
from world import World

class TestComputer(unittest.TestCase):
    CHARACTER_WIDTH = 32 
    CHARACTER_HEIGHT = 32
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 800
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
        self.player = CharacterAnimationManager(self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT, self.maze_map, True, 500, 700)
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
        path = computer.bfs_path_find()
        computer.stop_thread = True
        self.assertEqual(path, 
                        [(14, 10), (14, 9), (13, 9), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14)])        
        computer.stop_thread = True


if __name__ == '__main__':
    unittest.main()


