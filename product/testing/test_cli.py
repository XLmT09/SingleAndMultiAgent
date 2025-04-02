import io
import unittest
import constants as C
import main

from unittest.mock import patch
from cli import process_args


class TestCli(unittest.TestCase):
    """This class will test the cli flags the user can use
    for this application."""

    @patch('sys.argv', ['main', '--size', 'small', '--algo', 'bfs'])
    def test_small_size_and_bfs(self):
        """ This tests to see the correct width and height are produced
        for a small maze. It also tests id bfs is recorded as a values
        in the algo key. """
        result = process_args()
        self.assertEqual(result["screen_width"], 850)
        self.assertEqual(result["screen_height"], 350)
        self.assertEqual(result["maze_path"], "maze/maze_1")
        self.assertEqual(result["algo"], "bfs")

    @patch('sys.argv', ['main', '--size', 'small-filled'])
    def test_small_filled_maze(self):
        """ This tests to see correct small filled maze is generated """
        result = process_args()
        self.assertEqual(result["screen_width"], 850)
        self.assertEqual(result["screen_height"], 350)
        self.assertEqual(result["maze_path"], "maze/maze_5")

    @patch('sys.argv', ['main', '--size', 'medium', '--algo', 'dfs'])
    def test_small_size_and_dfs(self):
        """ This tests to see the correct width and height are produced
        for a medium maze. It also tests id dfs is recorded as a values
        in the algo key. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1000)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_2")
        self.assertEqual(result["algo"], "dfs")

    @patch('sys.argv', ['main', '--size', 'medium-filled'])
    def test_mid_filled_maze(self):
        """ This tests to see correct medium filled maze and attributes
        are generated. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1000)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_6")

    @patch('sys.argv', ['main', '--size', 'large', '--algo', 'ucs'])
    def test_large_size_and_ucs(self):
        """ This tests to see the correct width and height are produced
        for a large maze. It also tests id  is recorded as a values
        in the algo key. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_3")
        self.assertEqual(result["algo"], "ucs")

    @patch('sys.argv', ['main', '--size', 'large-filled'])
    def test_large_filled_maze(self):
        """ This tests to see correct large filled maze and attributes
        are generated. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_7")

    @patch('sys.argv', ['main', '--size', 'large', '--algo', 'astar'])
    def test_large_size_and_a_star(self):
        """ Test A star algo is registered. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_3")
        self.assertEqual(result["algo"], "astar")

    @patch('sys.argv', ['main', '--size', 'large-filled', '--algo', 'greedy'])
    def test_large_size_and_greedy_algo(self):
        """ Test greedy algo is registered. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_7")
        self.assertEqual(result["algo"], "greedy")

    @patch('sys.argv', ['main', '--size', 'small-filled', '--algo', 'minimax',
           '--enemy_count', '1'])
    def test_small_filled_maze_comp_algo(self):
        """ Test that for a comp algo, it will output maze 8 instead of 5. """
        result = process_args()
        self.assertEqual(result["screen_width"], 850)
        self.assertEqual(result["screen_height"], 350)
        self.assertEqual(result["maze_path"], "maze/maze_8")
        self.assertEqual(result["algo"], "minimax")

    @patch('sys.argv', ['main', '--size', 'large-filled', '--algo', 'astar'])
    def test_large_size_and_a_star_filled_algo(self):
        """ Test a star filled algo is registered. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_7")
        self.assertEqual(result["algo"], "astarFilled")

    @patch('sys.argv',
           ['main', '--size', 'large', '--algo', 'astar', '--weighted'])
    def test_weighted_a_star(self):
        """ Test A star algo is works with weighted flag. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_3")
        self.assertEqual(result["algo"], "astar")
        self.assertEqual(result["weighted"], True)

    def test_cli_fails_when_weighted_set_on_non_a_star_algo(self):
        """ Test the cli will fail when the user inputs a non astar algorithm
        with the weighted flag. """
        algos = ["bfs", "dfs", "ucs", "random"]

        for algo in algos:
            with patch('sys.stderr', new_callable=io.StringIO) as fake_stderr:
                with patch(
                    'sys.argv',
                    ['main', '--size', 'small', '--algo', algo, '--weighted']
                ):
                    with self.assertRaises(SystemExit):
                        process_args()

                # Capture the error message printed to stderr
                error_output = fake_stderr.getvalue()

                # Check if the error message is the expected one
                self.assertIn("error: --weighted is only applicable when "
                              "using the A* algorithm.", error_output)

    @patch('sys.argv', ['main', '--algo', 'ucs', '--size', 'small'])
    def test_algo_then_size_flag_given(self):
        """ Test cli will still work when we switch the flag order. """
        result = process_args()
        self.assertEqual(result["screen_width"], 850)
        self.assertEqual(result["screen_height"], 350)
        self.assertEqual(result["maze_path"], "maze/maze_1")
        self.assertEqual(result["algo"], "ucs")

    @patch('sys.argv', ['main', '--algo', 'random', '--size', 'small'])
    def test_cli_random_algo(self):
        """ Test cli with random as algo value. """
        result = process_args()
        self.assertEqual(result["screen_width"], 850)
        self.assertEqual(result["screen_height"], 350)
        self.assertEqual(result["maze_path"], "maze/maze_1")
        self.assertEqual(result["algo"], "random")

    @patch('sys.argv', ['main', '--algo', 'minimax', '--size', 'small',
           '--enemy_count', '1'])
    def test_cli_minimax_algo(self):
        """ Test cli with minimax as algo value. """
        result = process_args()
        self.assertEqual(result["screen_width"], 850)
        self.assertEqual(result["screen_height"], 350)
        self.assertEqual(result["maze_path"], "maze/maze_1")
        self.assertEqual(result["algo"], "minimax")

    @patch('sys.argv', ['main', '--size', 'bogus', '--algo', 'BFS'])
    def test_invalid_size_argument(self):
        """ Give the size flag an invalid value and check that
        it throws a error. """
        # Redirect stderr to prevent error message from printing
        with patch('sys.stderr', new=io.StringIO()):
            # argparse calls sys.exit() on a invalid input
            with self.assertRaises(SystemExit):
                process_args()

    @patch('sys.argv', ['main', '--size', 'small', '--algo', 'bogus'])
    def test_invalid_algo_argument(self):
        """ Give the algo flag an invalid value and check that
        it throws a error. """
        # Redirect stderr to prevent error message from printing
        with patch('sys.stderr', new=io.StringIO()):
            # argparse calls sys.exit() on a invalid input
            with self.assertRaises(SystemExit):
                process_args()

    @patch('sys.argv', ['main', '--size', 'bogus', '--algo', 'bogus'])
    def test_invalid_algo_and_size_argument(self):
        """ Give the algo and size flag an invalid value and check that
        it throws a error. """
        # Redirect stderr to prevent error message from printing
        with patch('sys.stderr', new=io.StringIO()):
            # argparse calls sys.exit() on a invalid input
            with self.assertRaises(SystemExit):
                process_args()

    @patch('sys.argv', ['main', '--algo', 'bfs'])
    def test_no_size_flag(self):
        """ Dont pass a size flag and we expect to see an error
        as this flag is needed for the application to decided
        what type of maze to generate."""
        # Redirect stderr to prevent error message from printing
        with patch('sys.stderr', new=io.StringIO()):
            # argparse calls sys.exit() on a invalid input
            with self.assertRaises(SystemExit):
                process_args()

    @patch('sys.argv', ['main'])
    def test_no_size_and_algo_flag(self):
        """ Dont pass a algo adn size flag and we expect to see an error
        as the application will not know the type of maze and agent to use."""
        # argparse calls sys.exit() on a invalid input
        # Redirect stderr to prevent error message from printing
        with patch('sys.stderr', new=io.StringIO()):
            # argparse calls sys.exit() on a invalid input
            with self.assertRaises(SystemExit):
                process_args()

    @patch('sys.argv', ['main', '--algo', 'ucs', '--size', 'small',
                        '--highlight'])
    def test_cli_highlight_flag_input(self):
        """ Test checks that when highlight flag is given it is registered as
        True in the config dict. """
        result = process_args()
        self.assertEqual(result["enable_highlighter"], True)

    @patch('sys.argv', ['main', '--algo', 'ucs', '--size', 'small'])
    def test_cli_highlight_flag_no_given(self):
        """ Test checks that when highlight flag is not given it is registered
        as False in the config dict by default."""
        result = process_args()
        self.assertEqual(result["enable_highlighter"], False)

    @patch('sys.argv', ['main', '--size', 'small', '--highlight'])
    def test_cli_fails_when_highlight_and_no_algo_given(self):
        """ Test the cli will fail when no algo is given and
        highlight flag is enabled. """

        # Redirect stderr to prevent error message from printing
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            # argparse calls sys.exit() on a invalid input
            with self.assertRaises(SystemExit):
                process_args()

            error_output = fake_stderr.getvalue()

            self.assertIn("--highlight is only applicable when using any "
                          "algorithm but random.", error_output)

    @patch(
        'sys.argv',
        ['main', '--size', 'small', '--algo', 'random', '--highlight']
    )
    def test_cli_fails_when_highlight_and_random_algo_given(self):
        """ Test the cli will fail when random algo is given and
        highlight flag is enabled. """

        # Redirect stderr to prevent error message from printing
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            # argparse calls sys.exit() on a invalid input
            with self.assertRaises(SystemExit):
                process_args()

            error_output = fake_stderr.getvalue()

            self.assertIn("--highlight is only applicable when using any "
                          "algorithm but random.", error_output)

    def test_cli_fails_when_filled_maze_and_not_using_filled_algo(self):
        """ Test the cli will fail when we are in a filled maze but using an
        algorithm not compatible with filled mazes. """

        incompatible_algos = ["bfs", "dfs", "ucs"]

        for algo in incompatible_algos:
            with patch('sys.stderr', new_callable=io.StringIO) as fake_stderr:
                with patch(
                    'sys.argv',
                    ['main', '--size', 'small-filled', '--algo', algo]
                ):
                    with self.assertRaises(SystemExit):
                        process_args()

                # Capture the error message printed to stderr
                error_output = fake_stderr.getvalue()

                # Check if the error message is the expected one
                self.assertIn(
                    "error: Filled maze only works when user controlled or "
                    "when using greedy algorithm.",
                    error_output
                )

    @patch('sys.argv', ['main', '--algo', 'ucs', '--size', 'small',
                        '--enemy_count', '3'])
    def test_cli_enemy_count(self):
        """ Test checks enemy_count value given by user is registered."""
        result = process_args()
        self.assertEqual(result["enemy_count"], 3)

    @patch('sys.argv', ['main', '--algo', 'ucs', '--size', 'small'])
    def test_cli_enemy_count_default(self):
        """ Test checks that when enemy count value is not given, then by
        default it should be 0"""
        result = process_args()
        self.assertEqual(result["enemy_count"], 0)

    def test_cli_fails_on_minimax_with_zero_enemies(self):
        """ Test the cli will fail when we are in a filled maze but using an
        algorithm not compatible with filled mazes. """

        incompatible_algos = ["bfs", "dfs", "ucs"]

        for algo in incompatible_algos:
            with patch('sys.stderr', new_callable=io.StringIO) as fake_stderr:
                with patch(
                    'sys.argv',
                    ['main', '--size', 'small-filled', '--algo', algo]
                ):
                    with self.assertRaises(SystemExit):
                        process_args()

                # Capture the error message printed to stderr
                error_output = fake_stderr.getvalue()

                # Check if the error message is the expected one
                self.assertIn(
                    "error: Filled maze only works when user controlled or "
                    "when using greedy algorithm.",
                    error_output
                )

    @patch(
        'sys.argv',
        ['main', '--size', 'small-filled', '--algo', 'minimax',
         '--enemy_count', str(C.MAX_ENEMIES + 1)]
    )
    def test_cli_fails_on_too_many_enemies(self):
        """ Test the cli will fail when the user gives a enemy count greater
        than the max enemies allowed. """

        # Redirect stderr to prevent error message from printing
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            # argparse calls sys.exit() on a invalid input
            with self.assertRaises(SystemExit):
                process_args()

            error_output = fake_stderr.getvalue()

            # Check if the error message is the expected one
            self.assertIn(
                f"Enemy count cannot be greater than {C.MAX_ENEMIES}.",
                error_output
            )

    @patch(
        'sys.argv',
        ['main', '--size', 'small', '--algo', 'random', '--explain']
    )
    def test_cli_explain_random_algo(self):
        """ Test CLI gives correct explanation for random algo. It is vital
        that we do not mislead the user of how an algorithm works. """

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            main.process_args()
            captured_output = fake_stdout.getvalue()

        self.assertIn("EXPLANATION: Random algorithm chooses a random path to "
                      "take, which may not be optimal.", captured_output)

    @patch(
        'sys.argv',
        ['main', '--size', 'small', '--algo', 'dfs', '--explain']
    )
    def test_cli_explain_dfs_algo(self):
        """ Test CLI gives correct explanation for dfs algo. It is vital
        that we do not mislead the user of how an algorithm works. """

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            main.process_args()
            captured_output = fake_stdout.getvalue()

        self.assertIn(
            "EXPLANATION: Depth First Search (DFS) explores as far as possible"
            " along each branch before backtracking.",
            captured_output
        )
