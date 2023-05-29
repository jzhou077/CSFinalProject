import pygame
from tiles import Tile, TerrainTile, WaterTile
from settings import *
from players import *
from animations import *
from magic import *
from ui import UI
from background import *

class Game:
    def __init__(self, surface):
        self.display_surface = surface
        self.setup_level()
        self.ui = UI(self.display_surface)

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_tile_group(self, layout, type):
        terrain = import_cut_graphics('assets/map/tiles/terrain.png')
        decorations = import_cut_graphics('assets/map/tiles/decorations.png')

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = tile_size * col_index
                    y = tile_size * row_index

                    if val == 'P1':
                        player_sprite = Player1((x, y), self.create_magic)
                        self.player1.add(player_sprite)
                    elif val == 'P2':
                        player_sprite = Player2((x, y), self.create_magic)
                        self.player2.add(player_sprite)
                    elif type == 'terrain':
                        tile_surface = terrain[int(val)]
                        sprite = TerrainTile((x, y), tile_size, tile_surface)
                        self.terrain.add(sprite)
                    elif type == 'bridge':
                        tile_surface = decorations[int(val)]
                        sprite = TerrainTile((x, y), tile_size, tile_surface)
                        self.terrain.add(sprite)
                    elif type == 'layer1_deco':
                        tile_surface = decorations[int(val)]
                        sprite = TerrainTile((x, y), tile_size, tile_surface)
                        self.decoration_layer2.add(sprite)
                    elif type == 'layer2_deco':
                        tile_surface = decorations[int(val)]
                        sprite = TerrainTile((x, y), tile_size, tile_surface)
                        self.decoration_layer1.add(sprite)
                    elif type == 'water':
                        tile_surface = decorations[int(val)]
                        sprite = WaterTile((x, y), tile_size, tile_surface)
                        self.water_tiles.add(sprite)

    def setup_level(self):
        self.attacks = pygame.sprite.Group()
        self.player1 = pygame.sprite.GroupSingle()
        self.player2 = pygame.sprite.GroupSingle()

        self.terrain = pygame.sprite.Group()
        self.decoration_layer1 = pygame.sprite.Group()
        self.decoration_layer2 = pygame.sprite.Group()
        self.water_tiles = pygame.sprite.Group()

        self.sky = Sky(12)
        self.clouds = Clouds(200, 5)

        terrain_layout = import_csv_layout('assets/map/tiles/terrain_layout.csv')
        self.create_tile_group(terrain_layout, 'terrain')
        
        bridge_layout = import_csv_layout('assets/map/tiles/bridge_layout.csv')
        self.create_tile_group(bridge_layout, 'bridge')

        layer1_layout = import_csv_layout('assets/map/tiles/tree_rock_layout.csv')
        self.create_tile_group(layer1_layout, 'layer1_deco')

        layer2_layout = import_csv_layout('assets/map/tiles/fence_layout.csv')
        self.create_tile_group(layer2_layout, 'layer2_deco')

        water_layout = import_csv_layout('assets/map/tiles/water_layout.csv')
        self.create_tile_group(water_layout, 'water')

    def horizontal_movement(self):
        player1 = self.player1.sprite
        player2 = self.player2.sprite
        player1.rect.x += player1.direction.x * player1.speed
        player2.rect.x += player2.direction.x * player2.speed
        for attack in self.attacks:
            attack.rect.x += attack.direction.x * attack.projectile_speed
            if attack.type == 'wizard_spell' and attack.rect.colliderect(player1.rect):
                player1.current_health -= 10
                attack.kill()
            elif attack.type == 'bullet' and attack.rect.colliderect(player2.rect):
                player2.current_health -= 10
                attack.kill()

        for sprite in self.terrain.sprites():
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
            for attack in self.attacks:
                if sprite.rect.colliderect(attack.rect) or attack.rect.left < -50 or attack.rect.right > SCREEN_WIDTH + 50:
                    attack.kill()

    def vertical_movement(self):
        player1 = self.player1.sprite
        player2 = self.player2.sprite
        player1.apply_gravity()
        player2.apply_gravity()

        for sprite in self.terrain.sprites():
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

    def create_magic(self, style):
        if style == 'wizard_spell':
            self.magic_player.wizard_spell(self.player2.sprite, self.attacks)
        if style == 'bullet':
            self.magic_player.bullet(self.player1.sprite, self.attacks)

    def run(self):
        
        #background
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, 2)

        #health bar
        self.ui.show_health(self.player1.sprite.current_health, self.player1.sprite.max_health, self.player2.sprite.current_health, self.player2.sprite.max_health)

        #tile sprites
        self.terrain.draw(self.display_surface)
        self.decoration_layer1.draw(self.display_surface)
        self.decoration_layer2.draw(self.display_surface)
        self.water_tiles.draw(self.display_surface)

        #attacks
        for attack in self.attacks:
            attack.update()
        self.attacks.draw(self.display_surface)

        #movement
        self.horizontal_movement()
        self.vertical_movement()

        #update player 1
        self.player1.update()
        self.player1.draw(self.display_surface)

        #update player 2
        self.player2.update()
        self.player2.draw(self.display_surface)

        if self.player1.sprite.check_alive() == False:
            return 2
        elif self.player2.sprite.check_alive() == False:
            return 1
        
        return -1