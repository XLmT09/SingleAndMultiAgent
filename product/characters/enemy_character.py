from characters.character import CharacterAnimationManager


class EnemyAnimationManager(CharacterAnimationManager):
    """ This class represents the enemy characters that will be in
    the game. """

    def init(self, width, height, maze_data,
             is_controlled_by_computer, x=0, y=0, **kwargs):
        super().__init__(
            width, height, maze_data, is_controlled_by_computer,
            x, y, **kwargs
        )
