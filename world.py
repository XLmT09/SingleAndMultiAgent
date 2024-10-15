import pygame

TILE_SIZE = 50
WHITE = (255, 255, 255)
DIAMOND_ANIMATION_SPEED = 0.2 

class Diamond(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        for i in range(1,9):
            self.sprites.append(pygame.image.load(f"assets/images/pixel-art-diamond/diamond{i}.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.current_sprite += DIAMOND_ANIMATION_SPEED
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

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
        for row in self.world_matrix:
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
                    img = pygame.transform.scale(self.ladder_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (img, img_rect)
                    self._non_collidable_tile_list.append(tile)
                col_cnt += 1
            row_cnt += 1
    
    def get_collidable_tile_list(self) -> list:
        return self._collidable_tile_list

    def get_diamond_group(self) -> list:
        return self._diamond_group

    def draw_grid(self, screen, screen_height, screen_width) -> None:
        """ This functions draws out the grids on the game, to help visualize on 
        what grid every asset is, or which grid the player is currently on.
        """
        for line in range(29):
            # Draw the vertical lines
            pygame.draw.line(screen, WHITE, (line * TILE_SIZE, 0), (line * TILE_SIZE, screen_height))
            # Draw the horizontal lines
            pygame.draw.line(screen, WHITE, (0, line * TILE_SIZE), (screen_width, line * TILE_SIZE))

    def load_world(self, screen, game_over) -> None:
        """ This function blits the maze onto the screen. 
        
        Args: 
            screen (pygame.display): The screen we want to blit the maze onto.
        """
        for tile in self._collidable_tile_list:
            screen.blit(tile[0], tile[1])
        for tile in self._non_collidable_tile_list:
            screen.blit(tile[0], tile[1])
        self._diamond_group.draw(screen)
        if game_over == 0:
            self._diamond_group.update()    
