import serial

class Rosbot:
    def __init__(self, port='/dev/ttyAMA0', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.ser.flush()

    def send_command(self, command, wait=False):
        self.ser.write((command + '\n').encode('utf-8'))
        if wait:
            response = self.ser.readline().decode('utf-8').strip()
            return response

    def pinMode(self, pin, mode):
        command = f'M1 {pin} {mode}'
        self.send_command(command)

    def digitalWrite(self, pin, level):
        command = f'M2 {pin} {level}'
        self.send_command(command)

    def digitalRead(self, pin):
        command = f'M3 {pin}'
        response = self.send_command(command, True)
        return int(response.split()[-1])

    def analogWrite(self, pin, pwm):
        command = f'M4 {pin} {pwm}'
        self.send_command(command)

    def analogRead(self, pin):
        command = f'M5 {pin}'
        response = self.send_command(command, True)
        return int(response.split()[-1])
    
    def led(self, pin, level):
        command = f'M2 {pin} {level}'
        self.send_command(command)

    def motorSpeed(self, index, speed):
        command = f'M200 {index} {speed}'
        self.send_command(command)

    def motorDual(self, speed1, speed2, delay=0):
        command = f'M204 {speed1} {speed2} {delay}'
        self.send_command(command)

    def motorQuad(self, speed1, speed2, speed3, speed4):
        command = f'M205 {speed1} {speed2} {speed3} {speed4}'
        self.send_command(command)

    def motorStop(self):
        command = f'M203'
        self.send_command(command)

    def servo(self, pin, angle, speed):
        command = f'M212 {pin} {angle} {speed}'
        self.send_command(command)

    def close(self):
        self.ser.close()