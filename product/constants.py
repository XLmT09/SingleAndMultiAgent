PLAYER_IDLE_FILE_PATH = (
    "product/assets/images/characters/Dude_Monster/Dude_Monster_Idle_4.png"
)

PLAYER_JUMP_FILE_PATH = (
    "product/assets/images/characters/Dude_Monster/Dude_Monster_Jump_8.png"
)

PLAYER_WALK_FILE_PATH = (
    "product/assets/images/characters/Dude_Monster/Dude_Monster_Walk_6.png"
)

PLAYER_CLIMB_FILE_PATH = (
    "product/assets/images/characters/Dude_Monster/Dude_Monster_Climb_4.png"
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
        f"product/assets/images/pixel-art-diamond/diamond{i}.png")
