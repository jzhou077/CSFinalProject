from settings import *
import pygame

def main_menu(screen):
    BACKGROUND = pygame.transform.scale(pygame.image.load('assets/sky_bottom.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(BACKGROUND, (0, 0))