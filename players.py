import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, create_magic):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft = pos)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.on_ground = False
        self.max_health = 100
        self.current_health = self.max_health

        #movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3
        self.gravity = 0.8
        self.jump_speed = -13

        #magic
        self.create_magic = create_magic
        self.attacking = False
        self.attack_cooldown = 250
        self.attack_time = None

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False

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

    def check_alive(self):
        if self.current_health <= 0:
            return False

    def update(self):
        self.get_input()
        self.keep_on_map()
        self.cooldowns()

class Player1(Player):
    def __init__(self, pos, create_magic):
        super().__init__(pos, create_magic)
        self.player_number = 1
        self.import_assets('assets/Agent/')
        self.image = None
        self.status = 'idle2'
        self.facing = 'right'

    def import_assets(self, asset):
        character_path = asset
        self.animations = {'idle2':[], 'run6':[], 'jumpfall2':[], 'hurt1':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation + '.png'
            self.animations[animation] = super().get_frames(full_path, 32, 32, 1, (0, 0, 0), int(animation[len(animation) - 1]))

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing == 'right':
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False).convert_alpha()
            self.image = flipped_image

    def get_status(self):
        if self.direction.y != 0:
            self.status = 'jumpfall2'
        elif self.direction.x != 0:
            self.status = 'run6'
        else:
            self.status = 'idle2'

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing = 'right'
            if self.on_ground:
                self.jump()
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing = 'left'
            if self.on_ground:
                self.jump()
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing = 'left'
        elif keys[pygame.K_UP] and self.on_ground:
            self.jump()
        else:
            self.direction.x = 0

        if keys[pygame.K_DOWN] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_magic('bullet')

    def update(self):
        super().update()
        self.get_status()
        self.animate()

class Player2(Player):
    def __init__(self, pos, create_magic):
        super().__init__(pos, create_magic)
        self.player_number = 2
        self.import_assets('assets/Wizard/')
        self.image = None
        self.status = 'idle5'
        self.facing = 'left'

    def import_assets(self, asset):
        character_path = asset
        self.animations = {'run6':[], 'hurt2':[], 'idle5':[], 'jump1':[], 'falling2':[], 'castspell4':[], 'groundrecovery3':[], 'repeatcastspell4':[], 'jumpcastspell4':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation + '.png'
            self.animations[animation] = super().get_frames(full_path, 32, 32, 1, (0, 0, 0), int(animation[len(animation) - 1]))

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing == 'right':
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False).convert_alpha()
            self.image = flipped_image

    def get_status(self):
        if self.attacking and self.direction.y > 0:
            self.status = "jumpcastspell4"
        elif self.attacking:
            self.status = "repeatcastspell4"
        elif self.direction.y < 0:
            self.status = 'jump1'
        elif self.direction.y > 0:
            self.status = 'falling2'
        elif self.direction.x != 0:
            self.status = 'run6'
        else:
            self.status = 'idle5'

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = 'right'
            if self.on_ground:
                self.jump()
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = 'left'
            if self.on_ground:
                self.jump()
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = 'left'
        elif keys[pygame.K_w] and self.on_ground:
            self.jump()
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_magic('wizard_spell')

    def update(self):
        super().update()
        self.get_status()
        self.animate()
        