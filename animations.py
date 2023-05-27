import pygame

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'wizard_spell': self.get_frames('assets/Wizard/spell4.png', 32, 32, 1, (0,0,0), 4),
            'bullet': self.get_frames('assets/Agent/bullet1.png', 16, 16, 2, (0, 0, 0), 1)
        }

    def reflect_images(self, frames):
        new_frames = []
        
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

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
    
    def create_spell(self, animation_type, pos, groups, facing):
        animation_frames = self.frames[animation_type]
        Attack(pos, animation_frames, groups, facing, animation_type)

class Attack(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, facing, animation_type):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.type = animation_type

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.facing = facing
        self.direction = pygame.math.Vector2(0, 0)
        self.projectile_speed = 4
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.facing == 'right':
            self.direction.x = 1
        else:
            self.direction.x = -1
        self.animate()