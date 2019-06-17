from RPi import GPIO


class Ledstrip:
    def __init__(self, red, green, blue):
        self.__red = red
        self.__green = green
        self.__blue = blue

        self.__init_gpio()

    def __init_gpio(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.__red, GPIO.OUT)
        GPIO.setup(self.__green, GPIO.OUT)
        GPIO.setup(self.__blue, GPIO.OUT)

        GPIO.output(self.__red, 1)
        GPIO.output(self.__green, 1)
        GPIO.output(self.__blue, 1)

    def white(self):
        GPIO.output(self.__red, 1)
        GPIO.output(self.__green, 1)
        GPIO.output(self.__blue, 1)

    def red(self):
        GPIO.output(self.__red, 1)
        GPIO.output(self.__green, 0)
        GPIO.output(self.__blue, 0)

    def green(self):
        GPIO.output(self.__red, 0)
        GPIO.output(self.__green, 1)
        GPIO.output(self.__blue, 0)

    def blue(self):
        GPIO.output(self.__red, 0)
        GPIO.output(self.__green, 0)
        GPIO.output(self.__blue, 1)

    def magenta(self):
        GPIO.output(self.__red, 1)
        GPIO.output(self.__green, 0)
        GPIO.output(self.__blue, 1)

    def yellow(self):
        GPIO.output(self.__red, 1)
        GPIO.output(self.__green, 1)
        GPIO.output(self.__blue, 0)

    def cyan(self):
        GPIO.output(self.__red, 0)
        GPIO.output(self.__green, 1)
        GPIO.output(self.__blue, 1)

    def off(self):
        GPIO.output(self.__red, 0)
        GPIO.output(self.__green, 0)
        GPIO.output(self.__blue, 0)