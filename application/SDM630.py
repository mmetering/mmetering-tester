import minimalmodbus
import datetime

class Meter:
    def __init__(self, id, address, port, start=None, end=None):
        self.id = id
        self.address = address
        self.port = port
        self.start = start
        self.end = end
        self.connected = False

        # port name, slave address (in decimal)
        self.instrument = minimalmodbus.Instrument(port, address)
        self.instrument.debug = False
        self.instrument.serial.timeout = 2.0 #sec
        self.instrument.serial.baudrate = 19200 # Baud
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.handle_local_echo = False

    def is_reachable(self):
        return self.getInputRegister('0x48', 2)
        # Alternatively test baud rate from holding register
        # return self.getHoldingRegister('0x1C', 2) == 3.0

    def getHoldingRegister(self, hexc, length):
        return self.getRegister(hexc, 3, length)

    def getInputRegister(self, hexc, length):
        return self.getRegister(hexc, 4, length)

    def getRegister(self, hexc, code, length):
        try:
            return self.instrument.read_float(int(hexc, 16), functioncode=code, numberOfRegisters=length)
        except OSError:
            pass
        except RuntimeError:
            print("There has been an runtime error", file=sys.stderr)
            print("Exception: ", exc_info=True, file=sys.stderr)

