import pygame
from settings import *

class UI:
    def __init__(self, surface):
        self.display_surface = surface

        self.health_bar_max_width = 152
        self.health_bar_height = 4

        self.p1_health_bar = pygame.image.load('assets/ui/health_bar.png')
        self.p1_health_bar_topleft = (54, 39)

        self.p2_health_bar = pygame.transform.flip(pygame.image.load('assets/ui/health_bar.png'), True, False)
        self.p2_health_bar_topleft = (SCREEN_WIDTH - 54 - self.health_bar_max_width, 39)

    def show_health(self, p1_current, p1_full, p2_current, p2_full):
        self.display_surface.blit(self.p1_health_bar, (20, 10))
        current_health_ratio = p1_current / p1_full
        current_bar_width = self.health_bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.p1_health_bar_topleft, (current_bar_width, self.health_bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

        self.display_surface.blit(self.p2_health_bar, (SCREEN_WIDTH - self.p2_health_bar.get_width() - 20, 10))
        current_health_ratio = p2_current / p2_full
        current_bar_width = self.health_bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.p2_health_bar_topleft, (current_bar_width, self.health_bar_height))
        self.p2_health_bar_topleft = (SCREEN_WIDTH - 54 - self.health_bar_max_width + (self.health_bar_max_width - current_bar_width), 39)
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)