'''
提供数据类型的处理相关的方法
'''
import struct


class DataOperation:
    def BytesToFloat8List(self, bytes_data):
        float_size = len(bytes_data)/4
        result_tmp = struct.unpack(
            'f'*int(float_size), bytes_data)
        result = []
        for i in result_tmp:
            result.append(float(i))
        return result
