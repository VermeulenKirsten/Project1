from subprocess import check_output
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from time import sleep
import threading
import smtplib, ssl

# Importing classes

from RPi import GPIO
from serial import Serial
from helpers.SimpleMFRC522 import SimpleMFRC522
from helpers.Keypad import Keypad
from helpers.MCP3008 import MCP3008
from helpers.Ledstrip import Ledstrip
from helpers.Database import Database
from helpers.LCDDisplay import LCDDisplay
from helpers.Lock import Lock
from datetime import datetime
import random

try:

    # App settings
    # sleep(90)

    app = Flask(__name__)
    CORS(app)
    socketio = SocketIO(app)

    # Making connection with the database
    conn = Database(app=app, user='mct', password='mct', db='smartpost', host='localhost', port=3306)

    # Initializing variables

    buttons = [[1, 2, 3, 'A'], [4, 5, 6, 'B'], [7, 8, 9, 'C'], ['*', 0, '#', 'D']]
    rows = [17, 27, 22, 5]
    columns = [6, 13, 19, 26]

    ips = str(check_output(['hostname', '--all-ip-addresses'])).split(' ')

    # Initializing classes

    lcddisplay = LCDDisplay(24, 23, 2, 3, 0)

    keypad_module = Keypad(buttons, rows, columns)

    rfid_module = SimpleMFRC522()

    mcp3008 = MCP3008(0, 1)

    lock1 = Lock(12)
    lock2 = Lock(4)

    ledstrip = Ledstrip(21, 16, 20)

    smtpUser = 'SmartPostNMCT@gmail.com'  # For SSL
    smtpPass = 'KSmartPost1!'

    toAdd = 'kirstenvermeul@gmail.com'
    fromAdd = smtpUser

    subject = 'Your Package'
    header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject

    # methods


    def setup():
        # Turning the lights on
        ledstrip.white()

        # Initializing display
        lcddisplay.init_LCD()
        lcddisplay.init_LCD()

        # Printing IP-address
        print_ip()


    def print_ip():
        ip = ips[1].strip('b\'')

        # Print IP-address
        lcddisplay.clear_LCD()
        lcddisplay.write_message("IP-address:")
        lcddisplay.second_row()
        lcddisplay.write_message(ip)


    def read_rfid():
        global badged

        badged = False

        try:
            print('RFID started !')

            while True:
                print("Hold a tag near the reader")
                rfid_id, text = rfid_module.read()
                print("ID: %s\nText: %s" % (rfid_id, text))

                conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(3, %s, null, null)", rfid_id)

                badged = True

                lcddisplay.clear_LCD()
                lcddisplay.write_message("Enter Locker: ")
                lcddisplay.second_row()

                value = 0

                while value == "A" or value == "B" or value == "C" or value == "D" or value == "*" or value == "#" or value <= 0 or value >= 3:
                    value = read_keypad_once()

                    if value == "A" or value == "B" or value == "C" or value == "D" or value == "*" or value == "#" or value <= 0 or value >= 3:
                        lcddisplay.clear_LCD()
                        lcddisplay.write_message("This locker does")
                        lcddisplay.second_row()
                        lcddisplay.write_message("not exist")
                        sleep(3)
                        lcddisplay.clear_LCD()
                        lcddisplay.write_message("Enter Locker: ")
                        lcddisplay.second_row()

                lcddisplay.write_message(value)

                control_locker(value)

                sleep(2)

                print_ip()

                badged = False

        except Exception as e:
            print("Error: " + str(e))
        finally:
            GPIO.cleanup()


    def control_locker(locker):

        inside = 0

        locker_info = conn.get_data("SELECT * FROM locker WHERE lockerID = %s", locker)

        if locker_info[0]['status'] == 0 and locker == 1:
            lock1.open_lock()
        elif locker_info[0]['status'] == 1 and locker == 1:
            ledstrip.red()
            lcddisplay.clear_LCD()
            lcddisplay.write_message('Locker %s is' % (locker))
            lcddisplay.second_row()
            lcddisplay.write_message('in use')
            sleep(2)
            ledstrip.white()
            print_ip()
            read_rfid()

        elif locker_info[0]['status'] == 0 and locker == 2:
            lock2.open_lock()
        elif locker_info[0]['status'] == 1 and locker == 2:
            ledstrip.red()
            lcddisplay.clear_LCD()
            lcddisplay.write_message('Locker %s is' % (locker))
            lcddisplay.second_row()
            lcddisplay.write_message('in use')
            sleep(2)
            ledstrip.white()
            print_ip()
            read_rfid()

        while mcp3008.read_channel(locker - 1) < 100:
            pass

        conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(%s, 'Open', %s, null)", [locker, locker])

        conn.set_data("INSERT INTO eigenaar(voornaam, achternaam, email, straat, huisnummer, postcode, gemeente) VALUES('Kirsten', 'Vermeulen', 'kirstenvermeul@gmail.com', 'Kaleshoekstraat', 3, 8020, 'Ruddervoorde')")

        eigenaar_id = conn.get_data("SELECT EigenaarID FROM eigenaar order by eigenaarID DESC limit 1")

        code = ""

        for teller in range(0, 8):
            code += str(random.randint(0, 9))

        print(code)

        while mcp3008.read_channel(locker - 1) > 100 or inside != 1:
            print(mcp3008.read_channel(locker - 1))
            lightsensors = read_lightsensors(locker)
            for value in lightsensors:
                if value > 600:
                    inside = 1

        if locker == 1:
            lock1.close_lock()
        elif locker == 2:
            lock2.close_lock()

        conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(%s, 'In use', %s, %s)", [locker, locker, eigenaar_id[0]['EigenaarID']])
        conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(%s, 'Closed', %s, %s)", [locker, locker, eigenaar_id[0]['EigenaarID']])

        body = 'Your package has arrived at the depot!\nUse the following code to open the locker.\n\nCode: %s' %(code)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.ehlo()
        s.starttls()
        s.ehlo()

        s.login(smtpUser, smtpPass)
        s.sendmail(fromAdd, toAdd, header + '\n\n' + body)

        s.quit()

        conn.set_data("INSERT INTO inhoud(EigenaarID, code) VALUES(%s, %s)", [eigenaar_id[0]['EigenaarID'], code])

        inhoud_id = conn.get_data("SELECT inhoudID FROM inhoud order by inhoudID desc limit 1")

        conn.set_data("UPDATE locker SET status = 1, inhoudID = %s, laatst_geopend = CURRENT_TIMESTAMP where lockerID = %s", [inhoud_id[0]['inhoudID'], locker])

    def read_lightsensors(locker):
        lightsensors = [0, 0, 0]
        start = 0
        if locker == 1:
            start = 2
        else:
            start = 5
        for teller in range(start, start + 3):
            lightsensors[teller-start] = mcp3008.read_channel(teller)
        print(lightsensors)
        return lightsensors


    def read_keypad():

            global status, input_code

            status = "A"
            previous_status = ""
            input_code = ""

            while True:
                if badged == False:

                    print('Keypad started !')
                    value = ""

                    while value == "" and badged is False:
                        value = keypad_module.read_keypad()
                        sleep(0.1)

                    if badged == True:
                        read_keypad()

                    if value == "A" or value == "B" or value == "C" or value == "D":
                        previous_status = status
                        status = check_keypad_status(value)
                        print(status)
                    else:
                        if status == "B":
                            status = previous_status
                        elif status == "C":
                            input_code += str(value)
                            lcddisplay.write_message(value)


    def check_keypad_status(value):
        if value == "A":
            # IP-address
            print_ip()
            return "A"
        elif value == "B":
            if status != "A":

                # Backspace

                print("Backspace")
                return "B"
        elif value == "C":
            # Code
            lcddisplay.clear_LCD()
            lcddisplay.write_message('Enter your code:')
            lcddisplay.second_row()
            input_code = ""
            return "C"
        elif value == "D":
            # submit code
            if status == "C":
                check_code()
                return "D"
        else:
            return "A"

    def check_code():
        correct = False
        locker = ""
        inside = False

        locker_code = conn.get_data("Select L.lockerID, I.code, I.EigenaarID from locker as L inner join inhoud as I on L.inhoudID = I.inhoudID")

        print(locker_code)

        for code in locker_code:
            if code['code'] == input_code:
                correct = True
                locker = code['lockerID']

        if correct:
            ledstrip.green()

            lcddisplay.clear_LCD()
            lcddisplay.write_message("Your package is")
            lcddisplay.second_row()
            message = "in locker %s" % (str(locker))
            lcddisplay.write_message(message)

            if locker == 1:
                lock1.open_lock()

                while mcp3008.read_channel(locker - 1) < 100:
                    pass

                conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(4, 'Open', 1, %s)", locker_code[0]['EigenaarID'])

                sleep(2)

                ledstrip.white()

                while mcp3008.read_channel(locker - 1) > 100 or inside != 0:
                    lightsensors = read_lightsensors(locker)
                    print(lightsensors)
                    inside = 1
                    for lightsensor in lightsensors:
                        if lightsensor < 600:
                            inside = 0
                        else:
                            inside = 1

                conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(1, 'Empty', 1, %s)", locker_code[0]['EigenaarID'])

                conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(4, 'Closed', 1, %s)", locker_code[0]['EigenaarID'])
                lock1.close_lock()

            elif locker == 2:
                lock2.open_lock()

                while mcp3008.read_channel(locker - 1) < 100:
                    pass

                conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(4, 'Open', 2, %s)", locker_code[0]['EigenaarID'])

                sleep(2)

                ledstrip.white()

                while mcp3008.read_channel(locker - 1) > 100 or inside != 0:
                    lightsensors = read_lightsensors(locker)
                    print(lightsensors)
                    inside = 1
                    for lightsensor in lightsensors:
                        if lightsensor < 600:
                            inside = 0
                        else:
                            inside = 1

                conn.set_data("INSERT INTO geschiedenis(sensorID, actie, lockerID, eigenaarID) VALUES(1, 'Empty', 2, %s)", locker_code[0]['EigenaarID'])

                lock2.close_lock()

            conn.set_data("UPDATE locker SET status = 0, inhoudID = null where lockerID = %s", [locker])

            print_ip()

        else:
            ledstrip.red()
            lcddisplay.clear_LCD()
            lcddisplay.write_message("Incorrect code!")
            sleep(2)
            ledstrip.white()
            print_ip()
            read_keypad()

        print(locker_code)


    def read_keypad_once():
            print('Keypad started !')
            value = ""

            while value == "":
                value = keypad_module.read_keypad()

            return value

    @app.route('/')
    def smartpost():
        return 'Hello World'


    @app.route('/lockers')
    def lockers_route():
        lockers = conn.get_data("SELECT * FROM locker as L left join inhoud as I on L.inhoudID = I.inhoudID left join eigenaar as E on I.eigenaarID = E.eigenaarID;")
        return jsonify(lockers)


    @app.route('/admin_history')
    def admin_history_route():
        admin_history = conn.get_data("SELECT * FROM geschiedenis where sensorID = 3 order by geschiedenisID DESC limit 15")
        return jsonify(admin_history)


    @app.route('/user_history')
    def user_history_route():
        user_history = conn.get_data("SELECT * FROM geschiedenis where sensorID != 3 order by geschiedenisID DESC limit 15")
        return jsonify(user_history)


    @app.route('/dashboard_lockers')
    def dashboard_lockers_route():
        dashboard_lockers = conn.get_data("SELECT * FROM locker")
        return jsonify(dashboard_lockers)


    @app.route('/dashboard_recent_events')
    def dashboard_recent_events_route():
        dashboard_recent_events = conn.get_data("SELECT * FROM geschiedenis order by geschiedenisID desc  limit 6")
        return jsonify(dashboard_recent_events)


    @app.route('/dashboard_bar_graph')
    def dashboard_bar_graph_route():
        dashboard_bar_graph = conn.get_data("SELECT day(tijd_van_actie) as 'day', actie, DATE_FORMAT(tijd_van_actie, '%d %b') as 'date' FROM geschiedenis where tijd_van_actie > date_add(now(), INTERVAL -7 DAY) and actie = 'Empty' or actie = 'In use' order by geschiedenisID desc")
        return jsonify(dashboard_bar_graph)


    @app.route('/dashboard_donut_graph')
    def dashboard_donut_graph_route():
        dashboard_donut_graph = conn.get_data("SELECT actie, DATE_FORMAT(tijd_van_actie, '%H') as 'hour' FROM geschiedenis where tijd_van_actie > date_add(now(), INTERVAL - 7 DAY) and actie = 'Empty' order by tijd_van_actie desc")
        return jsonify(dashboard_donut_graph)

    @app.route('/login', methods=['POST'])
    def login_route():
        if request.method == 'POST':
            print('request gekregen')
            login_data = request.get_json()
            print(login_data)
            login = conn.get_data("SELECT * FROM admin where gebruikersnaam = %s and wachtwoord = %s", [login_data['username'], login_data['password']])
            print(login)
            return jsonify(login)


    @socketio.on("connect")
    def connecting():
        socketio.emit("connected")
        print("Connection with client established")


    @socketio.on("open_locker")
    def connecting(locker):

       info = conn.get_data("SELECT * FROM locker where lockerID = %s", locker)

       if locker == '1' and info[0]['status'] == 0:
           ledstrip.green()
           lock1.open_lock()
           sleep(2)
           lock1.close_lock()
           ledstrip.white()
       elif locker == '1' and info[0]['status'] == 1:
           ledstrip.red()
           lcddisplay.clear_LCD()
           lcddisplay.write_message('This locker is')
           lcddisplay.second_row()
           lcddisplay.write_message('occupied!')
           sleep(2)
           ledstrip.white()
           print_ip()
       elif locker == '2' and info[0]['status'] == 0:
           ledstrip.green()
           lock2.open_lock()
           sleep(2)
           lock2.close_lock()
           ledstrip.white()
       elif locker == '2' and info[0]['status'] == 1:
           ledstrip.red()
           lcddisplay.clear_LCD()
           lcddisplay.write_message('This locker is')
           lcddisplay.second_row()
           lcddisplay.write_message('occupied!')
           sleep(2)
           ledstrip.white()
           print_ip()

    if __name__ == '__main__':
        setup()
        rfid = threading.Thread(name="rfid", target=read_rfid)
        rfid.daemon = True
        rfid.start()
        keypad = threading.Thread(name="keypad", target=read_keypad)
        keypad.daemon = True
        keypad.start()
        socketio.run(app=app, host="0.0.0.0", port=5000)

except Exception as e:
    print("Error: " + str(e))
finally:
    GPIO.cleanup()
