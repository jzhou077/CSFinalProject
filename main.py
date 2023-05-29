import pygame, sys
from settings import *
from screens import main_menu

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

main_menu(SCREEN)