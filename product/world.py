import constants as C
import pygame
import random
import time
import inspect


class Diamond(pygame.sprite.Sprite):
    """ This class stores the diamonds and its meta data, which will be used to
    print onto the maze and can handle collisons with players thanks to its
    inheritence of the pygame sprite class.

    Attributes:
        DIAMOND_ANIMATION_SPEED (float): The speed to transition to the next
        sprite image.
        _diamond_sprite_list (list): List which stores the sprite images.
        _current_sprite (int): The index we are currently on in
            _diamond_sprite_list.
        image (Surface): The image we are currently displaying of the
            diamond.
        rect (Rect): The rectangle which represents the hitbox of the diamond,
            and is also used to know exaclty where to put the diamond in the
            maze.

    Args:
        x (int): This represents the top left x coord of the rect object.
        y (int): This represents the top left y coord of the rect object.
    """
    DIAMOND_ANIMATION_SPEED = 0.2

    def __init__(self, x, y) -> None:
        super().__init__()
        self._diamond_sprite_list = []
        self._current_sprite = 0
        # Load the images into list now to fill the remaining member variables
        self._load_diamond_images()
        self.image = self._diamond_sprite_list[self._current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _load_diamond_images(self) -> None:
        """ Load and store images of the diamond sprites """
        for sprite_image in C.diamond_sprite_images:
            self._diamond_sprite_list.append(pygame.image.load(sprite_image))

    def update_position(self, x, y) -> None:
        """ Update the positon of the diamond """
        self.rect.x = x * C.TILE_SIZE + 10
        self.rect.y = y * C.TILE_SIZE + 10

    def update(self) -> None:
        """ This function moves to the next sprite image of the diamond
        every DIAMOND_ANIMATION_SPEED.
        """
        self._current_sprite += self.DIAMOND_ANIMATION_SPEED
        if int(self._current_sprite) >= len(self._diamond_sprite_list):
            self._current_sprite = 0

        self.image = self._diamond_sprite_list[int(self._current_sprite)]


class World:
    def __init__(self, world_matrix) -> None:
        """ This class takes in a matrix and converts into a maze, by using
        the values in the matrix to identify where each asset should be placed.
        Once conversion is complete the class will be able to blit the maze
        onto pygame.

        Attributes:
            _world_matrix (list of lists): The matrix which represnts the
                maze in numbers.
            _collidable_tile_list (list): The list which stores the tuple's of
                a tile image and its corrosponding position to be put in the
                maze that are collidable.
            _non_collidable_tile_list (list): The list which stores the
                tuple's of a tile image and its corrosponding position to be
                put in the maze that are non-collidable.
            _tile_list_images (list): The list which stores all the tile
                images that can be used in the maze.
            _diamond_group (Group): This holds all the diamonds
                to be used in the game, and can be blit all at once with a
                single method.
            _ladder_img (Surface): Holds the image a ladder.

        Args:
            world_matrix (list of lists): The inital matrix to be used for the
            maze.
        """
        self._world_matrix = world_matrix
        self._maze_size = self.get_maze_size()
        self._collidable_tile_list = []
        self._non_collidable_tile_list = []
        self._tile_list_images = []
        self._diamond_group = pygame.sprite.Group()
        self._ladder_img = pygame.image.load(
            "assets/images/blocks/ladder.png")
        self._walkable_maze_matrix = (
            [[0 for _ in range(len(self._world_matrix[0]))]
                for _ in range(len(self._world_matrix))]
        )

        # Gather available images and there positions in the maze
        self._load_asset_and_tile_images()
        self._genrate_world_tiles_and_assets()
        # Also initalize the walkable maze now, so that the computer can use it
        self._find_walkable_areas_in_the_maze()
        self.was_highlight_ran = False
        self.diamond_regeneration_positions = {"small": [(1, 13), (5, 11),
                                                         (1, 6), (5, 2)],
                                               "medium": [(3, 7), (13, 18),
                                                          (7, 8), (1, 18)],
                                               "large": [(4, 2), (13, 17),
                                                         (11, 21), (1, 15)]}

    def _load_asset_and_tile_images(self) -> None:
        """ Load and store all images/sprites of sprites/assets to be used in
        the game. """
        for i in range(1, 5):
            image = pygame.image.load(
                f"assets/images/blocks/tile{i}.png").convert_alpha()
            self._tile_list_images.append(image)

    def _genrate_world_tiles_and_assets(self) -> None:
        """ Use's the world matrix given to the class, to collect data of
        every tile/asset in the map with it's corrosponding location. This is
        used to identify where to blit tiles/assets in the game.
        """

        row_cnt = 0
        # Loop through the matrix and store any asset/tile information found
        for row in self._world_matrix:
            col_cnt = 0
            for tile in row:
                # Check if the tile is a noraml platform block
                if tile == 1:
                    img = pygame.transform.scale(
                        self._tile_list_images[0],
                        (C.TILE_SIZE, C.TILE_SIZE)
                    )
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * C.TILE_SIZE
                    img_rect.y = row_cnt * C.TILE_SIZE
                    tile = (img, img_rect)
                    self._collidable_tile_list.append(tile)
                # Check if this tile will contain a diamond
                if tile == 2:
                    diamond = Diamond(col_cnt * C.TILE_SIZE + 10,
                                      row_cnt * C.TILE_SIZE + 10)
                    self._diamond_group.add(diamond)
                # Check if this tile should have a ladder
                if tile == 3:
                    img = pygame.transform.scale(
                        self._ladder_img,
                        (C.TILE_SIZE, C.TILE_SIZE)
                    )
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * C.TILE_SIZE
                    img_rect.y = row_cnt * C.TILE_SIZE
                    tile = (img, img_rect)
                    self._non_collidable_tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(
                        self._tile_list_images[3],
                        (C.TILE_SIZE, C.TILE_SIZE)
                    )
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * C.TILE_SIZE
                    img_rect.y = row_cnt * C.TILE_SIZE
                    tile = (img, img_rect)
                    self._collidable_tile_list.append(tile)
                col_cnt += 1
            row_cnt += 1

    def _find_walkable_areas_in_the_maze(self) -> None:
        """ This functions uses the _world_matrix to create a new matrix which
        fills all walkable tiles with 1 and climable paths with 3.

        A tile is considered walkable if it is empty and there is a tile
        platform directly above and below it.

        A tile is considered climbable if there there is a ladder i.e. a 3 in
        the world matrix.
        """
        walkable_tiles = {1, 4}
        for i in range(len(self._world_matrix)):
            for j in range(len(self._world_matrix[0])):
                # Check if the tile is empty and that there is a tile above
                # and below it
                if (self._world_matrix[i][j] == 2):
                    self._walkable_maze_matrix[i][j] = 2
                # Check if the tile contains a ladder
                elif (self._world_matrix[i][j] == 3):
                    self._walkable_maze_matrix[i][j] = 3
                # Statements with continue in the body check if the cell is
                # walkable, if its not walkable then leave as 0 and go to the
                # next loop.
                elif (not (self._world_matrix[i][j] == 0)):
                    continue
                elif not ((i - 1 >= 0) and (j - 1 >= 0) and
                          (i + 1 < len(self._world_matrix)) and
                          (j + 1 < len(self._world_matrix[0]))):
                    continue
                elif not ((self._world_matrix[i-1][j] in walkable_tiles) and
                          (self._world_matrix[i + 1][j] in walkable_tiles)):
                    continue
                elif (self._world_matrix[i+1][j] == 1):
                    # 1 indicates a normal block
                    self._walkable_maze_matrix[i][j] = 1
                elif (self._world_matrix[i+1][j] == 4):
                    # 4 indicates a slow block
                    self._walkable_maze_matrix[i][j] = 4

    def get_walkable_locations(self, clear_diamond_pos=True) -> list:
        """ Loop through the walkable matrix and return the list of coords
        that are walkable.

        Args:
            clear_diamond_pos (bool): When looping the matix we will clear
                the diamond location when spotted.
        """
        # Valid walkable locations will have a one in the matrix
        location_of_ones_in_matrix = []

        # First find all valid locations to place the diamond.
        for i in range(len(self._walkable_maze_matrix)):
            for j in range(len(self._walkable_maze_matrix[0])):
                if self._walkable_maze_matrix[i][j] == 1:
                    location_of_ones_in_matrix.append((i, j))
                # During this loop we can also clear the position of the
                # current diamond location, on the original maze.
                if self._world_matrix[i][j] == 2 and clear_diamond_pos:
                    self._world_matrix[i][j] = 0
                    self._walkable_maze_matrix[i][j] = 0

        return location_of_ones_in_matrix

    def update_diamond_position(self, are_locations_defined=False):
        """ This function will find update the coords of a diamond by removing
        the current diamond and placing a new diamond at a different location.

        Args:
            are_locations_defined (list of tuples): A flag which when set will
                place diamonds at specific locations and not randomly.
        """
        # Before starting we should update the walkable areas in the maze,
        # as the diamond has moved positions.
        self._find_walkable_areas_in_the_maze()

        # We will get the list of walkable verticies and also clear the current
        # diamond position.
        walkable_vertices = self.get_walkable_locations(clear_diamond_pos=True)

        new_diamond_row, new_diamond_col = None, None
        diamond_locations_stack = (
            self.diamond_regeneration_positions[self._maze_size]
        )

        # If we are you using defined positions and the stack is empty, then
        # we have found all the diamonds and can stop execution.
        if are_locations_defined and not diamond_locations_stack:
            return 2
        elif are_locations_defined:
            new_diamond_row, new_diamond_col = diamond_locations_stack.pop()
        else:
            # we randomly choose a random walkable vertex to place our diamond,
            # if locations specified flag is off.
            new_diamond_row, new_diamond_col = random.choice(
                                                walkable_vertices)

        # Now we can update the position of the diamond rect and maze index
        self._world_matrix[new_diamond_row][new_diamond_col] = (
            C.DIAMOND_GRID
        )
        # We should also update the walkable maze so that the player knows
        # where the new diamond is
        self._walkable_maze_matrix[new_diamond_row][new_diamond_col] = (
            C.DIAMOND_GRID
        )
        for diamond in self._diamond_group:
            # we pass new_diamond_index[1] as y and vise versa, as went iterate
            # through the column using the second index
            diamond.update_position(new_diamond_col, new_diamond_row)

        return C.PASS

    def draw_grid(self, screen, screen_height, screen_width) -> None:
        """ This functions draws out the grids on the game, to help visualize
        on what grid every asset is, or which grid the player is currently on.
        """
        for line in range(29):
            # Draw the vertical lines
            pygame.draw.line(screen, C.WHITE, (line * C.TILE_SIZE, 0),
                             (line * C.TILE_SIZE, screen_height))
            # Draw the horizontal lines
            pygame.draw.line(screen, C.WHITE, (0, line * C.TILE_SIZE),
                             (screen_width, line * C.TILE_SIZE))

    def load_world(self, screen) -> None:
        """ This function blits the maze onto the screen.

        Args:
            screen (pygame.display): The screen we want to blit the maze onto.
        """
        for tile in self._collidable_tile_list:
            screen.blit(tile[0], tile[1])
        for tile in self._non_collidable_tile_list:
            screen.blit(tile[0], tile[1])
        self._diamond_group.draw(screen)
        self._diamond_group.update()

    def highlight_grids_visited_by_algo(self, screen, visited_list,
                                        path_to_goal) -> int:
        """ This function will highlight the grids the algorithm currently in
        use had visited.

        Args:
            screen (pygame.display): The screen we want to blit the maze onto.
            visited_list (list of tuples): The list of coords the algorithm
                had visited.
            path_to_goal (list of tuples): The list of coords from player start
                position to the goal state.
        """

        if visited_list is None or path_to_goal is None:
            print(f"{inspect.currentframe().f_code.co_name}: Skipping "
                  "execution because the visited_list and/or path_to_goal have"
                  " not yet been generated.")
            return C.FAIL

        # Create a transparent cube to use to highlight the grid
        grid_higlight_size = (C.TILE_SIZE, C.TILE_SIZE)

        highlight_visited_surface = pygame.Surface(grid_higlight_size,
                                                   pygame.SRCALPHA)
        highlight_visited_surface.fill(C.colour_vals["red_transparent"])

        highlight_path_surface = pygame.Surface(grid_higlight_size,
                                                pygame.SRCALPHA)
        highlight_path_surface.fill(C.colour_vals["blue_transparent"])

        # Iteratate through every position the algortihm visited and
        # highlight thise grids/
        for top_right_grid_position in visited_list:
            time.sleep(0.04)
            screen.blit(highlight_visited_surface,
                        (top_right_grid_position[1] * C.TILE_SIZE,
                         top_right_grid_position[0] * C.TILE_SIZE))

            # We need to update the screen on every iteration to see the
            # visually see the sequential order of the grids visited.
            pygame.display.update()

        # Now that we have highlighted the visited grids, we will end it off
        # by highlighting the final path found.
        for top_right_grid_position in path_to_goal:
            time.sleep(0.04)
            screen.blit(highlight_path_surface,
                        (top_right_grid_position[1] * C.TILE_SIZE,
                         top_right_grid_position[0] * C.TILE_SIZE))

            # Update the screen on every blit iteration
            pygame.display.update()

        time.sleep(3)
        return C.PASS

    def print_walkable_maze_matrix(self) -> None:
        """ Print walkable maze matrix in a nice format """
        print(*self._walkable_maze_matrix, sep="\n")

    def get_walkable_maze_matrix(self) -> list:
        return self._walkable_maze_matrix

    def get_collidable_tile_list(self) -> list:
        return self._collidable_tile_list

    def get_diamond_group(self) -> list:
        return self._diamond_group

    def get_maze_size(self) -> str:
        """ This function deterimes the size of a maze based on its matrix
         data"""
        if len(self._world_matrix) <= 7:
            return "small"
        elif (len(self._world_matrix) <= 15 and
              len(self._world_matrix[0]) <= 20):
            return "medium"
        else:
            return "large"
