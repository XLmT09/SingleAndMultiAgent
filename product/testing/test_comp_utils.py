import pygame
import unittest
import pickle

from characters.character import get_character_types

from world import World
from constants import player_sprite_file_paths, pink_enemy_file_sprite_paths
from agent.competitive_computer import MinimaxComputer

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 32
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
# Test cases will generate the maze map
maze_map = None


class TestCompetitiveUtils(unittest.TestCase):
    """ Test tools (functions) in a competitive computer class is
    working properly. """

    # Load up a default map for use if child class does not load a maze
    default_maze_map = None
    with open('maze/maze_8', 'rb') as file:
        default_maze_map = pickle.load(file)
    maze_map = None

    def setUp(self, player_pos_x=350, player_pos_y=300):
        """
        Args:
            pos_x (int): x position of the agent.
            pos_y (int): y position of the agent.
        """
        pygame.init()
        pygame.display.set_mode((1, 1), 0, 32)

        self.player = get_character_types()["main"](
            CHARACTER_WIDTH,
            CHARACTER_HEIGHT,
            self.maze_map if self.maze_map else self.default_maze_map,
            True, player_pos_x,
            player_pos_y
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

        self.world = World(
            self.maze_map if self.maze_map else self.default_maze_map
        )

        # We need to know the goal state for these tests so get the
        # diamond object.
        self.diamond = self.world.get_diamond_group().sprites()[0]

        diamond_pos = (
            [
                (dmd.grid_y, dmd.grid_x) for
                dmd in self.world.get_diamond_group()
            ]
        )

        enemy = get_character_types()["enemy"](
            CHARACTER_WIDTH,
            CHARACTER_HEIGHT,
            self.maze_map if self.maze_map else self.default_maze_map,
            is_controlled_by_computer=True,
            x=200, y=200
        )

        enemy.set_char_animation(
            "idle",
            pink_enemy_file_sprite_paths["idle"],
            animation_steps=4
        )
        enemy.set_char_animation(
            "walk",
            pink_enemy_file_sprite_paths["walk"],
            animation_steps=6
        )
        enemy.set_char_animation(
            "climb",
            pink_enemy_file_sprite_paths["climb"],
            animation_steps=4
        )
        enemy.set_char_animation(
            "jump",
            pink_enemy_file_sprite_paths["jump"],
            animation_steps=8
        )

        state = {
            "main_agent": self.player.get_player_grid_coordinates(),
            "enemies": enemy.get_player_grid_coordinates(),
            "diamond_positions": diamond_pos,
            "score": 0,
            "win": False,
            "lose": False,
            "diamond_count": 0
        }

        self.computer = MinimaxComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.diamond,
            state=state
        )

    #  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #  ┃ 💡 REMINDER: THIS CODE IS TESTED ON MAZE 8
    #  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def test_legal_movements_left_right(self):
        """Test if the computer can ONLY move left and right, when there
        are no walls.
        """

        legal_moves = self.computer.legal_movements(
            pos=(1, 3),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["LEFT", "RIGHT"])

    def test_legal_movements_up_down(self):
        """Test if the computer can ONLY move up and down, when they are on a
        ladder with walls on either side."""

        legal_moves = self.computer.legal_movements(
            pos=(4, 9),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["DOWN", "UP"])

    def test_legal_movements_down_left_right(self):
        """Test if the agent has reached the top of the ladder they can
        ONLY go down, left and right."""

        legal_moves = self.computer.legal_movements(
            pos=(3, 9),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["LEFT", "RIGHT", "DOWN"])

    def test_legal_movements_left_boundary(self):
        """Test if the agent has reached the left boundary they can ONLY go
        right, note that they will also be able to go up as this grid is a
        ladder."""

        legal_moves = self.computer.legal_movements(
            pos=(5, 1),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["RIGHT", "UP"])

    def test_legal_movements_right_boundary(self):
        """Test if the agent has reached the right boundary they can ONLY go
        left, note that they will also be able to go up as this grid is a
        ladder."""

        legal_moves = self.computer.legal_movements(
            pos=(5, 15),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["LEFT", "UP"])

    def tearDown(self):
        pygame.quit()
