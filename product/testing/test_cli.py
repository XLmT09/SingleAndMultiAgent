import unittest
from unittest.mock import patch
from main import process_args


class TestCli(unittest.TestCase):
    """This class will test the cli flags the user can use 
    for this application."""

    @patch('sys.argv', ['main', '--size', 'small', '--algo', 'bfs'])
    def test_small_size_and_bfs(self):
        """ This tests to see the correct width and height are produced
        for a small maze. It also tests id bfs is recorded as a valuse
        in the algo key. """
        result = process_args()
        self.assertEqual(result["screen_width"], 850)
        self.assertEqual(result["screen_height"], 350)
        self.assertEqual(result["maze_path"], "maze/maze_1")
        self.assertEqual(result["algo"], "bfs")

    @patch('sys.argv', ['main', '--size', 'medium', '--algo', 'dfs'])
    def test_small_size_and_dfs(self):
        """ his tests to see the correct width and height are produced
        for a medium maze. It also tests id dfs is recorded as a valuse
        in the algo key. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1000)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_2")
        self.assertEqual(result["algo"], "dfs")

    @patch('sys.argv', ['main', '--size', 'large', '--algo', 'ucs'])
    def test_large_size_and_dfs(self):
        """ This tests to see the correct width and height are produced
        for a large maze. It also tests id  is recorded as a valuse
        in the algo key. """
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_3")
        self.assertEqual(result["algo"], "ucs")

    @patch('sys.argv', ['program_name', '--size', 'bogus', '--algo', 'BFS'])
    def test_invalid_size_argument(self):
        """ Give the size flag an invalid value and check that
        it throws a error. """
        # argparse calls sys.exit() on a invlaid input
        with self.assertRaises(SystemExit):
            process_args()

    @patch('sys.argv', ['program_name', '--size', 'small', '--algo', 'bogus'])
    def test_invalid_algo_argument(self):
        """ Give the algo flag an invalid value and check that
        it throws a error. """
        # argparse calls sys.exit() on a invlaid input
        with self.assertRaises(SystemExit):
            process_args()

    @patch('sys.argv', ['program_name', '--size', 'bogus', '--algo', 'bogus'])
    def test_invalid_algo_and_size_argument(self):
        """ Give the algo and size flag an invalid value and check that
        it throws a error. """
        # argparse calls sys.exit() on a invlaid input
        with self.assertRaises(SystemExit):
            process_args()

    @patch('sys.argv', ['program_name', '--algo', 'bfs'])
    def test_no_size_flag(self):
        """ Dont pass a size flag and we expect to see an error
        as this flag is needed for the application to decided
        what type of maze to generate."""
        # argparse calls sys.exit() on a invlaid input
        with self.assertRaises(SystemExit):
            process_args()

    @patch('sys.argv', ['program_name', '--size', 'small'])
    def test_no_algo_flag(self):
        """ Dont pass a algo flag and we expect to see an error
        as this flag is needed for the application to decided
        what type of agent to use."""
        # argparse calls sys.exit() on a invlaid input
        with self.assertRaises(SystemExit):
            process_args()

    @patch('sys.argv', ['program_name'])
    def test_no_size_and_algo_flag(self):
        """ Dont pass a algo adn size flag and we expect to see an error
        as the application will not know the type of maze and agent to use."""
        # argparse calls sys.exit() on a invlaid input
        with self.assertRaises(SystemExit):
            process_args()
