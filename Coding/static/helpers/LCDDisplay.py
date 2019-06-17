from RPi import GPIO
from helpers.PCF8574 import PCF8574
import time


class LCDDisplay:
    def __init__(self, e, rs, pcf_data, pcf_clock, pcf_address):
        self.__e = e
        self.__rs = rs

        self.__pcf_data = pcf_data
        self.__pcf_clock = pcf_clock
        self.__pcf_address = pcf_address

        self.__init_gpio()

    def __init_gpio(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.__rs, GPIO.OUT)
        GPIO.setup(self.__e, GPIO.OUT)

        self.__pcf8574 = PCF8574(self.__pcf_data, self.__pcf_clock, self.__pcf_address)

    def __send_instruction(self, value):
        bits = []
        mask = 0x80

        for position in range(0, 8):
            bit = value & mask >> position
            bits.append(bit)

        self.__set_data_bits(bits)

    def __send_character(self, value):
        letter = ord(value)

        bits = []
        mask = 0x80

        for position in range(0, 8):
            bit = letter & mask >> position
            bits.append(bit)

        GPIO.output(self.__rs, 1)
        self.__set_data_bits(bits)
        GPIO.output(self.__rs, 0)

    def __set_data_bits(self, value):
        for position in range(0, 8):
            if value[position] > 0:
                value[position] = 1
            else:
                value[position] = 0

        self.__pcf8574.write_outputs(value)

        GPIO.output(self.__e, 1)
        time.sleep(0.001)
        GPIO.output(self.__e, 0)

    def init_LCD(self):
        self.reset_LCD()
        self.display_on()
        self.clear_LCD()

    def reset_LCD(self):
        self.__send_instruction(56)

    def clear_LCD(self):
        self.__send_instruction(1)

    def second_row(self):
        self.__send_instruction(192)

    def cursor_position(self, row, position):
        if isinstance(row, int) and isinstance(position, int) and row > 0 and row < 3 and position >= 0 and position <= 40:

            if row == 1:
                value = 0x80 | position
            elif row == 2:
                value = 0xC0 | position

            self.__send_instruction(value)

    def display_on(self):
        self.__send_instruction(14)

    def write_message(self, message):
        message = str(message)
        message.strip()

        for char in range(0, len(message)):

            letter = message[char:char+1]
            self.__send_character(letter)
