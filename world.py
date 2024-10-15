import pygame
import random

TILE_SIZE = 50
WHITE = (255, 255, 255)

class Diamond(pygame.sprite.Sprite):
    DIAMOND_ANIMATION_SPEED = 0.2
    NUM_DIAMOND_SPRITE_IMAGES = 8 

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
        for i in range(1, self.NUM_DIAMOND_SPRITE_IMAGES + 1):
            self._diamond_sprite_list.append(pygame.image.load(f"assets/images/pixel-art-diamond/diamond{i}.png"))

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
        """ This class takes in a matrix and converts into a maze, by using the values
        in the matrix to identify where each asset should be placed. Once conversion is 
        complete the class will be able to blit the maze onto pygame.

        Attributes:
            world_matrix (list of lists): The matrix which represnts the maze in numbers.
            collidable_tile_list (list): The list which stores the tuple's of a tile image 
                and its corrosponding position to be put in the maze that are collidable.
            collidable_tile_list (list): The list which stores the tuple's of a tile image 
                and its corrosponding position to be put in the maze that are non-collidable.
            tile_list_images (list): The list which stores all the tile images that can be 
                used in the maze.
            diamond_group (pygame.sprite.Group): This holds all the diamonds to be used in 
                the game, and can be blit all at once with a single method.
            ladder_img (pygame.image): Holds the image a ladder.
            
        Args:
            world_matrix (list of lists): The inital matrix to be used for the maze.
        """
        self._world_matrix = world_matrix
        self._collidable_tile_list = []
        self._non_collidable_tile_list = []
        self._tile_list_images = []
        self._diamond_group = pygame.sprite.Group()
        self._ladder_img = pygame.image.load("assets/images/blocks/ladder.png")
        self._walkable_maze_matrix = [[0 for _ in range(len(self._world_matrix[0]))] for _ in range(len(self._world_matrix))]

        # Gather available images and there positions in the maze
        self._load_asset_and_tile_images()
        self._genrate_world_tiles_and_assets()


    def _load_asset_and_tile_images(self) -> None:
        """ Load and store all images/sprites of sprites/assets to be used in the game. """
        for i in range(1, 5):
            image = pygame.image.load(f"assets/images/blocks/tile{i}.png").convert_alpha()
            self._tile_list_images.append(image)  
    

    def _genrate_world_tiles_and_assets(self) -> None:
        """ Use's the world matrix given to the class, to collect data of every tile/asset in the map
        with it's corrosponding location. This is used to identify where to blit tiles/assets
        in the game.
        """

        row_cnt = 0
        # Loop through the matrix and store any asset/tile information found
        for row in self._world_matrix:
            col_cnt = 0
            for tile in row:
                # Check if the tile is a noraml platform block
                if tile == 1:
                    img = pygame.transform.scale(self._tile_list_images[0], (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (img, img_rect)
                    self._collidable_tile_list.append(tile)
                # Check if this tile will contain a diamond
                if tile == 2:
                    diamond = Diamond(col_cnt * TILE_SIZE + 10, row_cnt * TILE_SIZE + 10)
                    self._diamond_group.add(diamond)
                # Check if this tile should have a ladder
                if tile == 3:
                    img = pygame.transform.scale(self._ladder_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (img, img_rect)
                    self._non_collidable_tile_list.append(tile)
                col_cnt += 1
            row_cnt += 1

    def draw_grid(self, screen, screen_height, screen_width) -> None:
        """ This functions draws out the grids on the game, to help visualize on 
        what grid every asset is, or which grid the player is currently on.
        """
        for line in range(29):
            # Draw the vertical lines
            pygame.draw.line(screen, WHITE, (line * TILE_SIZE, 0), (line * TILE_SIZE, screen_height))
            # Draw the horizontal lines
            pygame.draw.line(screen, WHITE, (0, line * TILE_SIZE), (screen_width, line * TILE_SIZE))
        
    def update_diamond_position(self):
        """ This function will find the walkable paths and then update the
        location of diamond onto the walkable path.
        """
        self._find_walkable_areas_in_the_maze()
        self._randomly_update_diamond_location()
        
    def _find_walkable_areas_in_the_maze(self) -> None:
        """ This functions uses the _world_matrix to create a new matrix which 
        fills all walkable tiles with 1 and climable paths with 3.

        A tile is considered walkable if it is empty and there is a tile platform
        directly above and below it.

        A tile is considered climable is there is a ladder i.e. a 3 in the world
        matrix
        """
        for i in range(len(self._world_matrix)):
            for j in range(len(self._world_matrix[0])):
                # Check if the tile is empty and that there is a tile above and below it
                if(self._world_matrix[i][j] == 0):
                    if ((i - 1 >= 0) and (j - 1 >= 0) and (i + 1 < len(self._world_matrix)) and 
                        (j + 1 < len(self._world_matrix[0]))):
                        if ((self._world_matrix[i-1][j] == 1) and (self._world_matrix[i + 1][j] == 1)):
                            self._walkable_maze_matrix[i][j] = 1
                # Check if the tile contains a ladder
                elif(self._world_matrix[i][j] == 3):
                    self._walkable_maze_matrix[i][j] = 3
    
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
                # During this loop we can also clear the position of the current
                # diamond location, on the original maze.
                if self._world_matrix[i][j] == 2:
                    self._world_matrix[i][j] = 0
                    
                
        # Next we randomly choose a index to place our diamond
        new_diamond_index = random.choice(location_of_one_indices)

        # Now we can update the position of the diamond rect and maze index
        self._world_matrix[new_diamond_index[0]][new_diamond_index[1]]
        for diamond in self._diamond_group:
            # we pass new_diamond_index[1] as y and vise versa, as went iterate
            # through the column using the second index
            diamond.update_position(new_diamond_index[1], new_diamond_index[0])

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

    def get_collidable_tile_list(self) -> list:
        return self._collidable_tile_list

    def get_diamond_group(self) -> list:
        return self._diamond_group

    def show_walkable_maze_matrix(self) -> None:
        """ Print walkable maze matrix in a nice format """
        print(*self._walkable_maze_matrix, sep="\n")