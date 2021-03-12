import pygame
from led import RoundLed
from matrix import Matrix
from constants import *
from button import Button
import random

class Card:

    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = color
        self.led_red = RoundLed(RED, DARK_RED, x + (w // 5), y + h * 4//10, 25)
        self.led_green = RoundLed(GREEN, DARK_GREEN, x + (w // 5), y + (h * 6//10), 25)
        self.led_yellow = RoundLed(ORANGE, DARK_ORANGE, x + w * 4//5, y + h * 4//10, 25)
        self.led_blue = RoundLed(BLUE, DARK_BLUE, x + w * 4//5, y + (h * 6 //10), 25)

        d = ((x + w * 4//5) - (x + (w // 5))) 
        d2 = (y + (h * 6 //10)) - (y + (h * 4//10))
        self.matrix = Matrix(8,8, (x + (w // 5)) + (d // 4),(y + (h * 4//10)) - ((d//2 - d2) //2), d // 2, d // 2, WHITE)

        self.button_red = Button(x + (w // 10), y + h * 4//10 -25, 50,50, RED)
        self.button_green = Button(x + (w // 10), y + h * 6//10 -25, 50,50, GREEN)
        self.button_yellow = Button(x + (w * 9// 10), y + h * 4//10 -25, 50,50, ORANGE)
        self.button_blue = Button(x + (w  * 9// 10), y + h * 6//10 - 25, 50,50, BLUE)
        self.component_lst = [self.led_red, self.led_green, self.led_yellow, self.led_blue, self.button_red, self.button_green, self.button_yellow, self.button_blue, self.matrix]
        self.led_lst = [self.led_red, self.led_green, self.led_yellow, self.led_blue]
        self.btn_lst = [self.button_red, self.button_green, self.button_yellow, self.button_blue]
    def draw(self,win):
        pygame.draw.rect(win, self.color, self.rect)
        for component in self.component_lst:
            component.draw(win)
