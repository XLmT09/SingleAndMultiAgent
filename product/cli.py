import argparse
import constants as C


def explain_algo(algo: str) -> None:
    """ This function will explain the algorithm passed in by the user. """

    if algo == "random":
        print(
            "EXPLANATION: Random algorithm chooses a random path to take, "
            "which may not be optimal."
        )
    elif algo == "dfs":
        print(
            "EXPLANATION: Depth First Search (DFS) explores as far as "
            "possible along each branch before backtracking."
        )
    elif algo == "bfs":
        print(
            "EXPLANATION: Breadth First Search (BFS) explores all neighbors "
            "at the present depth prior to moving on to nodes at the next "
            "depth level."
        )
    elif algo == "ucs":
        print(
            "EXPLANATION: Uniform Cost Search (UCS) is a search algorithm "
            "that expands the least cost node first."
        )
    elif algo == "astar":
        print(
            "EXPLANATION: A* is a graph traversal and pathfinding algorithm "
            "that is efficient and finds the shortest path."
        )
    elif algo == "greedy":
        print(
            "EXPLANATION: Greedy Best-First Search algorithm selects the "
            "path that appears to be the best at the moment."
        )
    elif algo == "minimax":
        print(
            "EXPLANATION: Minimax algorithm is used in decision-making and "
            "game theory, to minimize the possible loss for a worst-case "
            "scenario."
        )
    elif algo == "alphabeta":
        print(
            "EXPLANATION: Alpha-Beta pruning is an optimization technique "
            "for the minimax algorithm that reduces the number of nodes "
            "evaluated."
        )
    elif algo == "expectimax":
        print(
            "EXPLANATION: Expectimax is a decision-making algorithm used in "
            "game theory that considers the expected utility of actions."
        )


def process_args() -> dict:
    """ This function takes the flags passed in by the user and
    will process them.

    Returns:
        dict: data gathered from user CLI input.
    """

    # Some values we will pass into the return dict.
    screen_width, screen_height, maze, filled = None, None, None, False

    # This is used to define, manage and parser the command line args.
    parser = argparse.ArgumentParser()

    # define the size flag
    parser.add_argument(
        "--size",
        choices=[
            "small", "medium", "large",
            "small-filled", "medium-filled", "large-filled"
        ],
        required=True,
        help="Choose a size: small, medium, or large"
    )

    # define the algo flag
    parser.add_argument(
        "--algo",
        choices=C.ALGOS,
        required=False,
        help=f"Choose a algorithm: {C.ALGOS}"
    )

    parser.add_argument(
        "--weighted",
        action="store_true",
        help="Use a weighted manhattan (x2) to influence the "
             "pathfinding (only applicable to A*)."
    )

    # define the algo flag
    parser.add_argument(
        "--highlight",
        action="store_true",
        required=False,
        help="Highlights the visited grids and final path before moving the"
             " agent"
    )

    parser.add_argument(
        "--enemy_count",
        type=int,
        default=0,
        required=False,
        help="The number of enemies to appear in the game."
    )

    parser.add_argument(
        "--explain",
        action="store_true",
        required=False,
        help="Gives a brief explanation of an algorithm, set by --algo."
    )

    # parse args from command line
    args = parser.parse_args()

    # TODO: Currently competitive algorithms do not work with non-filled mazes,
    # due to logic behind the diamond_group variable in world.py. So for now
    # throw an error if the user tries to input this combination in the cli.
    if "filled" not in args.size and args.algo in C.COMPETITIVE_ALGOS:
        parser.error(C.ERROR_COMP_NON_FILLED)

    # setup the window width and height, depending on
    # the size the user specified.
    if "small" in args.size:
        screen_width = 850
        screen_height = 350
        # retrieve the small maze filled with diamonds
        if "filled" in args.size:
            if args.algo in C.COMPETITIVE_ALGOS:
                maze = "maze/maze_8"
            else:
                maze = "maze/maze_5"
            filled = True
        else:
            maze = "maze/maze_1"
    elif "medium" in args.size:
        screen_width = 1000
        screen_height = 750
        if "filled" in args.size:
            if args.algo in C.COMPETITIVE_ALGOS:
                maze = "maze/maze_9"
            else:
                maze = "maze/maze_6"
            filled = True
        else:
            maze = "maze/maze_2"
    elif "large" in args.size:
        screen_width = 1400
        screen_height = 750
        if "filled" in args.size:
            if args.algo in C.COMPETITIVE_ALGOS:
                maze = "maze/maze_10"
            else:
                maze = "maze/maze_7"
            filled = True
        else:
            maze = "maze/maze_3"

    if args.explain:
        explain_algo(args.algo)

    # PERFORM VALIDATION ON USER INPUT

    if args.weighted and args.algo != "astar":
        parser.error("--weighted is only applicable when using the "
                     "A* algorithm.")

    if ((not args.algo and args.highlight) or
       (args.algo == "random" and args.highlight)):
        parser.error(
            "--highlight is only applicable when using any algorithm but "
            "random."
        )

    if (args.algo and filled and not
       (args.algo in C.FILLED_COMPETITIVE_ALGOS)):
        parser.error(
            f"Filled maze only works when user controlled or when using "
            f"the following algos: {C.FILLED_COMPETITIVE_ALGOS}"
        )

    if args.algo == "minimax" and args.enemy_count == 0:
        parser.error(
            "Minimax algorithm requires at least one enemy to be present."
        )

    if args.enemy_count > C.MAX_ENEMIES:
        parser.error(
            f"Enemy count cannot be greater than {C.MAX_ENEMIES}."
        )

    # If we are in a filled maze and using astar then update astar to work in
    # a filled maze context.
    if filled and args.algo == "astar":
        args.algo = "astarFilled"

    return {
        "maze_path": maze,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "algo": args.algo,
        "enable_highlighter": args.highlight,
        "weighted": args.weighted,
        "filled": filled,
        "enemy_count": args.enemy_count
    }
