import unittest
import pygame
import pickle
import time

from agent.uninformed_computer import (
    BFSComputer,
    DFSComputer,
    RandomComputer,
    UCSComputer
)
from agent.informed_computer import AStarComputer
from characters.character import get_character_types
from world import World
from constants import (
    player_sprite_file_paths, game_values, pink_enemy_file_sprite_paths,
    MAX_PATH_TEST_TIME
)

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32

# Maze map the functions will use
maze_map = None
with open('maze/maze_tiny_test', 'rb') as file:
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
        self.screen = pygame.display.set_mode((300, 250))

        self.player = get_character_types()["main"](
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

        start_time = time.time()

        running = True

        # Start the path finding algorithm
        self.computer.start_thread()

        # We will stop once two diamonds have been found
        score_count = 0
        TARGET = 2

        # We will run a game loop until collision is detected
        while running:
            self.screen.blit(self.bg, (0, 0))

            # We have found the diamond and can begin to stop the test
            if self.player.get_is_diamond_found():
                self.world.update_diamond_position()
                self.player.set_is_diamond_found_to_false()
                self.diamond_positions = self.world.get_diamond_group()
                self.computer.update_diamond_list(self.diamond_positions)
                score_count += 1

            # Blitting the tiles
            self.world.load_world(self.screen)

            # Moving the player
            self.game_over, remove_diamond_pos = self.computer.move(
                self.screen,
                self.tile_data,
                asset_groups=self.diamond_positions,
                game_over=self.game_over
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

            if time.time() - start_time > MAX_PATH_TEST_TIME:
                running = False
                self.assertFalse(f"Time limit of {MAX_PATH_TEST_TIME} seconds "
                                 "exceeded.")

            # Now render all changes we made in this loop
            # iteration onto the game screen.
            pygame.display.update()

    def tearDown(self):
        pygame.quit()


class TestDFSGUIComputer(TestGUIComputer, unittest.TestCase):
    def setUp(self):
        super().setUp(pos_x=100, pos_y=100)
        self.computer = DFSComputer(
            self.player,
            self.world.get_walkable_maze_matrix()
        )


class TestBFSGUIComputer(TestGUIComputer, unittest.TestCase):
    def setUp(self):
        super().setUp(pos_x=100, pos_y=100)
        self.computer = BFSComputer(
            self.player,
            self.world.get_walkable_maze_matrix()
        )


class TestUCSGUIComputer(TestGUIComputer, unittest.TestCase):
    def setUp(self):
        super().setUp(pos_x=100, pos_y=100)
        self.computer = UCSComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.world.get_diamond_group().sprites()[0]
        )


class TestAstarGUIComputer(TestGUIComputer, unittest.TestCase):
    def setUp(self):
        super().setUp(pos_x=100, pos_y=100)
        self.computer = AStarComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.world.get_diamond_group().sprites()[0]
        )


class TestGUIEnemyCollisionComputer(TestGUIComputer, unittest.TestCase):
    """ This test class will also test the GUI, but this time we will add
    enemies in the game."""
    def setUp(self):
        super().setUp(pos_x=100, pos_y=100)

        self.computer = AStarComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.world.get_diamond_group().sprites()[0]
        )

        self.enemy = get_character_types()["enemy"](
            game_values["character_width"],
            game_values["character_height"],
            maze_map,
            is_controlled_by_computer=True,
            x=150, y=100
        )

        self.enemy.set_char_animation(
            "idle",
            pink_enemy_file_sprite_paths["idle"],
            animation_steps=4
        )
        self.enemy.set_char_animation(
            "walk",
            pink_enemy_file_sprite_paths["walk"],
            animation_steps=6
        )
        self.enemy.set_char_animation(
            "climb",
            pink_enemy_file_sprite_paths["climb"],
            animation_steps=4
        )

        self.enemy_computer = RandomComputer(
            self.enemy,
            self.world.get_walkable_maze_matrix(),
        )

    def testPathFindGUI(self):
        """ This function test for a collision between the enemy and
        main player. """

        # Start the path finding algorithm
        self.computer.start_thread()

        # We will run a game loop until collision is detected
        while not self.game_over:
            self.screen.blit(self.bg, (0, 0))

            # We have found the diamond and can begin to stop the test
            if self.player.get_is_diamond_found():
                self.world.update_diamond_position()
                self.player.set_is_diamond_found_to_false()
                self.diamond_positions = self.world.get_diamond_group()
                self.computer.update_diamond_list(self.diamond_positions)

            # Blitting the tiles
            self.world.load_world(self.screen)

            # Keep the enemy idle to guarantee a collision
            self.enemy_computer.requested_movement = "idle"
            self.enemy_computer.move(
                self.screen,
                self.tile_data
            )

            # Moving the player
            self.game_over, _ = self.computer.move(
                self.screen,
                self.tile_data,
                asset_groups=self.diamond_positions,
                game_over=self.game_over,
                enemy_computers=[self.enemy_computer]
            )

            # End test once enemy collision was detected.
            if self.game_over:
                self.assertTrue(
                    "Test passed as collision with enemy was detected."
                )
                self.computer.stop_thread = True
                break

            # Set the game refresh rate
            clock.tick(game_values["FPS"])

            # Now render all changes we made in this loop
            # iteration onto the game screen.
            pygame.display.update()
