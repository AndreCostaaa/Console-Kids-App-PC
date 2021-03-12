import pygame

class Button:
    def __init__(self, x,y, w, h, clr):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = clr
        self.pressed = False

    def draw(self, win):
        if self.pressed:
            pygame.draw.rect(win, self.color, self.rect)
        else:
            pygame.draw.rect(win, self.color, self.rect, 3)
    
    def set_pressed(self, b):
        self.pressed = b