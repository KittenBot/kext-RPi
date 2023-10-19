import smbus

class MeowI2C:
    def __init__(self):
        self.i2c = smbus.SMBus(1)
    
    def writeBlockData(self,addr,register,data):
        self.i2c.write_i2c_block_data(addr,register,data)

    def readBlockData(self,addr,register,len):
        return self.i2c.read_i2c_block_data(addr,register,len)

    def writeByte(self,addr,data):
        self.i2c.write_byte(addr,data)
    
    def readByte(self,addr):
        return self.i2c.read_byte(addr)
