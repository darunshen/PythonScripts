from utility import RedisOperation
import time
redis_op = RedisOperation.RedisOperation()
# host_ip = '172.17.0.4'
# host_port = 6379
host_port = 6380
host_ip = '127.0.0.1'


def KeyEventHandle(message):
    print('event handle called : ', message)


if __name__ == '__main__':
    redis_op.ConnectDB(host=host_ip, port=host_port)
    redis_op.KeyEventInit('Ex', '__keyevent@0__:expired',
                          KeyEventHandle, if_threaded=True)
    redis_op.AddHash([{'key': '1',
                       'value': '11',
                       'hash_field': 'redis'},
                      {'key': '2',
                       'value': '22',
                       'hash_field': 'redis'}, ])

    time.sleep(10)
    redis_op.AddHash([{'key': '1',
                       'value': '11',
                       'hash_field': 'redis'}])
    while True:
        time.sleep(0.5)
