import serial
import time
from serial.serialutil import SerialException
from constants import MSG_SIZE, CONNECTED
class Serial:
    def __init__(self, com, br, time_out=0.1, debug=False):
        self.serial = None
        self.buffer = []
        self.disconnected = True
        self.debug = debug
        self.start(com, br)

    def start(self, com, br):
        try:
            print("Connecting to " + com)
            self.serial = serial.Serial(com, br)
            self.buffer = []
            self.disconnected = False
            self.serial.flushOutput()   
            time.sleep(2)
            self.setData(CONNECTED)
            time.sleep(.5)
            print("Connected to " + com)
        except Exception as e:
            print(e)
        
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
                while self.serial.in_waiting >= MSG_SIZE:
                    data = self.serial.read(MSG_SIZE)              
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

    def setData(self, data: str):
        if not self.disconnected:
            self.serial.write(data.encode('ascii'))
            
