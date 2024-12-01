import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Text:
    """ This class represents the text objects that can be used to
    blit onto the maze game.

    Attributes:
        _font (Font): Font type and size for the text.

    Args:
        size (int): The font size for the text.
    """
    def __init__(self, size) -> None:
        self._font = pygame.font.SysFont(None, size)

    def draw(self, screen, text_string, x, y) -> None:
        """ This method will blit the text object on the screen.

        Args:
            screen (Surface): The screen to display the text.
            text_string (str): The text to be output.
            x (int): the top left x coord of the object.
            y (int): the top left y corrd of the object.
        """
        text = self._font.render(text_string, True, WHITE)
        # We create a surface to put the text on, we can use this surface to
        # tell the programme where to put the text.
        text_surface = pygame.Surface(text.get_size())
        text_surface.fill(BLACK)
        text_surface.blit(text, (0, 0))
        screen.blit(text_surface, (x, y))
