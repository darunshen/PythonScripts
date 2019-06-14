from utility import RedisOperation
import time
redis_op = RedisOperation.RedisOperation()
# host_ip = '172.17.0.4'
# host_port = 6379
host_port = 6380
host_ip = '127.0.0.1'
keyspace_config = str('KEA')
# keyspace_config = str('Ex')
psub_str = str('__key*__:*')
# psub_str = str('__keyevent@0__:expired')


def KeyEventHandle(message):
    print('event handle called : ', message)


if __name__ == '__main__':
    redis_op.ConnectDB(host=host_ip, port=host_port, db=1)
    redis_op.KeyEventInit(
        keyspace_config, {psub_str: KeyEventHandle}, if_threaded=True)
    # redis_op.AddHash([{'key': '1',
    #                    'value': '11',
    #                    'hash_field': 'redis'},
    #                   {'key': '2',
    #                    'value': '22',
    #                    'hash_field': 'redis'}, ])

    # time.sleep(15)
    # redis_op.AddHash([{'key': '1',
    #                    'value': '11',
    #                    'hash_field': 'redis'}])
    # redis_op.AddHash([{'key': 'ss',
    #                    'value': '11',
    #                    'hash_field': 'redis'},
    #                   {'key': 's1',
    #                    'value': '11',
    #                    'hash_field': 'redis'},
    #                   {'key': 'sss1',
    #                    'value': '11',
    #                    'hash_field': 'redis'}, ], -1)
    result = []
    redis_op.Increase([{'key': 'test11',
                        'value': '11',
                        'expire_time': 5}])
    result.append(redis_op.GetData([{'key': '1'}]))
    time.sleep(6)
    redis_op.Increase([{'key': 'test22',
                        'value': '11',
                        'expire_time': 5}])
    result.append(redis_op.GetData([{'key': '1'}]))
    print(result)
    print('data init done')

    while True:
        time.sleep(0.5)
