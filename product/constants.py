##############################################################################
#                             GENERAL CONSTANTS                              #
##############################################################################
# Some global constants to be used
PASS = 1
FAIL = 0

TILE_SIZE = 50
ANIMATION_COOLDOWN = 120

game_values = {
    "character_width": 32,
    "character_height": 32,
    "FPS": 60
}

##############################################################################
#                                 ASCII ART                                  #
##############################################################################
GAME_OVER = (
    "  ____                         ___                 \n"        # noqa: E501
    " / ___| __ _ _ __ ___   ___   / _ \\__   _____ _ __ \n"       # noqa: E501
    "| |  _ / _` | '_ ` _ \\ / _ \\ | | | \\ \\ / / _ \\ '__|\n"   # noqa: E501
    "| |_| | (_| | | | | | |  __/ | |_| |\\ V /  __/ |   \n"       # noqa: E501
    " \\____|\\__,_|_| |_| |_|\\___|  \\___/  \\_/ \\___|_|   \n"  # noqa: E501
)

##############################################################################
#                               GAME CONSTANTS                              #
##############################################################################

# Max enemies allowed in the game
MAX_ENEMIES = 3

# Max time path finding algos in test can run for
MAX_PATH_TEST_TIME = 20

# grid type
FREE_GRID = 0
DIAMOND_GRID = 2
LADDER_GRID = 3
SLOW_GRID = 4

# Walkable
NON_WALKABLE_GRID = 0
WALKABLE_GRID = 1

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED_TRANSPARENT = (255, 0, 0, 150)
BLUE_TRANSPARENT = (0, 0, 255, 150)

colour_vals = {
    "black": BLACK,
    "white": WHITE,
    "red_transparent": RED_TRANSPARENT,
    "blue_transparent": BLUE_TRANSPARENT
}

##############################################################################
#                                 Analytics                                  #
##############################################################################

# fix positions where diamonds get regenerated
# There are 9 positions + 1 more that automatically gets generated in maze
# initialization.
small_regeneration = [
    (1, 2), (3, 13), (3, 1), (1, 9), (1, 6),
    (3, 2), (5, 2), (5, 10), (5, 12)
]

mid_regeneration = [
    (5, 15), (11, 17), (13, 13), (5, 1), (1, 14),
    (3, 6), (7, 10), (9, 6), (11, 7)
]

large_regeneration = [
    (1, 5), (11, 12), (13, 10), (13, 2), (5, 25), (9, 20), (7, 6), (9, 13),
    (13, 11)
]


##############################################################################
#                                 FILE PATHS                                 #
##############################################################################

player_sprite_file_paths = {
    "idle": "assets/images/characters/Dude_Monster/Dude_Monster_Idle_4.png",
    "jump": "assets/images/characters/Dude_Monster/Dude_Monster_Jump_8.png",
    "walk": "assets/images/characters/Dude_Monster/Dude_Monster_Walk_6.png",
    "climb": "assets/images/characters/Dude_Monster/Dude_Monster_Climb_4.png"
}

pink_enemy_file_sprite_paths = {
    "idle": "assets/images/characters/Pink_Monster/Pink_Monster_Idle_4.png",
    "walk": "assets/images/characters/Pink_Monster/Pink_Monster_Walk_6.png",
    "climb": "assets/images/characters/Pink_Monster/Pink_Monster_Climb_4.png",
    "jump": "assets/images/characters/Pink_Monster/Pink_Monster_Jump_8.png",
}

# unlike the player, the diamond sprite images are in separate files and
# not the same on so we need to iterate through the paths and store in
# a list
NUM_DIAMOND_SPRITE_IMAGES = 8
diamond_sprite_images = []

for i in range(1, NUM_DIAMOND_SPRITE_IMAGES + 1):
    diamond_sprite_images.append(
        f"assets/images/pixel-art-diamond/diamond{i}.png")


##############################################################################
#                                  CLI LOGIC                                 #
##############################################################################

# list of useable algorithms
ALGOS = [
    "random",
    "dfs",
    "bfs",
    "ucs",
    "astar",
    "greedy",
    "minimax",
    "alphabeta",
    "expectimax",
]

# Algorithms which are intended to work with at least one enemy agent
# present.
COMPETITIVE_ALGOS = [
    "minimax",
    "alphabeta",
    "expectimax",
]

HIGHLIGHT_ALGOS = [
    "dfs",
    "bfs",
    "ucs",
    "astar",
    "greedy"
]

# Algorithms that are compatible with diamond filled mazes.
FILLED_COMPETITIVE_ALGOS = [
    "greedy", "random", "astar", "minimax", "alphabeta", "expectimax"
]

ERROR_COMP_NON_FILLED = (
    f"Cannot use competitive algos ({COMPETITIVE_ALGOS}) in a non filled"
    " maze. Please enter a maze size in this format <maze_size>-filled."
)

ERROR_HIGHLIGHT_COMPATIBILITY = (
    f"highlight flag will only work for these algos: {HIGHLIGHT_ALGOS}"
)

ERROR_0_LESS_ENEMY = {
    f"enemy count cannot be zero or less for the following algos: "
    f"{COMPETITIVE_ALGOS}"
}
