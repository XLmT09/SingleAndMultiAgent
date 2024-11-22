import sys, os, pygame, unittest, pickle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from computer import *
from characters import CharacterAnimationManager
from world import World

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
        pygame.display.set_mode((1,1), 0, 32)
        self.player = CharacterAnimationManager(CHARACTER_WIDTH, CHARACTER_HEIGHT, self.maze_map, True, 500, 700)
        self.player.set_char_animation("idle", "product/assets/images/characters/Dude_Monster/Dude_Monster_Idle_4.png", 4)  
        self.player.set_char_animation("jump", "product/assets/images/characters/Dude_Monster/Dude_Monster_Jump_8.png", 8)
        self.player.set_char_animation("walk", "product/assets/images/characters/Dude_Monster/Dude_Monster_Walk_6.png", 6)
        self.player.set_char_animation("climb", "product/assets/images/characters/Dude_Monster/Dude_Monster_Climb_4.png", 4)

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