import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.rect = self.image.get_rect(topleft = pos)

        #movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -16
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def keep_on_map(self):
        if self.rect.left < 0 and self.direction.x < 0:
            self.direction.x = 0
        if self.rect.right > SCREEN_WIDTH and self.direction.x > 0:
            self.direction.x = 0

    def update(self):
        self.get_input()
        self.keep_on_map()

class Player1(Player):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load('assets/Devil/Standing.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_UP]:
            self.jump()
        else:
            self.direction.x = 0

class Player2(Player):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load('assets/Ghost/Movement.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_SPACE]:
            self.jump()
        else:
            self.direction.x = 0
        