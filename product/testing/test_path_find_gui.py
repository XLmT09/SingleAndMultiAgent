import unittest
import pygame
import pickle

from agent.uninformed_computer import BFSComputer, DFSComputer
from agent.informed_computer import AStarComputer, UCSComputer
from characters import CharacterAnimationManager
from world import World
from constants import player_sprite_file_paths, game_values

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32

# Maze map the functions will use
maze_map = None
with open('maze/maze_1', 'rb') as file:
    maze_map = pickle.load(file)
clock = pygame.time.Clock()


class TestGUIComputer():
    """ Setup class which the other tests classes in this
    file will inherit from.

    Format is similar to main.py, anything not commented here would
    likely be commented over there.
    """
    def setUp(self, pos_x, pos_y):
        """
        Args:
            pos_x (int): x position of the agent.
            pos_y (int): y position of the agent.
        """

        # To avoid frozen screen between tests we will init the display
        # instead of the whole pygame module.
        pygame.display.init()
        self.screen = pygame.display.set_mode((850, 350))

        self.player = CharacterAnimationManager(
            CHARACTER_WIDTH,
            CHARACTER_HEIGHT,
            maze_map,
            True,
            pos_x,
            pos_y,
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

        self.world = World(maze_map)
        self.game_over = 0
        self.tile_data = self.world.get_collidable_tile_list()
        self.diamond_positions = self.world.get_diamond_group()

        self.bg = pygame.image.load(
            "assets/images/background/cave.png"
        ).convert_alpha()

    def testPathFindGUI(self):
        """ This function will run a given path finding algorithm in the
        given initialized maze environment. The test passes if it can collect
        two diamonds without errors. """

        # Start the path finding algorithm
        self.computer.start_thread()

        # We will stop once two diamonds have been found
        score_count = 0
        TARGET = 2

        # We will run a game loop until collision is detected
        while score_count != TARGET:
            self.screen.blit(self.bg, (0, 0))

            # We have found the diamond and can begin to stop the test
            if self.player.get_is_diamond_found():
                self.world.update_diamond_position()
                self.player.set_is_diamond_found_to_false()
                self.diamond_positions = self.world.get_diamond_group()
                score_count += 1

            # Blitting the tiles
            self.world.load_world(self.screen)

            # Moving the player
            self.game_over = self.computer.move(
                self.screen,
                self.tile_data,
                self.diamond_positions,
                self.game_over
            )

            # Can end the test once collision is detected
            if score_count == TARGET:
                self.assertTrue(score_count,
                                f"Test passed as collision {TARGET} diamonds "
                                "were collected without errors.")
                self.computer.stop_thread = True
                break

            # Set the game refresh rate
            clock.tick(game_values["FPS"])

            # Now render all changes we made in this loop
            # iteration onto the game screen.
            pygame.display.update()

    def tearDown(self):
        pygame.quit()


class TestDFSGUIComputer(TestGUIComputer, unittest.TestCase):
    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.computer = DFSComputer(
            self.player,
            self.world.get_walkable_maze_matrix()
        )


class TestBFSGUIComputer(TestGUIComputer, unittest.TestCase):
    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.computer = BFSComputer(
            self.player,
            self.world.get_walkable_maze_matrix()
        )


class TestAstarGUIComputer(TestGUIComputer, unittest.TestCase):
    def setUp(self):
        super().setUp(pos_x=350, pos_y=300)
        self.computer = AStarComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.world.get_diamond_group().sprites()[0]
        )
