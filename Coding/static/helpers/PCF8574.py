from RPi import GPIO


class PCF8574:
    def __init__(self, data, clock, address):
        self.data = data
        self.clock = clock
        self.address = address

        self.__setup()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        if (isinstance(value, int)) and (value >= 1) and (value <= 40):
            self.__data = value

    @property
    def clock(self):
        return self.__clock

    @clock.setter
    def clock(self, value):
        if (isinstance(value, int)) and (value >= 1) and (value <= 40):
            self.__clock = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if (isinstance(value, int)) and (value >= 0) and (value <= 7):
            self.__address = value

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.data, GPIO.OUT)
        GPIO.setup(self.clock, GPIO.OUT)

    def __start_conditions(self):
        GPIO.output(self.data, 1)
        GPIO.output(self.clock, 1)
        GPIO.output(self.data, 0)
        GPIO.output(self.clock, 0)

    def __stop_conditions(self):
        GPIO.output(self.clock, 0)
        GPIO.output(self.data, 0)
        GPIO.output(self.data, 1)
        GPIO.output(self.clock, 1)

    def __acknowlege(self):
        GPIO.setup(self.data, GPIO.IN)
        GPIO.output(self.clock, 1)
        datavalue = GPIO.input(self.data)

        if datavalue == 1:
            print('Error occured')
        elif datavalue == 0:
            print('Success')

        GPIO.output(self.clock, 0)
        GPIO.setup(self.data, GPIO.OUT)

    def __write_bit(self, value):
        GPIO.output(self.data, value)
        GPIO.output(self.clock, 1)
        GPIO.output(self.clock, 0)

    def write_byte(self, value):
        mask = 0x80
        for count in range(0, 8):
            bit = value & mask >> count
            self.__write_bit(bit)

    def write_outputs(self, data):
        self.__start_conditions()
        self.write_byte(64)
        self.__acknowlege()  # Ack

        for value in data:
            self.__write_bit(value)

        self.__acknowlege()  # Ack
        self.__stop_conditions()
