from settings import *
from background import Clouds
from button import Button
from game import Game
import pygame
import sys

BACKGROUND = pygame.transform.scale(pygame.image.load('assets/map/background/sky_top.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
TEXT_COLOR = (84, 75, 61)
clock = pygame.time.Clock()

def main_menu(screen):
    clouds = Clouds(SCREEN_HEIGHT - 200, 5)
    font = pygame.font.Font('assets/font.ttf', 125)
    running = True
    while running:
        screen.blit(BACKGROUND, (0, 0))
        clouds.draw(screen, 2)

        play_label = font.render("PLAY", False, TEXT_COLOR)
        play_button = Button(SCREEN_WIDTH / 2 - play_label.get_width()/2, SCREEN_HEIGHT / 2 - play_label.get_height() * 1.25, play_label.get_width(), play_label.get_height() - 10, play_label)
        if play_button.draw(screen):
            running = False
            start_game(screen)

        instructions_label = font.render("INSTRUCTIONS", False, (84, 75, 61))
        instructions_button = Button(SCREEN_WIDTH / 2 - instructions_label.get_width()/2, SCREEN_HEIGHT / 2 + instructions_label.get_height() / 4, instructions_label.get_width(), instructions_label.get_height() - 10, instructions_label)
        if instructions_button.draw(screen):
            running = False
            instructions(screen)

        pygame.display.update()
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

def instructions(screen):
    clouds = Clouds(SCREEN_HEIGHT - 200, 5)
    smallFont = pygame.font.Font('assets/font.ttf', 50)
    largeFont = pygame.font.Font('assets/font.ttf', 150)
    running = True
    while running:
        screen.blit(BACKGROUND, (0, 0))
        clouds.draw(screen, 2)

        line1 = smallFont.render("This is a 2-player game. The goal is to kill the other player using your attacks!", False, TEXT_COLOR)
        screen.blit(line1, (SCREEN_WIDTH / 2 - line1.get_width() / 2, 100))

        line2 = smallFont.render("Player 1 is Agent Colt. Use the arrow keys to control him. Press down arrow to attack!", False, TEXT_COLOR)
        screen.blit(line2, (SCREEN_WIDTH/2 - line2.get_width()/2, 150))

        line3 = smallFont.render("Player 2 is Wizard Luna. Use W, S, D to control her. Press spacebar to attack!", False, TEXT_COLOR)
        screen.blit(line3, (SCREEN_WIDTH/2 - line3.get_width()/2, 200))

        menu_label = largeFont.render("MAIN MENU", False, TEXT_COLOR)
        menu_button = Button(SCREEN_WIDTH/2 - menu_label.get_width()/2, SCREEN_HEIGHT - 200, menu_label.get_width(), menu_label.get_height(), menu_label)
        if menu_button.draw(screen):
            running = False
            main_menu(screen)

        pygame.display.update()
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

def start_game(screen):
    game = Game(screen)
    
    running = True
    while running:
        game_status = game.run()
        if game_status != -1:
            running = False
            end_game(screen, game_status)

        pygame.display.update()
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

def end_game(screen, winner):
    clouds = Clouds(SCREEN_HEIGHT - 200, 5)
    largeFont = pygame.font.Font('assets/font.ttf', 175)
    mediumFont = pygame.font.Font('assets/font.ttf', 100)
    running = True
    while running:
        screen.blit(BACKGROUND, (0, 0))
        clouds.draw(screen, 2)

        if winner == 1:
            winner_name = "Agent Colt"
        else:
            winner_name = "Wizard Luna"

        winner_label = largeFont.render(winner_name + ' Wins!', False, TEXT_COLOR)
        screen.blit(winner_label, (SCREEN_WIDTH/2 - winner_label.get_width()/2, SCREEN_HEIGHT/2 - winner_label.get_height()/2))

        replay_label = mediumFont.render("PLAY AGAIN", False, TEXT_COLOR)
        replay_button = Button(SCREEN_WIDTH/2 - replay_label.get_width()/2, SCREEN_HEIGHT - 150, replay_label.get_width(), replay_label.get_height(), replay_label)
        if replay_button.draw(screen):
            running = False
            main_menu(screen)

        pygame.display.update()
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()