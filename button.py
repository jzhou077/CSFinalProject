import pygame

class Button:
    def __init__(self, x, y, width, height, label):
        self.pos = (x, y)
        self.hitbox = pygame.Rect(self.pos, (width, height))
        self.label = label
        self.clicked = False
    
    def draw(self, surface):
        action = False

        pos = pygame.mouse.get_pos()

        if self.hitbox.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        surface.blit(self.label, self.pos)

        return action