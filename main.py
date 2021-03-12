import pygame
import sys
import threading
from constants import *
from card import Card
from SerialCommunication import Serial


class main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Console App")
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.card = Card(0, 0, WIDTH, HEIGHT, GREY)
        self.draw_list = [self.card]
        self.serial = Serial('COM3', 115200)
        self.LED_DIC = {CMD_RED: self.card.led_red, CMD_GREEN: self.card.led_green,
                        CMD_ORANGE: self.card.led_yellow, CMD_BLUE: self.card.led_blue}
        self.BTN_DIC = {CMD_RED: self.card.button_red, CMD_GREEN: self.card.button_green,
                        CMD_ORANGE: self.card.button_yellow, CMD_BLUE: self.card.button_blue}
        self.read_data_thread = threading.Thread(target=self.process_data)
        self.read_data_thread.setDaemon(True)
        self.read_data_thread.start()
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if not self.serial .disconnected:
                        self.serial.close()
                    sys.exit()
            if self.serial.disconnected:
                self.serial = Serial('COM3', 115200)
            self.draw()

    def draw(self):
        self.window.fill(GREY)
        for obj in self.draw_list:
            obj.draw(self.window)
        pygame.display.update()

    def treat_data_in(self, data):
        if data[0] == SET:
            if data[1] == MATRIX:
                if data[2] != EVERYTHING:
                    self.card.matrix.set_color(
                        (int(data[2]), int(data[3])), COLOR_DIC[data[4]])
                else:
                    index = 4
                    for i in range(2):
                        for j in range(8):
                            self.card.matrix.set_color(
                                (int(data[3]) + i, j), COLOR_DIC[data[index]])
                            index += 1
            if data[1] == LED:
                if data[2] != EVERYTHING:
                    obj = self.LED_DIC[data[2]]
                    if data[3] == ON:
                        obj.set_on()
                    elif data[3] == OFF:
                        obj.set_off()
                else:
                    index = 3
                    for led in self.card.led_lst:
                        if data[index] == ON:
                            led.set_on()
                        elif data[index] == OFF:
                            led.set_off()
                        index += 1
            if data[1] == BTN:
                if data[2] != EVERYTHING:
                    obj = self.BTN_DIC[data[2]]
                    if data[3] == ON:
                        obj.set_pressed(True)
                    elif data[3] == OFF:
                        obj.set_pressed(False)
                else:
                    index = 3
                    for btn in self.card.btn_lst:
                        if data[index] == ON:
                            btn.set_pressed(True)
                        elif data[index] == OFF:
                            btn.set_pressed(False)
                        index += 1
            if data[1] == MIC:
                pass
        elif data[0] == GET:
            pass
        print(data)

    # Thread func

    def process_data(self):
        while True:
            if not self.serial.disconnected:
                self.serial.getNewData()
                data = self.serial.getData()
                if data != 0:
                    self.treat_data_in(data)

if __name__ == "__main__":
    main()
