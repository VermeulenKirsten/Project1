from RPi import GPIO
from helpers.PCF8574 import PCF8574
from time import sleep


class Lock:
    def __init__(self, pin):
        self.__pin = pin

        self.__init_gpio()

    def __init_gpio(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, 0)

    def open_lock(self):
        GPIO.output(self.__pin, 1)

    def close_lock(self):
        GPIO.output(self.__pin, 0)
