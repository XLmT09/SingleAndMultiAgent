import pygame
import constants as C


class Player:
    """
    This class will hold the data/attributes of different player animation
    cycles.

    For example:
    A player can be in various states such as: move, walk, climb and idle.

    So we will have 4 different classes for a player to represent each state.
    Then we will use the CharacterAnimationManager class to determine which of
    these states we should use at any given moment for the player.

    Attributes:
        _sprite_sheet (Surface): This contains all the sprite images of the
            player.
        width (int): The width (in pixels) of the player.
        height (int): The height (in pixels) of the player.
        _steps (int): This number represents the number of player images in the
            sprite sheet.
        _animation_list (list of Surface): A list of every image of the player
            looking rightwards.
        _animation_list_left (list of Surface): A list of every image of the
            player looking leftwards.
        _frame_counter (int): This number represents the sprite image we want
            to output.

    Args:
        sprite_sheet (str): Path to the sprite sheet animation that needs
            to be unwrapped.
        width (int): The pixel width of each frame in the sprite height.
        height (int): The pixel height of each frame in the sprite sheet.
        animation_steps (int): The number of frame in the sprite sheet to
            be unwrapped.
    """
    def __init__(self, sprite_sheet, width, height, animation_steps) -> None:
        self._sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.width = width
        self.height = height
        self._steps = animation_steps
        _scale = 1.7
        # List of animation images to cycle through
        self._animation_list = (
         [self.load_image(step, _scale, False) for step in range(self._steps)]
        )
        self._animation_list_left = (
         [self.load_image(step, _scale, True) for step in range(self._steps)]
        )
        self._frame_counter = 0

    def load_image(self, frame, scale, look_left) -> pygame.Surface:
        """ This function will extract an particular images from the sprite
        sheet, and then put it on its own independent Surface object.

        Args:
            frame (int): The number indicates the sprite image we want to
                extract from the sprite sheet.
            scale (int): This number tells us how much we want to enlarge
                the image.
            look_left (bool): This flag indicates if we should flip the image
                to look leftwards.

        Returns:
            Surface: A particular image in a sprite sheet after formatting.
        """

        # Create an empty surface with the same raw width and height pixels of
        # the player in the sprite sheet.
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        # We will now get a particular image in the sprite sheet.
        #
        # The value of a sprite sheet length is:
        # sheet width = self.width * number player images in the sprite sheet.
        #
        # That means we can get a certain frame from the sprite sheet by
        # multiplying the player width by the position of a certain image in
        # the sheet. For example, if we want the second sprite image in the
        # sprite sheet we would do 1 * self._width.
        #
        # Once we are at correct position on the sprite sheet we put it on the
        # image surface object.
        image.blit(self._sprite_sheet, (0, 0),
                   ((frame * self.width), 0, self.width, self.height))
        # Enlarge the image to fit with the game environment
        image = pygame.transform.scale(image,
                                       (self.width * scale,
                                        self.height * scale))

        # Flip the image if we want it to look left
        if look_left:
            image = pygame.transform.flip(image, True, False)

        # This will make the background transparent
        image.set_colorkey(C.BLACK)

        return image

    def draw_animation(self, screen, rect, update_frame, look_left) -> None:
        """ This function updates the player frame to the next sprite
        image.

        Args:
            screen (Surface): The surface we will draw the player.
            rect (Rect): The rectangle of the player, used to understand where
                the updated animation should be drawn.
            update_frame (bool): Flag which tells us we should update to the
                next sprite image or not.
            look_left (bool): Flag to tell us if we should use the player
                looking right or left set of images.
        """

        if update_frame:
            # update to the next sprite image, by incrementing the frame number
            self._frame_counter = (self._frame_counter + 1) % self._steps

        # Use the player look left images, if the flag is set otherwise we use
        # the player look right images
        if look_left:
            screen.blit(self._animation_list_left[self._frame_counter], rect)
            return

        screen.blit(self._animation_list[self._frame_counter], rect)


