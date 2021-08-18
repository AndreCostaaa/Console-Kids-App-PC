import pygame
from constants import BACKGROUND
class Led:
    def __init__(self, clr_on, clr_off, x, y):
        self.x = x
        self.y = y
        self.color_on = clr_on
        self.color_off = clr_off
        self.color = self.color_on
        self.on = False

    def set_on(self):
        #self.color = self.color_on
        self.on = True

    def set_off(self):
        #self.color = self.color_off
        self.on = False

    def toggle(self):
        if self.color == self.color_on:
            self.color = self.color_off
        else:
            self.color = self.color_on
        
class RoundLed(Led):
    def __init__(self,clr_on, clr_off,x,y,r):
        super().__init__(clr_on, clr_off,x,y)
        self.radius = r

    def draw(self, win):
        pygame.draw.circle(win, self.color,(self.x, self.y),self.radius, 0 if self.on else 3)

class SquareLed(Led):
    def __init__(self,clr_on, clr_off,x,y,w, h):
        super().__init__(clr_on, clr_off,x,y)
        self.width = w
        self.height = h

    def draw(self, win):
        pygame.draw.rect(win, self.color,(self.x, self.y, self.width, self.height))

class BiColorSquareLed(SquareLed):
    def __init__(self,clr_off, x, y, w, h):
        super().__init__(BACKGROUND, clr_off, x,y,w,h)
    
    def set_color(self, clr):
        self.color = clr