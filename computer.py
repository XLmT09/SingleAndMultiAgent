from characters import CharacterAnimationManager

class Computer:
    def __init__(self, character):
        self.character = character

    def move(self, screen, world_data, asset_groups, game_over):
        return self.character.draw_animation(screen, world_data, asset_groups, game_over, "LEFT")
