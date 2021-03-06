import serial
import sys
import time


class rfid_reader() :
    @staticmethod
    def factory(t):
        if t == 'hid':
            return rfid_reader_hid()
        elif t == 'serial':
            return rfid_reader_serial()
        assert 0, "bad rfid type specified: " + t
    
    def initialize(self, baud_rate=None) :
        pass

    def get_card(self):
        return None

    def flush(self):
        pass

    def fileno(self):
        pass


class rfid_reader_hid(rfid_reader) :

    def get_card(self):
        return input()

    def flush(self):
        pass

    def fileno(self):
        return sys.stdin.fileno()
        
class rfid_reader_serial(rfid_reader) :
    def __init__(self) :
        # self.ID = ""
        # self.Zeichen = 0
        # self.checksum = 0
        # self.Tag = 0
        pass


    def fileno(self):
        return self.UART.fileno()
    
    def initialize(self, serial_port="/dev/ttyAMA0", baud_rate=9600) :

        print('port %s %d baud' % (serial_port, baud_rate))
        # Open UART (close first just to make sure)
        #
        self.UART = serial.Serial(serial_port, baud_rate)
        self.UART.close()
        self.UART.open()


    def flush(self) :
#        self.UART.reset_input_buffer()
        self.UART.flushInput()  # Deprecated since version 3.0: see reset_input_buffer()


    def get_card(self) :

        if not self.UART.inWaiting() :
            return None

        # Reset vars
        checksum = 0
        checksum_Tag = 0
        ID = ""

        # Read chars
        buf = self.UART.read(size=1)

        # look for STX
        if buf[0] != 0x02:
            self.flush()
            return None

        # Build ID
        for Counter in range(13):
            buf = self.UART.read(size=1)
            ID = ID + '%c' % buf[0]

        # Remove ETX from string
        ID = ID.replace("\x03", "")


        # Calc checksum
        for I in range(0, 9, 2):
            checksum = checksum ^ (((int(ID[I], 16)) << 4) + int(ID[I+1], 16))
        checksum = hex(checksum)
        # Find tag
        Tag = ((int(ID[1], 16)) << 8) + ((int(ID[2], 16)) << 4) + ((int(ID[3], 16)) << 0)
        Tag = hex(Tag)
        # Print data

        card = str(int(ID[4:10], 16))
        print("------------------------------------------")
        print("Data: ", ID)
        print("Tag: ", Tag)
        print("ID: ", ID[4:10], " - ", int(ID[4:10], 16))
        print("Checksum: ", checksum)
        print("------------------------------------------")


        return card





