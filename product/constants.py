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

# grid type
FREE_GRID = 0
DIAMOND_GRID = 2
LADDER_GRID = 4

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

PLAYER_IDLE_FILE_PATH = (
    "assets/images/characters/Dude_Monster/Dude_Monster_Idle_4.png"
)

PLAYER_JUMP_FILE_PATH = (
    "assets/images/characters/Dude_Monster/Dude_Monster_Jump_8.png"
)

PLAYER_WALK_FILE_PATH = (
    "assets/images/characters/Dude_Monster/Dude_Monster_Walk_6.png"
)

PLAYER_CLIMB_FILE_PATH = (
    "assets/images/characters/Dude_Monster/Dude_Monster_Climb_4.png"
)

player_sprite_file_paths = {
    "idle": PLAYER_IDLE_FILE_PATH,
    "jump": PLAYER_JUMP_FILE_PATH,
    "walk": PLAYER_WALK_FILE_PATH,
    "climb": PLAYER_CLIMB_FILE_PATH
}

# unlike the player, the diamond sprite images are in seperate files and
# not the same on so we need to iterate through the paths and store in
# a list
NUM_DIAMOND_SPRITE_IMAGES = 8
diamond_sprite_images = []

for i in range(1, NUM_DIAMOND_SPRITE_IMAGES + 1):
    diamond_sprite_images.append(
        f"assets/images/pixel-art-diamond/diamond{i}.png")
