import serial
import time
from serial.serialutil import SerialException
from constants import VALID_MSG_BEGGINING
class Serial:
    def __init__(self, com, br, time_out=0.1):
        self.serial = None
        self.buffer = []
        self.disconnected = True
        self.start(com, br)

    def start(self, com, br):
        try:
            self.serial = serial.Serial(com, br)
            self.buffer = []
            self.disconnected = False
            time.sleep(1)
            self.setData('k')
        except:
            print("Could not open port", com)
        
    def open(self):
        if not self.disconnected:
            if not self.serial.isOpen():
                self.serial.open()
            self.serial.reset_input_buffer()

    def close(self):
        self.serial.close()

    def getNewData(self):
        if not self.disconnected:
            try:
                string_in = []
                valid_start = False
                if self.serial.in_waiting > 0:
                    data = self.serial.read(self.serial.in_waiting)
                    for i in range(len(data)):
                        if chr(data[i]) in VALID_MSG_BEGGINING or valid_start:
                            valid_start = True
                            if chr(data[i]) == "\r":
                                self.buffer.append(string_in)
                                valid_start = False
                                string_in = []
                            else:
                                string_in.append(data[i])
            except SerialException as e:
                print(e)
                if not self.disconnected:
                    print("Disconnected")
                    self.disconnected = True

    def getData(self):
        if len(self.buffer) > 0:
            return self.buffer.pop(0)
        return 0

    def setData(self, data):
        if not self.disconnected:
            self.serial.write(data.encode())
