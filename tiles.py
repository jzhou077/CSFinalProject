import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect(topleft = pos)

class TerrainTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image.blit(surface, (0, 0))

class WaterTile(TerrainTile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size, surface)
        self.image.set_alpha(220)