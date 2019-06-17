# Importing classes
from RPi import GPIO
from time import sleep
from subprocess import check_output
from helpers.MCP3008 import MCP3008
from helpers.LCDDisplay import LCDDisplay
from helpers.Ledstrip import Ledstrip
from mfrc522 import SimpleMFRC522
from serial import Serial, PARITY_NONE

# Initializing classes

# Initializing variables


# Methodes



try:
    teller = 0
    while True:
        code = input('iets: ')
        print(code)


except Exception as e:
    print('Error: ' + str(e))
finally:
    GPIO.cleanup()
