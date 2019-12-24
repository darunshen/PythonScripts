'''
提供串口通信所需的工具
'''
import serial
from serial.threaded import LineReader, ReaderThread
import sys
import struct
import crcmod.predefined


class SerialOperation:
    transport = None
    protocol = {}
    reader_thread = None
    ser = {}

    def InitSerial(self, port, Policy, baudrate=115200, if_use_thread=True):
        '''
        初始化生成一个串口通信的实例
        port:串口名称 ，如'/dev/ttyUSB0'
        Policy:重载串口通信相关接口的类，而非实例
        baudrate:串口通信波特率
        '''
        self.ser = serial.Serial(timeout=1)
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.stopbits = 1
        self.ser.open()
        if self.ser.isOpen():
            if if_use_thread:
                self.reader_thread = ReaderThread(self.ser, Policy)
                self.reader_thread.start()
                self.transport, self.protocol = self.reader_thread.connect()
            return True
        else:
            return False

    def GetProtocol(self):
        '''
        返回通信的实例
        '''
        return self.protocol

    def StopSerial(self):
        '''
        关闭串口
        '''
        self.reader_thread.close()

    def GetReaderThread(self):
        '''
        返回串口读取线程
        '''
        return self.reader_thread

    def GetSerial(self):
        '''
        返回串口句柄
        '''
        return self.ser

    def GetAppendedCrc16Modbus(self, bytes_data):
        '''
        获取追加了crc16 modbus校验码的数据
        '''
        crcmodbus = crcmod.predefined.mkCrcFun('modbus')
        return bytes_data+(struct.pack('i', crcmodbus(bytes_data))[0:2])


if __name__ == '__main__':
    import traceback

    class SerialLineProcess(LineReader):
        def connection_made(self, transport):
            super(SerialLineProcess, self).connection_made(transport)
            sys.stdout.write('port opened\n')

        def handle_line(self, data):
            sys.stdout.write('line received: {}\n'.format(repr(data)))

        def connection_lost(self, exc):
            if exc:
                traceback.print_exc(exc)
            sys.stdout.write('port closed\n')

        # ser = serial.serial_for_url('loop://', baudrate=115200, timeout=1)
        # with ReaderThread(ser, SerialLineProcess) as protocol:
        #     protocol.write_line('hello')
        #     time.sleep(2)
    # ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
    # t = ReaderThread(ser, SerialLineProcess)
    # t.start()
    # transport, protocol = t.connect()
    # protocol.write_line('hello')
    # time.sleep(2)
    # t.close()
    test_exa = SerialOperation()
    test_exa.InitSerial('/dev/ttyUSB0', SerialLineProcess)
