import RPi.GPIO as GPIO

pinValue = {
    0:GPIO.LOW,
    1:GPIO.HIGH
}

class MeowPin():
    def __init__(self,pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.mode = -1
        self.pwm = None

    def setMode(self,mode):
        GPIO.setup(self.pin,mode)

    def readDigital(self):
        if self.mode != GPIO.IN:
            self.setMode(GPIO.IN)
            self.mode = GPIO.IN
        return GPIO.input(self.pin)
    
    def writeDigital(self,val):
        if self.mode != GPIO.OUT:
            self.setMode(GPIO.OUT)
            self.mode = GPIO.OUT
        GPIO.output(self.pin,pinValue[val])

    def setFrequency(self,hz):
        if self.mode != GPIO.OUT:
            self.setMode(GPIO.OUT)
            self.mode = GPIO.OUT
        if not self.pwm:
            self.pwm = GPIO.PWM(self.pin, hz)
            self.pwm.start(0)
        else:
            self.pwm.ChangeFrequency(hz)
    
    def setDutyfactor(self,dc):
        if self.mode != GPIO.OUT:
            self.setMode(GPIO.OUT)
            self.mode = GPIO.OUT
        if not self.pwm:
            self.pwm = GPIO.PWM(self.pin, 100)
            self.pwm.start(0)
        else:
            self.pwm.ChangeDutyCycle(dc)
        
    

        

    