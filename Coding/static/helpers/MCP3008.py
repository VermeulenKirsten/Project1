from spidev import SpiDev


class MCP3008:
    def __init__(self, bus, slave):
        self.__spi = SpiDev()
        self.__spi.open(bus, slave)
        self.__spi.max_speed_hz = 10 ** 5

    def read_channel(self, channel):
        channel = (channel * 0x10) + 0x80
        value = self.__spi.xfer2([0x1, channel, 0x0])
        return (value[1] & 3) << 8 | value[2]

    def close_bus(self):
        self.__spi.close()
