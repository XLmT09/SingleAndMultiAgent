import pygame

TILE_SIZE = 50

class World:
    def __init__(self, world_data):
        self.data = world_data
        self.tile_list = []
        self.asset_list = []

        for i in range(1, 5):
            image = pygame.image.load(f"assets/images/blocks/tile{i}.png").convert_alpha()
            self.asset_list.append(image)

        row_cnt = 0
        for row in world_data:
            col_cnt = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(self.asset_list[0], (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_cnt += 1
            row_cnt += 1

    def load_world(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

        return self.tile_list