from csv import reader
import pygame

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / 16)
    tile_num_y = int(surface.get_size()[1] / 16)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * 16
            y = row * 16
            new_surf = pygame.Surface((16, 16))
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, 16, 16))
            new_surf = pygame.transform.scale(new_surf, (tile_size, tile_size)).convert_alpha()
            cut_tiles.append(new_surf)

    return cut_tiles

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

tile_size = 32
terrain_layout = import_csv_layout('assets/map/tiles/terrain_layout.csv')

SCREEN_WIDTH = len(terrain_layout[0]) * tile_size
SCREEN_HEIGHT = len(terrain_layout) * tile_size