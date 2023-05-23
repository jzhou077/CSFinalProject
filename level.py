import pygame
from tiles import Tile
from settings import *
from players import *

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
    
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player1 = pygame.sprite.GroupSingle()
        self.player2 = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = tile_size * col_index
                y = tile_size * row_index

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P1':
                    player_sprite = Player1((x, y))
                    self.player1.add(player_sprite)
                if cell == 'P2':
                    player_sprite = Player2((x, y))
                    self.player2.add(player_sprite)

    def horizontal_movement(self):
        player1 = self.player1.sprite
        player2 = self.player2.sprite
        player1.rect.x += player1.direction.x * player1.speed
        player2.rect.x += player2.direction.x * player2.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player1.rect):
                if player1.direction.x < 0:
                    player1.rect.left = sprite.rect.right
                elif player1.direction.x > 0:
                    player1.rect.right = sprite.rect.left

            if sprite.rect.colliderect(player2.rect):
                if player2.direction.x < 0:
                    player2.rect.left = sprite.rect.right
                elif player2.direction.x > 0:
                    player2.rect.right = sprite.rect.left

    def vertical_movement(self):
        player1 = self.player1.sprite
        player2 = self.player2.sprite
        player1.apply_gravity()
        player2.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player1.rect):
                if player1.direction.y > 0:
                    player1.rect.bottom = sprite.rect.top
                    player1.direction.y = 0
                    player1.on_ground = True
                elif player1.direction.y < 0:
                    player1.rect.top = sprite.rect.bottom
                    player1.direction.y = 0
            
            if sprite.rect.colliderect(player2.rect):
                if player2.direction.y > 0:
                    player2.rect.bottom = sprite.rect.top
                    player2.direction.y = 0
                    player2.on_ground = True
                elif player2.direction.y < 0:
                    player2.rect.top = sprite.rect.bottom
                    player2.direction.y = 0
        
        if player1.on_ground and player1.direction.y < 0 or player1.direction.y > 1:
            player1.on_ground = False
        if player2.on_ground and player2.direction.y < 0 or player2.direction.y > 1:
            player2.on_ground = False

    def create_magic(self, style, strength):
        pass

    def run(self):
        self.tiles.draw(self.display_surface)

        self.horizontal_movement()
        self.vertical_movement()

        self.player1.update()
        self.player1.draw(self.display_surface)

        self.player2.update()
        self.player2.draw(self.display_surface)