class CharacterAnimationManager:
    """ This class will handle the movement and collision logic
    of a character/player.
    It will also decide which player state/animation to use at any
    given moment.

    Attributes:
        width (int): The width (in pixels) of the player.
        height (int): The height (in pixels) of the player.
        rect (Rect): The rectangle of the player, not using private notation
            here as external pygame files need access to this.
        _pos_x (int): The x position of the player.
        _pos_y (int): The y position of the player.
        rect (Rect): The rectangle surrounding the character, we use this
            rectangle for the movement.
        hitbox_width (int): The width of the character hitbox, should be equal
            to or smaller than the normal width.
        hitbox_height (int): The height of the character hitbox, should be
            equal to or smaller than the normal height.
        hitbox_rect (Rect): We will use this rect attached to the player to
            detect collisions.
        _animation_actions (dict of Player): This will hold the different
            player animation states.
        _requested_animation (str): The animation sate we want the player
            to be in.
        _last_update (int): Timestamp of when we last updated the animation.
        _vel_y (int): The speed the player will fall, if not on a platform.
        look_left (bool): A flag to check if the player is looking left or not.
        _jumped (bool): A flag to check if the player is currently not on a
            platform.
        _is_controlled_by_computer (bool): A flag to state if we want the
            computer to move the player or the user.
        grid_x (int): Current x grid location of the player in the maze.
        grid_y (int): Current y grid location of the player in the maze.
        _maze_data (list of int lists): This is the maze matrix character is
            currently within.
        _is_diamond_found (bool): A flag to check is the diamond was found or
            not.
        _score (int): The number of diamonds the character has collected.
    """
    def __init__(self, width, height, maze_data,
                 is_controlled_by_computer, x=0, y=0, **kwargs):
        # ================= PLAYER RECT =====================
        self.width = width
        self.height = height
        scale = 1.8
        self.rect = pygame.Rect(x, y, width * scale, height * scale)
        self._pos_x, self._pos_y = x, y

        # We have already defined the position when initializing the rect, the
        # reason we are using center here is because its the only way pygame
        # will allow movements of float values.
        self.rect.center = (self._pos_x, self._pos_y)

        # ================= PLAYER HITBOX RECT ===============
        self.hitbox_width = width
        # We offset values as the hitbox rect has shrunk and will
        # therefore have to re align with the player.
        _hitbox_height_offset = 14
        _hitbox_posx_offset, _hitbox_posy_offset = -1, 4
        # We need to shrink the height of the hitbox by adding an offset
        # because there is too much empty space in the original rect
        # used for movement.
        self.hitbox_height = height + _hitbox_height_offset
        self.hitbox_rect = pygame.Rect(x, y, self.hitbox_width,
                                       self.hitbox_height)

        self.hitbox_rect.center = (self._pos_x - _hitbox_posx_offset,
                                   self._pos_y + _hitbox_posy_offset)

        # ================= PLAYER ANIMATION/MOVEMENT ===========
        self._animation_actions = {}
        self._requested_animation = "idle"
        self._last_update = pygame.time.get_ticks()
        self._vel_y, self._dx, self._dy = 0, 0, 0
        self.look_left = False
        self._jumped = False
        self._is_controlled_by_computer = is_controlled_by_computer
        if self.look_left:
            self.grid_x = (self.hitbox_rect.x + self.width) // 50
        else:
            self.grid_x = self.hitbox_rect.x // 50
        self.grid_y = (self.hitbox_rect.y) // 50

        # ================= PLAYER ENV ATTRIBUTES ===============
        self._maze_data = maze_data
        self._is_diamond_found = False
        self._score = 0
        self.diamond_removal_pos = None
        self.in_filled_maze = None
        if "in_filled_maze" in kwargs:
            self.in_filled_maze = kwargs["in_filled_maze"]

    def set_char_animation(self, animation_description, sprite_sheet,
                           animation_steps) -> None:
        """ This function appends the player animation states to the
        _animations_actions dict.

        Attributes:
            animation_description (str): Describes the animation type, for
                example climb and idle.
            sprite_sheet (str): Path to the sprite sheet animation that needs
                to be unwrapped.
            animation_steps (int): The number of frames the sprite sheet has.
        """
        self._animation_actions[animation_description] = (
            Player(sprite_sheet, self.width, self.height, animation_steps)
        )

    def draw_outline(self, screen):
        """ This function draws the outline of the player rect. """
        border_width = 2
        pygame.draw.rect(screen, C.WHITE, self.hitbox_rect, border_width)

    def human_player_movement(self) -> None:
        """ This function handles player movement by the user, by registering
        keyboard inputs."""

        # Get the key that way pressed
        key = pygame.key.get_pressed()

        # Update the requested_animation based on the key that was pressed and
        # then update update how much we should increase the x and y pos of
        # the player.
        if key[pygame.K_RIGHT]:
            self._requested_animation = "walk"
            self.look_left = False
            self._dx += 1
        if key[pygame.K_LEFT]:
            self._requested_animation = "walk"
            self.look_left = True
            self._dx -= 1
        # If the user uses the up key and is on a grid which has a ladder
        # we will climb.
        if key[pygame.K_UP] and self._maze_data[self.grid_y][self.grid_x] == 3:
            self._requested_animation = "climb"
            self._dy -= 2
        if key[pygame.K_SPACE] and not self._jumped:
            self._requested_animation = "jump"
            self._vel_y = -15
            self._jumped = True
        if not key[pygame.K_SPACE]:
            self._jumped = False

    def computer_player_movement(self, direction) -> None:
        """ This function handles player movement based on instructions by
        the computer. The computer has multiple states it can be BFS,DFS,etc.

        Args:
            direction (str): The direction the computer commands the player to
                move.
        """

        if direction == "RIGHT":
            self._requested_animation = "walk"
            self.look_left = False
            # If the player is on a slow block then decrease the movement
            if self._on_a_slow_block():
                self._dx += 0.5
            else:
                self._dx += 1
        elif direction == "LEFT":
            self._requested_animation = "walk"
            self.look_left = True
            # If the player is on a slow block then decrease the movement
            if self._on_a_slow_block():
                self._dx -= 0.5
            else:
                self._dx -= 1
        elif direction == "UP":
            self._requested_animation = "climb"
            self._dy -= 2
        elif direction == "UP RIGHT":
            self._requested_animation = "climb"
            self._dy -= 2
            self._dx += 1
        elif direction == "UP LEFT":
            self._requested_animation = "climb"
            self._dy -= 2
            self._dx -= 1
        # elif direction == "DOWN":
        #     self._requested_animation = "climb"
        #     self._dy += 1
        else:
            self._dx, self._dy = 0, 0
            self._requested_animation = "idle"

    def diamond_collision_in_non_filled_maze(self, world_assets):
        """ Check for diamond collision in a non filled maze.

        If there is a collision then update the score and set found to True so
        that we can regenerate it to a new location. """
        if pygame.sprite.spritecollide(
            self, world_assets, False,
            pygame.sprite.collide_rect_ratio(0.7)
        ):
            self._is_diamond_found = True
            self._score += 1

    def diamond_collision_in_filled_maze(self, world_assets):
        """ Check for diamond collision in a filled maze. """
        diamond_removal_coord = []

        if diamond := pygame.sprite.spritecollideany(
                        self,
                        world_assets,
                        pygame.sprite.collide_rect_ratio(0.7)
                    ):
            world_assets.remove(diamond)
            self._is_diamond_found = True
            self._score += 1
            diamond_removal_coord = [diamond.grid_x, diamond.grid_y]

        return diamond_removal_coord

    def draw_animation(self, screen, world_tile_data, direction=None) -> int:
        """ This function handles the logic of drawing the player onto the
        screen. It also updates the movement speed and detects collisions.

        Args:
            screen (Surface): The surface we blit the player onto.
            world_tile_data (list of Rect): List of rects the player can
                collide into on the current maze.
            world_assets (Group): Get list of assets in the maze, currently
                the only assets are diamonds.
            game_over (int): flag to check if we should halt player movement.
            direction (str): If the computer is taking control then we need
                this arg to check the direction the computer wants the player
                to go.

        Returns:
            game_over (int): If set then it will inform main.py to stop
                running.
        """

        # By default we will set player animation to idle
        self._requested_animation = "idle"
        update_frame = False
        current_time = pygame.time.get_ticks()
        self._dx = 0
        self._dy = 0

        # Update the animation if the current one is past cool down limit.
        # Animation cool down is used to make sure transition between the
        # different sprite images are smooth.
        if current_time - self._last_update >= C.ANIMATION_COOLDOWN:
            self._last_update = current_time
            update_frame = True

        # Stick with jump animation while still in air
        if self._vel_y != 0:
            self._requested_animation = "jump"

        # Decide if the user or computer should handle the movement
        if self._is_controlled_by_computer:
            self.computer_player_movement(direction)
        else:
            self.human_player_movement()

        # Handle velocity movement while in air
        self._vel_y += 1
        if self._vel_y > 10:
            self._vel_y = 10
        if self._requested_animation != "climb":
            self._dy += self._vel_y

        # Check for maze collisions by looping through the collidable tiles in
        # the current maze.
        for tile in world_tile_data:
            # Check for collision in x direction
            if tile[1].colliderect(self.hitbox_rect.x + self._dx,
                                   self.hitbox_rect.y, self.hitbox_width,
                                   self.hitbox_height):
                self._dx = 0
            # Check for y direction collisions
            if tile[1].colliderect(self.hitbox_rect.x,
                                   self.hitbox_rect.y + self._dy,
                                   self.hitbox_width, self.hitbox_height):
                # Check if below the ground
                if self._vel_y < 0 or self._requested_animation == "climb":
                    self._dy = tile[1].bottom - self.hitbox_rect.top
                    self._vel_y = 0
                # Check if above the ground
                elif self._vel_y >= 0:
                    self._dy = tile[1].top - self.hitbox_rect.bottom
                    self._vel_y = 0

        # Update the character x and y positions using the delta values
        self._pos_x += self._dx
        self._pos_y += self._dy

        # Update the center values, therefore we can use decimal movement.
        # Directly updating the center values, does not
        # support decimal movement.
        self.rect.center = (self._pos_x, self._pos_y)
        self.hitbox_rect.center = (self._pos_x - 1, self._pos_y + 4)

        # When an the player is facing left we still want to the right position
        # of the rect so we add the width. This is because the left side if
        # the rect will be outside the grid when moving left.
        if self.look_left:
            self.grid_x = (self.hitbox_rect.x + self.width) // C.TILE_SIZE
        else:
            self.grid_x = self.hitbox_rect.x // C.TILE_SIZE
        self.grid_y = (self.hitbox_rect.y) // C.TILE_SIZE

        # Now draw the animation using the Player class draw_animation
        # function, as thats where the frames of the different animations
        # are stored.
        self._animation_actions[self._requested_animation].draw_animation(
            screen, self.rect, update_frame, self.look_left
        )

    def _on_a_slow_block(self) -> bool:
        """ Check the player is moving over a slow block """
        return self._maze_data[self.grid_y + 1][self.grid_x] == (
            C.LADDER_GRID
        )

    def get_is_diamond_found(self) -> bool:
        return self._is_diamond_found

    def set_is_diamond_found_to_false(self) -> None:
        self._is_diamond_found = False

    def get_player_score(self) -> int:
        return self._score

    def get_player_grid_coordinates(self) -> int:
        return (self.grid_y, self.grid_x)


def get_character_types():
    from characters.enemy_character import (
        EnemyAnimationManager
    )
    from characters.main_character import (
        MainAnimationManager
    )

    return {
        "main": MainAnimationManager,
        "enemy": EnemyAnimationManager,
    }
