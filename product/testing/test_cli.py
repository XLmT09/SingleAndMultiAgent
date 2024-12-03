import unittest
from unittest.mock import patch
from main import process_args


class TestCli(unittest.TestCase):
    """This class will test the cli flags the user can use 
    for this application."""

    @patch('sys.argv', ['main', '--size', 'small', '--algo', 'bfs'])
    def test_small_size_and_bfs(self):
        """This tests to see the correct width and height are produced
        for a small maze. It also tests id bfs is recorded as a valuse
        in the algo key."""
        result = process_args()
        self.assertEqual(result["screen_width"], 850)
        self.assertEqual(result["screen_height"], 350)
        self.assertEqual(result["maze_path"], "maze/maze_1")
        self.assertEqual(result["algo"], "bfs")

    @patch('sys.argv', ['main', '--size', 'medium', '--algo', 'dfs'])
    def test_small_size_and_dfs(self):
        """This tests to see the correct width and height are produced
        for a medium maze. It also tests id dfs is recorded as a valuse
        in the algo key."""
        result = process_args()
        self.assertEqual(result["screen_width"], 1000)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_2")
        self.assertEqual(result["algo"], "dfs")

    @patch('sys.argv', ['main', '--size', 'large', '--algo', 'ucs'])
    def test_large_size_and_dfs(self):
        """This tests to see the correct width and height are produced
        for a medium maze. It also tests id dfs is recorded as a valuse
        in the algo key."""
        result = process_args()
        self.assertEqual(result["screen_width"], 1400)
        self.assertEqual(result["screen_height"], 750)
        self.assertEqual(result["maze_path"], "maze/maze_3")
        self.assertEqual(result["algo"], "ucs")
