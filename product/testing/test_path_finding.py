import unittest
import sys, os
import pygame 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from computer import Computer 
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
    [1, 1, 0, 0 , 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1 , 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0 , 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1],
    [1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    def setUp(self):
        pygame.init()
        pygame.display.set_mode()
        self.player = CharacterAnimationManager(self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT, self.maze_map, True, 500, 700)
        self.player.set_char_animation("idle", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Idle_4.png", 4)  
        self.player.set_char_animation("jump", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Jump_8.png", 8)
        self.player.set_char_animation("walk", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Walk_6.png", 6)
        self.player.set_char_animation("climb", r"product\assets\images\characters\Dude_Monster\Dude_Monster_Climb_4.png", 4)

        self.world = World(self.maze_map)

    def test_bfs_can_find_path_in_small_maze(self):
        computer = Computer(self.player, self.world.get_walkable_maze_matrix())
        computer.bfs_path_find()
        self.assertEqual(computer.bfs_path_find(),
                        [(14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15)])

if __name__ == '__main__':
    unittest.main()


