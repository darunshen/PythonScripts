import serial
import serial.threaded.ReaderThread
import serial.threaded.LineReader
import threading
import sys


class SerialOperation:
    thread_read = None
    tty_serial_map = {}

    def InitSerial(self, port, baudrate=115200):
        ser = serial.Serial()
        ser.port = port
        ser.baudrate = baudrate
        ser.timeout = 2
        ser.open()
        if ser.isOpen():
            self.tty_serial_map[port] = ser
            return True
        else:
            return False


if __name__ == '__main__':
    class SerialLineProcess(LineReader):
        def connection_made(self, transport):
            super(PrintLines, self).connection_made(transport)
            sys.stdout.write('port opened\n')

        def handle_line(self, data):
            sys.stdout.write('line received: {}\n'.format(repr(data)))

        def connection_lost(self, exc):
            if exc:
                traceback.print_exc(exc)
            sys.stdout.write('port closed\n')

        # ser = serial.serial_for_url('loop://', baudrate=115200, timeout=1)
        # with ReaderThread(ser, PrintLines) as protocol:
        #     protocol.write_line('hello')
        #     time.sleep(2)
