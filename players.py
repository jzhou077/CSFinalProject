import pygame
from settings import *
from attacks import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, create_magic):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft = pos)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.on_ground = False

        #movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3
        self.gravity = 0.8
        self.jump_speed = -13

        #magic
        self.create_magic = create_magic

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

    def get_frames(self, sheet, width, height, scale, color, numOfFrames):
        sheet = pygame.image.load(sheet).convert_alpha()
        frames = []
        i = 0
        while i < numOfFrames:
            image = pygame.Surface((width, height)).convert_alpha()
            image.blit(sheet, (0, 0), ((i * width), 0, width, height))
            image = pygame.transform.scale(image, (width * scale, height * scale))
            image.set_colorkey(color)
            frames.append(image)
            i += 1
        return frames

    def update(self):
        self.get_input()
        self.keep_on_map()

class Player1(Player):
    def __init__(self, pos, create_magic):
        super().__init__(pos, create_magic)
        self.import_assets('assets/Devil/')
        self.image = pygame.image.load('assets/Devil/idle1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.status = 'idle'
        self.facing_left = True

    def import_assets(self, asset):
        character_path = asset
        self.animations = {'idle1':[], 'run4':[], 'jump1':[], 'hurt1':[], 'fall1': []}

        for animation in self.animations.keys():
            full_path = character_path + animation + '.png'
            self.animations[animation] = super().get_frames(full_path, 16, 16, 2, (0, 0, 0), int(animation[len(animation) - 1]))

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_left:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump1'
        elif self.direction.y > 0:
            self.status = 'fall1'
        #add that its running left later
        elif self.direction.x < 0:
            self.status = 'run4'
        elif self.direction.x > 0:
            self.status = 'run4'
        else:
            self.status = 'idle1'

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_left = False
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_left = True
        elif keys[pygame.K_UP] and self.on_ground:
            self.jump()
        elif keys[pygame.K_DOWN]:
            pass
        else:
            self.direction.x = 0

    def update(self):
        super().update()
        self.get_status()
        self.animate()

class Player2(Player):
    def __init__(self, pos, create_magic):
        super().__init__(pos, create_magic)
        self.import_assets('assets/Wizard/')
        self.image = pygame.image.load('assets/Wizard/idle5.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, (48, 48))
        self.status = 'idle5'
        self.facing_right = True

    def import_assets(self, asset):
        character_path = asset
        self.animations = {'run6':[], 'hurt2':[], 'idle5':[], 'jump1':[], 'falling2':[], 'castspell4':[], 'groundrecovery3':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation + '.png'
            self.animations[animation] = super().get_frames(full_path, 32, 32, 1, (0, 0, 0), int(animation[len(animation) - 1]))

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False).convert_alpha()
            self.image = flipped_image

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump1'
        elif self.direction.y > 0:
            self.status = 'falling2'
        elif self.direction.x != 0:
            self.status = 'run6'
        else:
            self.status = 'idle5'

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
        else:
            self.direction.x = 0

    def update(self):
        super().update()
        self.get_status()
        self.animate()
        