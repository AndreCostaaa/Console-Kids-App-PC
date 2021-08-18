import pygame
import sys
import threading
from constants import *
from card import Card
from SerialCommunication import Serial
import argparse
import time

COM = 'COM2'
BR = 115200

class main:
    def __init__(self):
        
        pygame.init()
        pygame.display.set_caption("Console App")
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.card = Card(0, 0, WIDTH, HEIGHT, BACKGROUND)
        self.draw_list = [self.card]
        self.serial = Serial(COM, BR, debug=DEBUG)
        self.LED_ARR = [self.card.led_red, self.card.led_green, self.card.led_yellow, self.card.led_blue]
        self.BTN_ARR = [self.card.button_red,self.card.button_green, self.card.button_yellow, self.card.button_blue]
        self.poll_data_thread = threading.Thread(target=self.poll_data)
        self.poll_data_thread.setDaemon(True)
        self.process_data_thread = threading.Thread(target=self.process_data)
        self.process_data_thread.setDaemon(True)
        self.run()

    def run(self):
        print("Loading Completed")
        self.poll_data_thread.start()
        self.process_data_thread.start()
        last_time = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_program()
            if self.is_thread_dead():
                print("Thread:", self.get_crashed_thread(), "crashed...")
                print("Quitting the program")
                self.quit_program()
            if self.serial.disconnected and time.time() - last_time > 1:
                self.serial = Serial(COM, BR)
                last_time = time.time()
            self.draw()

    def draw(self):
        self.window.fill(GREY)
        for obj in self.draw_list:
            obj.draw(self.window)
        pygame.display.update()

    def quit_program(self):
        if not self.serial .disconnected:
            self.serial.close()
        pygame.quit()
        sys.exit()

    def is_thread_dead(self):
        if not self.poll_data_thread.is_alive() or not self.process_data_thread.is_alive():
            return True
        return False
    def get_crashed_thread(self):
        if not self.poll_data_thread.is_alive():
            return "Poll Data Thread"
        elif not self.process_data_thread.is_alive():
            return "Process Data Thread"
        return "No Thread"

    def treat_data_in(self, data):
        command = chr(data[0])
        detail = chr(data[1])
        if command == SET:
            if detail == MATRIX:
                for i in range(8):
                    row_data = (data[i*2+2] & 0xFF) << 8 | (data[i*2+3] & 0xFF)
                    for j in range(8):
                        self.card.matrix.set_color((i,7 - j), (row_data & (0x3 << j *2)) >> j * 2)
            if detail == LED:
                for i in range(len(self.LED_ARR)):
                    if data[2] & (0x1 << i):
                        self.LED_ARR[i].set_on()
                    else:
                        self.LED_ARR[i].set_off()
            if detail == BTN:
                for i in range(len(self.BTN_ARR)):
                    self.BTN_ARR[i].set_pressed(data[2] & (0x1 << i))
            if detail == MIC:
                pass
        elif command == GET:
            pass
            
    # Thread func
    def process_data(self):
        while True:
            if not self.serial.disconnected:
                data = self.serial.getData()
                if data != 0:
                    if DEBUG:
                        print("Treating:", end="")
                        for i, c in enumerate(data[:-1]):
                            if i < 2:
                                print(chr(c), end=" ")
                            else:
                                print(c, end=" ")
                        print()
                    self.treat_data_in(data)

    def poll_data(self):
        while True:
            self.serial.getNewData()

if __name__ == "__main__":
    print()
    print('-----------------------------------------------------------------------------------------------------')
    print(" Welcome to the Console Kids' PC App")
    print(' In order to use this app, a "Console Kids" board must be connected to the computer')
    print(' Check which COM PORT is being used by the arduino and start this app using "python main.py -c [COM]"')
    print('-----------------------------------------------------------------------------------------------------')
    print()
    parser = argparse.ArgumentParser(description="Console Kids PC App")
    parser.add_argument('-c', '--com', metavar='?', help="REQUIRED: Number of arduino's COM PORT", required=True)
    parser.add_argument('-d', '--debug', help="OPTIONAL: Use this flag for debugging", action="store_true", required=False)
    args = parser.parse_args()

    COM = 'COM'+ args.com
 
       
    if args.debug:
        DEBUG = True
        print("Debug Mode Activated")
    print("Loading ...") 

    main()
