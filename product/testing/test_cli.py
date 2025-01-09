import unittest
from unittest.mock import patch
from main import process_args

import io


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

    @patch('sys.argv', ['main', '--size', 'medium', '--algo', 'dfs'])
    def test_small_size_and_dfs(self):
        """ his tests to see the correct width and height are produced
        for a medium maze. It also tests id dfs is recorded as a values
        in the algo key. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1000)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_2")
        self.assertEqual(result["algo"], "dfs")

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

    @patch('sys.argv', ['main', '--size', 'large', '--algo', 'astar'])
    def test_large_size_and_a_star(self):
        """ Test A star algo is registered. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_3")
        self.assertEqual(result["algo"], "astar")

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

    @patch('sys.argv', ['main', '--size', 'small'])
    def test_no_algo_flag(self):
        """ Dont pass a algo flag and we expect to see an error
        as this flag is needed for the application to decided
        what type of agent to use."""
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

    @patch('sys.argv', ['main', '--algo', 'random', '--size', 'small',
                        '--highlight'])
    def test_cli_highlight_flag_disabled_on_random(self):
        """ Test that when we use the random algo, the highlighter will remain
        disabled even when the user passes adds the flag."""
        result = process_args()
        self.assertEqual(result["algo"], "random")
        self.assertEqual(result["enable_highlighter"], False)
