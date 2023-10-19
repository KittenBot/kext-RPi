import serial

class MeowUart:
    def __init__(self, port='/dev/ttyAMA0', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=0)
        self.ser.flush()

    def writeString(self,text):
        self.ser.write(text.encode())
    
    def writeByte(self,byt):
        self.ser.write(byt)
    
    def ifData(self):
        return bool(self.ser.in_waiting)

    def readString(self):
        return self.ser.read_all().decode()
    
    def readStringLine(self):
        return self.ser.readline().decode()
    
    def readByte(self):
        return self.ser.read_all()