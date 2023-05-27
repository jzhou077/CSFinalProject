import pygame 

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def wizard_spell(self, player, groups):
        if player.facing == 'right':
            facing = 'right'
        elif player.facing == 'left':
            facing = 'left'
        
        x = player.rect.centerx
        y = player.rect.centery
        self.animation_player.create_spell('wizard_spell', (x, y), groups, facing)
    
    def bullet(self, player, groups):
        if player.facing == 'right':
            facing = 'right'
        elif player.facing == 'left':
            facing = 'left'

        x = player.rect.centerx
        y = player.rect.centery
        self.animation_player.create_spell('bullet', (x, y), groups, facing)
