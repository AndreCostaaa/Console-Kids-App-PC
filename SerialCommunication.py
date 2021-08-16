import serial
import time
from serial.serialutil import SerialException
from constants import VALID_MSG_BEGGINING, DEBUG
class Serial:
    def __init__(self, com, br, time_out=0.1, debug=False):
        self.serial = None
        self.buffer = []
        self.disconnected = True
        self.debug = debug
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
                if self.serial.in_waiting > 0:
                    data = self.serial.readline()
                    
                    self.buffer.append(data)
                    if self.debug:
                        print("Data: ", data)
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
