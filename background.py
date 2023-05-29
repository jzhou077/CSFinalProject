from settings import *
from tiles import *
from random import *
import pygame

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('assets/map/background/sky_top.png')
        self.middle = pygame.image.load('assets/map/background/sky_middle.png')
        self.bottom = pygame.image.load('assets/map/background/sky_bottom.png')
        self.horizon = horizon

        self.top = pygame.transform.scale(self.top, (SCREEN_WIDTH, tile_size))
        self.middle = pygame.transform.scale(self.middle, (SCREEN_WIDTH, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (SCREEN_WIDTH, tile_size))

    def draw(self, surface):
        for row in range(len(terrain_layout)):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

class Water:
    def __init__(self, start):
        self.start = start
        self.image = pygame.image.load('assets/map/background/water_bg.png')
        self.image = pygame.transform.scale_by(self.image, 2)
        self.image.set_alpha(220)

    def draw(self, surface):
        for row in range(len(terrain_layout)):
            y = row * tile_size
            if row == self.start:
                for i in range(int(SCREEN_WIDTH / self.image.get_width()) + 1):
                    surface.blit(self.image, (i * self.image.get_width(), y))

class Clouds:
    def __init__(self, horizon, cloud_number):
        cloud1 = pygame.image.load('assets/map/background/cloud1.png').convert_alpha()
        cloud2 = pygame.image.load('assets/map/background/cloud2.png').convert_alpha()
        cloud3 = pygame.image.load('assets/map/background/cloud3.png').convert_alpha()
        self.cloud_surf_list = [cloud1, cloud2, cloud3]
        
        self.min_x = 0
        self.max_x = SCREEN_WIDTH
        self.min_y = 0
        self.max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(self.cloud_surf_list)
            x = randint(self.min_x, self.max_x)
            y = randint(self.min_y, self.max_y)
            sprite = TerrainTile((x, y), cloud.get_width(), cloud)
            self.cloud_sprites.add(sprite)

    def update(self, shift):
        for sprite in self.cloud_sprites:
            if sprite.rect.right < 0:
                sprite.kill()
                cloud = choice(self.cloud_surf_list)
                y = randint(self.min_y, self.max_y)
                sprite = TerrainTile((SCREEN_WIDTH, y), cloud.get_width(), cloud)
                self.cloud_sprites.add(sprite)
            sprite.rect.x -= shift
    
    def draw(self, surface, shift):
        self.update(shift)
        self.cloud_sprites.draw(surface)

# class Clouds:
#     def __init__(self, start):
#         self.start = start
#         self.image = pygame.image.load('assets/map/background/floating_clouds.png').convert_alpha()
#         self.image = pygame.transform.scale_by(self.image, 2)
#         self.rect = self.image.get_rect(topleft = (0, start * tile_size))

#     def update(self):
#         if self.rect.left < 0:
#             self.rect.right = SCREEN_WIDTH
#         self.rect.x -= 2

#     def draw(self, surface):
#         for row in range(len(terrain_layout)):
#             y = row * tile_size
#             if row == self.start:
#                 surface.blit(self.image, (self.rect.x, y))