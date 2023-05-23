import pygame

class Nagic(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 3
        self.direction = pygame.math.Vector2(0, 0)
    
    def spawn(self, pos):
        self.image = pygame.Surface((48, 24))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction.x = 1

    def destroy(self):
        self.kill()