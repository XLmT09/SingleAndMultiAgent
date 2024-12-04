from computer import BFSComputer
from characters import CharacterAnimationManager
from world import World
from constants import player_sprite_file_paths, game_values

import unittest
import pygame
import pickle

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32

# Maze map the functions will use
maze_map = None
with open('maze/maze_1', 'rb') as file:
    maze_map = pickle.load(file)
clock = pygame.time.Clock()


class TestGUIComputer(unittest.TestCase):
    """ Setup class which the other tests classes in this
    file will inherit from.

    Format is similar to main.py, anything not commented here would must
    likely be commented over there.
    """
    def setUp(self):
        """
        Args:
            pos_x (int): x position of the agent.
            pos_y (int): y position of the agent.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((850, 350))
        self.player = CharacterAnimationManager(CHARACTER_WIDTH,
                                                CHARACTER_HEIGHT,
                                                maze_map, True,
                                                350, 300)
        self.player.set_char_animation("idle",
                                       player_sprite_file_paths["idle"], 4)
        self.player.set_char_animation("jump",
                                       player_sprite_file_paths["jump"], 8)
        self.player.set_char_animation("walk",
                                       player_sprite_file_paths["walk"], 6)
        self.player.set_char_animation("climb",
                                       player_sprite_file_paths["climb"], 4)

        self.world = World(maze_map)
        self.computer = BFSComputer(self.player,
                                    self.world.get_walkable_maze_matrix(),
                                    True)

        # Start the path finding algorithm
        self.computer.start_thread()

        self.game_over = 0
        self.tile_data = self.world.get_collidable_tile_list()
        self.diamond_positons = self.world.get_diamond_group()

    def tearDown(self):
        pygame.quit()

    def testGUICollision(self):
        """ This function will test if collision detection between the diamond
        and agent."""
        collision_detected = False

        # We will run a game loop until collision is detected
        while not collision_detected:
            # We have found the diamond and can begin to stop the test
            if self.player.get_is_diamond_found():
                self.computer.stop_thread = True
                collision_detected = True

            # Blitting the tiles
            self.world.load_world(self.screen)

            # Moving the player
            self.game_over = self.computer.move(self.screen,
                                                self.tile_data,
                                                self.diamond_positons,
                                                self.game_over)

            # Can end the test once collision is detected
            if collision_detected:
                self.assertTrue(collision_detected, "Test passed as collison "
                                "was detected.")
                break

            # Set the game refresh rate
            clock.tick(game_values["FPS"])

            # Now render all changes we made in this loop
            # iteration onto the game screen.
            pygame.display.update()
