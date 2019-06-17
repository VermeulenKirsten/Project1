from RPi import GPIO
from time import sleep

class Keypad:
    def __init__(self, buttons, rows, columns):
        self.__buttons = buttons
        self.__rows = rows
        self.__columns = columns

        self.__init_gpio()

    def __init_gpio(self):

        GPIO.setmode(GPIO.BCM)

        for row in self.__rows:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, 1)

        for column in self.__columns:
            GPIO.setup(column, GPIO.IN, GPIO.PUD_UP)

    def read_keypad(self):

        value = ""

        for r in range(0, 4):
            GPIO.output(self.__rows[r], 0)

            for c in range(0, 4):
                if GPIO.input(self.__columns[c]) == 0:
                    print(self.__buttons[r][c])
                    value = self.__buttons[r][c]
                    while (GPIO.input(self.__columns[c]) == 0):
                        sleep(0.5)

            GPIO.output(self.__rows[r], 1)

        return value
