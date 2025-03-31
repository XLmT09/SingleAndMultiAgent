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

GAME_OVER = (
    "  ____                         ___                 \n"        # noqa: E501
    " / ___| __ _ _ __ ___   ___   / _ \\__   _____ _ __ \n"       # noqa: E501
    "| |  _ / _` | '_ ` _ \\ / _ \\ | | | \\ \\ / / _ \\ '__|\n"   # noqa: E501
    "| |_| | (_| | | | | | |  __/ | |_| |\\ V /  __/ |   \n"       # noqa: E501
    " \\____|\\__,_|_| |_| |_|\\___|  \\___/  \\_/ \\___|_|   \n"  # noqa: E501
)


MAX_ENEMIES = 3

# grid type
FREE_GRID = 0
DIAMOND_GRID = 2
LADDER_GRID = 3

# Walkable
NON_WALKABLE_GRID = 0

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
