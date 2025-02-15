from characters.character import CharacterAnimationManager


class MainAnimationManager(CharacterAnimationManager):
    """ This class represents the main character to be used the game. """
    def init(self, width, height, maze_data,
             is_controlled_by_computer, x=0, y=0, **kwargs):
        super().__init__(
            width, height, maze_data, is_controlled_by_computer,
            x, y, **kwargs
        )

    def check_enemy_collision(self, enemy_agents) -> bool:
        """ Check for collisions between the main character and any enemies in
        the game."""
        for enemy in enemy_agents:
            if self.hitbox_rect.colliderect(enemy.character.hitbox_rect):
                return True

        return False

    def draw_animation(self, screen, world_tile_data, direction=None,
                       asset_groups=None, game_over=0,
                       enemy_computers=[]) -> int:
        """ As this is the main character in the game, we will need to handle
        the collision logic for the diamond.

        Also, based on the action of this character the game will end."""

        remove_diamond_pos = None
        update_frame = False

        if enemy_computers and self.check_enemy_collision(enemy_computers):
            game_over = 1

        # If game_over flag is set, then we will halt character movement
        if game_over != 0:
            self._animation_actions[self._requested_animation].draw_animation(
                screen, self.rect, update_frame, self.look_left
            )
            return game_over, remove_diamond_pos

        # Do diamond collision logic based on whether the maze is filled or not
        if self.in_filled_maze:
            remove_diamond_pos = (
                self.diamond_collision_in_filled_maze(asset_groups)
            )
        else:
            self.diamond_collision_in_non_filled_maze(asset_groups)

        # Call the parent draw function to handle the rest of the animation
        # logic.
        super().draw_animation(screen, world_tile_data, direction)

        return game_over, remove_diamond_pos
