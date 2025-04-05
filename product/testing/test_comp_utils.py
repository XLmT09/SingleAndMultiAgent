import pygame
import unittest
import pickle
import time
import copy
import constants as C

from characters.character import get_character_types

from world import World
from constants import player_sprite_file_paths, pink_enemy_file_sprite_paths
from agent.competitive_computer import (
    MinimaxComputer,
    AlphaBetaComputer,
    ExpectimaxComputer
)

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

        enemy_list = []

        enemy_pos = [
            (200, 200),
            (100, 200),
            (400, 400)
        ]

        for enemy_index in range(3):
            x, y = enemy_pos[enemy_index]

            enemy = get_character_types()["enemy"](
                CHARACTER_WIDTH,
                CHARACTER_HEIGHT,
                self.maze_map if self.maze_map else self.default_maze_map,
                is_controlled_by_computer=True,
                x=x, y=y
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

            enemy_list.append(enemy)

        enemy_positions = []

        for enemy in enemy_list:
            enemy_positions.append(enemy.get_player_grid_coordinates())

        self.state = {
            "main_agent": self.player.get_player_grid_coordinates(),
            "enemies": enemy_positions,
            "diamond_positions": diamond_pos,
            "score": 0,
            "win": False,
            "lose": False,
            "diamond_count": 0
        }

        self.minimax_computer = MinimaxComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.diamond,
            state=self.state,
            num_characters=4
        )

        self.alphabeta_computer = AlphaBetaComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.diamond,
            state=self.state,
            num_characters=4
        )

        self.expectimax_computer = ExpectimaxComputer(
            self.player,
            self.world.get_walkable_maze_matrix(),
            diamond=self.diamond,
            state=self.state,
            num_characters=4
        )

    #  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #  ┃ 💡 REMINDER: THIS CODE IS TESTED ON MAZE 8
    #  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def test_legal_movements_left_right(self):
        """Test if the computer can ONLY move left and right, when there
        are no walls.
        """

        legal_moves = self.minimax_computer.legal_movements(
            pos=(1, 3),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["LEFT", "RIGHT"])

    def test_legal_movements_up_down(self):
        """Test if the computer can ONLY move up and down, when they are on a
        ladder with walls on either side."""

        legal_moves = self.minimax_computer.legal_movements(
            pos=(4, 9),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["DOWN", "UP"])

    def test_legal_movements_down_left_right(self):
        """Test if the agent has reached the top of the ladder they can
        ONLY go down, left and right."""

        legal_moves = self.minimax_computer.legal_movements(
            pos=(3, 9),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["LEFT", "RIGHT", "DOWN"])

    def test_legal_movements_left_boundary(self):
        """Test if the agent has reached the left boundary they can ONLY go
        right, note that they will also be able to go up as this grid is a
        ladder."""

        legal_moves = self.minimax_computer.legal_movements(
            pos=(5, 1),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["RIGHT", "UP"])

    def test_legal_movements_right_boundary(self):
        """Test if the agent has reached the right boundary they can ONLY go
        left, note that they will also be able to go up as this grid is a
        ladder."""

        legal_moves = self.minimax_computer.legal_movements(
            pos=(5, 15),
            prev_action=None
        )

        self.assertEqual(legal_moves, ["LEFT", "UP"])

    def test_legal_movements_bottom_of_ladder(self):
        """Test the agent cannot go down when they are at the bottom of the
        ladder."""

        legal_moves = self.minimax_computer.legal_movements(
            pos=(5, 15),
            prev_action=None
        )

        self.assertNotIn("DOWN", legal_moves)

    def test_generate_successors_can_be_applied_to_all_agents(self):
        """Test if the generate_successors function can be applied to all
        agents."""

        calculated_positions = []

        # Before starting test, ensure initial coordinates are correct
        self.assertEqual(
            [(5, 6), (3, 3), (3, 1), (7, 7)],
            [
                self.state["main_agent"],
                self.state["enemies"][0],
                self.state["enemies"][1],
                self.state["enemies"][2]
            ]
        )

        # Index of each agent
        main_agent, enemy_one, enemy_two, enemy_three = 0, 1, 2, 3

        # In this test, we will apply a left movement to all agents
        calculated_positions.append(
            self.minimax_computer.generate_successor(
                self.state,
                main_agent,
                "LEFT"
            )["main_agent"]
        )

        calculated_positions.append(
            self.minimax_computer.generate_successor(
                self.state,
                enemy_one,
                "LEFT"
            )["enemies"][0]
        )

        calculated_positions.append(
            self.minimax_computer.generate_successor(
                self.state,
                enemy_two,
                "LEFT"
            )["enemies"][1]
        )

        calculated_positions.append(
            self.minimax_computer.generate_successor(
                self.state,
                enemy_three,
                "LEFT"
            )["enemies"][2]
        )

        self.assertEqual(
            [(5, 5), (3, 2), (3, 0), (7, 6)],
            calculated_positions
        )

    def test_generate_successors_on_one_enemy_does_not_affect_others(self):
        """Test that when we generate a successor for one enemy, the other
        agents are not affected."""

        # Before starting test, ensure initial coordinates are correct
        self.assertEqual(
            [(5, 6), (3, 3), (3, 1), (7, 7)],
            [
                self.state["main_agent"],
                self.state["enemies"][0],
                self.state["enemies"][1],
                self.state["enemies"][2]
            ]
        )

        # Index of agent
        enemy_two = 2

        # In this test, we will apply a left movement to all agents

        new_agent_pos = self.minimax_computer.generate_successor(
            self.state,
            enemy_two,
            "LEFT"
        )["enemies"][1]

        self.assertEqual(
            [(5, 6), (3, 3), (3, 0), (7, 7)],
            [
                self.state["main_agent"],
                self.state["enemies"][0],
                new_agent_pos,
                self.state["enemies"][2]
            ]
        )

    def test_alphabeta_faster_execution_than_minimax(self):
        """Test that the alphabeta algorithm will run faster than the minimax
        algorithm, on a guaranteed pruning game state."""

        # TODO: The previous enemy positions were out of bounds, so I created
        # new ones. Changing this in the setup would require updating all
        #  previous tests, which would take time, so I’ve left it as is for
        # now.
        new_enemy_pos = [(5, 1), (3, 5), (1, 8)]

        new_state = copy.deepcopy(self.state)

        new_state["enemies"] = new_enemy_pos

        start = time.time()

        self.minimax_computer.minimax(
            new_state,
            depth=2,
            agent_index=0
        )
        end = time.time()

        minimax_time = end - start

        start = time.time()
        self.alphabeta_computer.minimax(
            new_state,
            depth=2,
            agent_index=0
        )
        end = time.time()

        alphabeta_computer = end - start

        self.assertGreater(minimax_time, alphabeta_computer)

    def test_expectimax_probability_func_normal_movements(self):
        """Test the expectimax probability function gives the expected
         probability values for each direction. The function splits the
         probability equally and there are 3 legal directions in this context.
         Therefore, the expected probability is 1/3."""

        # In this position, the enemy can move left, right or up.
        enemy_pos = (5, 9)

        prob_output = self.expectimax_computer.get_enemy_actions_with_probs(
            enemy_pos
        )

        self.assertEqual([
            ('LEFT', 1/3),
            ('RIGHT', 1/3),
            ('UP', 1/3)
        ], prob_output)

    def test_expectimax_probability_func_one_move(self):
        """Test the expectimax probability function will give probability of 1
         when it can only move in one direction. This could be because there
         is a wall to the left or right."""

        # temporarily remove ladders, to restrict movement only right
        self.expectimax_computer._walkable_maze_matrix[5][1] = C.WALKABLE_GRID
        self.expectimax_computer._walkable_maze_matrix[4][1] = C.WALKABLE_GRID

        # In this position, the enemy can only move right.
        enemy_pos = (5, 1)

        prob_output = self.expectimax_computer.get_enemy_actions_with_probs(
            enemy_pos
        )

        self.assertEqual([
            ('RIGHT', 1),
        ], prob_output)

        # restore ladders
        self.expectimax_computer._walkable_maze_matrix[5][1] = C.LADDER_GRID
        self.expectimax_computer._walkable_maze_matrix[4][1] = C.LADDER_GRID

    def test_expectimax_probability_func_no_move(self):
        """Test the expectimax probability function will return an empty list
        when there are no legal moves."""

        # temporarily block enemy path, to restrict movements
        self.expectimax_computer._walkable_maze_matrix[5][1] = C.WALKABLE_GRID
        self.expectimax_computer._walkable_maze_matrix[4][1] = C.WALKABLE_GRID
        self.expectimax_computer._walkable_maze_matrix[5][2] = (
            C.NON_WALKABLE_GRID
        )

        # In this position, the enemy can not make a legal move.
        enemy_pos = (5, 1)

        prob_output = self.expectimax_computer.get_enemy_actions_with_probs(
            enemy_pos
        )

        self.assertEqual([], prob_output)

        # restore matrix
        self.expectimax_computer._walkable_maze_matrix[5][1] = C.LADDER_GRID
        self.expectimax_computer._walkable_maze_matrix[4][1] = C.LADDER_GRID
        self.expectimax_computer._walkable_maze_matrix[5][2] = C.WALKABLE_GRID

    def tearDown(self):
        pygame.quit()
