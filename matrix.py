import pygame
from led import BiColorSquareLed
from constants import BLACK
class Matrix:

    def __init__(self, rows, cols,x ,y, w,h, clr):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = clr
        self.led_lst = [[None for y in range(rows)] for x in range(cols)]
        self.rows = rows
        self.cols = cols
        distance_x =  w //cols
        distance_y =  h // rows
        for i in range(rows):
            for j in range(cols):
                self.led_lst[i][j] = BiColorSquareLed(BLACK, x + j * distance_x + 2, y + i * distance_y + 2,distance_x -4 , distance_y - 4)

    def draw(self,win):
        pygame.draw.rect(win, self.color, self.rect)
        for y in range(self.rows):
            for x in range(self.cols):
                self.led_lst[y][x].draw(win)

    def set_color(self, pos, clr):
        self.led_lst[pos[0]][pos[1]].set_color(clr)