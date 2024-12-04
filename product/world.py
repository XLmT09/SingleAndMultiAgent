from constants import diamond_sprite_images, colour_vals, PASS, FAIL

import pygame
import random
import time
import inspect


TILE_SIZE = 50
WHITE = (255, 255, 255)


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
        image (pygame.image): The image we are currently displaying of the
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
        for sprite_image in diamond_sprite_images:
            self._diamond_sprite_list.append(pygame.image.load(sprite_image))

    def update_position(self, x, y) -> None:
        """ Update the positon of the diamond """
        self.rect.x = x * TILE_SIZE + 10
        self.rect.y = y * TILE_SIZE + 10

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
            _diamond_group (pygame.sprite.Group): This holds all the diamonds
                to be used in the game, and can be blit all at once with a
                single method.
            _ladder_img (pygame.image): Holds the image a ladder.

        Args:
            world_matrix (list of lists): The inital matrix to be used for the
            maze.
        """
        self._world_matrix = world_matrix
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
                    img = pygame.transform.scale(self._tile_list_images[0],
                                                 (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (img, img_rect)
                    self._collidable_tile_list.append(tile)
                # Check if this tile will contain a diamond
                if tile == 2:
                    diamond = Diamond(col_cnt * TILE_SIZE + 10,
                                      row_cnt * TILE_SIZE + 10)
                    self._diamond_group.add(diamond)
                # Check if this tile should have a ladder
                if tile == 3:
                    img = pygame.transform.scale(self._ladder_img,
                                                 (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (img, img_rect)
                    self._non_collidable_tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(self._tile_list_images[3],
                                                 (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (img, img_rect)
                    self._collidable_tile_list.append(tile)
                col_cnt += 1
            row_cnt += 1

    def _find_walkable_areas_in_the_maze(self) -> None:
        """ This functions uses the _world_matrix to create a new matrix which
        fills all walkable tiles with 1 and climable paths with 3.

        A tile is considered walkable if it is empty and there is a tile
        platform directly above and below it.

        A tile is considered climable is there is a ladder i.e. a 3 in the#
        world matrix.
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

    def _randomly_update_diamond_location(self) -> None:
        """ This function randomly updates the location of the diamond,
        in a valid spot on the maze.
        """

        # First find all valid locations to place the diamond.
        # Valid location will have a one in the walkable matrix, so
        # we will store all instances of these.
        location_of_one_indices = []
        for i in range(len(self._walkable_maze_matrix)):
            for j in range(len(self._walkable_maze_matrix[0])):
                if self._walkable_maze_matrix[i][j] == 1:
                    location_of_one_indices.append((i, j))
                # During this loop we can also clear the position of the
                # current diamond location, on the original maze.
                if self._world_matrix[i][j] == 2:
                    self._world_matrix[i][j] = 0
                    self._walkable_maze_matrix[i][j] = 0

        # Next we randomly choose a index to place our diamond
        new_diamond_row, new_diamond_col = random.choice(
                                            location_of_one_indices)

        # Now we can update the position of the diamond rect and maze index
        self._world_matrix[new_diamond_row][new_diamond_col] = 2
        # We should also update the walkable maze so that the player knows
        # where the new diamond is
        self._walkable_maze_matrix[new_diamond_row][new_diamond_col] = 2
        for diamond in self._diamond_group:
            # we pass new_diamond_index[1] as y and vise versa, as went iterate
            # through the column using the second index
            diamond.update_position(new_diamond_col, new_diamond_row)

    def draw_grid(self, screen, screen_height, screen_width) -> None:
        """ This functions draws out the grids on the game, to help visualize
        on what grid every asset is, or which grid the player is currently on.
        """
        for line in range(29):
            # Draw the vertical lines
            pygame.draw.line(screen, WHITE, (line * TILE_SIZE, 0),
                             (line * TILE_SIZE, screen_height))
            # Draw the horizontal lines
            pygame.draw.line(screen, WHITE, (0, line * TILE_SIZE),
                             (screen_width, line * TILE_SIZE))

    def update_diamond_position(self):
        """ This function will find the walkable paths and then update the
        location of diamond onto the walkable path.
        """
        self._find_walkable_areas_in_the_maze()
        self._randomly_update_diamond_location()

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
            return FAIL

        # Create a transparent cube to use to highlight the grid
        grid_higlight_size = (TILE_SIZE, TILE_SIZE)

        highlight_visited_surface = pygame.Surface(grid_higlight_size,
                                                   pygame.SRCALPHA)
        highlight_visited_surface.fill(colour_vals["red_transparent"])

        highlight_path_surface = pygame.Surface(grid_higlight_size,
                                                pygame.SRCALPHA)
        highlight_path_surface.fill(colour_vals["blue_transparent"])

        # Iteratate through every position the algortihm visited and
        # highlight thise grids/
        for top_right_grid_position in visited_list:
            time.sleep(0.04)
            screen.blit(highlight_visited_surface,
                        (top_right_grid_position[1] * TILE_SIZE,
                         top_right_grid_position[0] * TILE_SIZE))

            # We need to update the screen on every iteration to see the
            # visually see the sequential order of the grids visited.
            pygame.display.update()

        # Now that we have highlighted the visited grids, we will end it off
        # by highlighting the final path found.
        for top_right_grid_position in path_to_goal:
            time.sleep(0.04)
            screen.blit(highlight_path_surface,
                        (top_right_grid_position[1] * TILE_SIZE,
                         top_right_grid_position[0] * TILE_SIZE))

            # Update the screen on every blit iteration
            pygame.display.update()

        time.sleep(3)
        return PASS

    def print_walkable_maze_matrix(self) -> None:
        """ Print walkable maze matrix in a nice format """
        print(*self._walkable_maze_matrix, sep="\n")

    def get_walkable_maze_matrix(self) -> list:
        return self._walkable_maze_matrix

    def get_collidable_tile_list(self) -> list:
        return self._collidable_tile_list

    def get_diamond_group(self) -> list:
        return self._diamond_group
