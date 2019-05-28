import redis


class RedisOperation:
    redis_op = {}

    def ConnectDB(self, password=None, host="127.0.0.1", port=6379, db=0):
        '''
        连接到redis，db为redis数据库编号
        '''
        self.redis_op = redis.Redis(
            host=host, port=port, password=password, db=db)

    def KeyEventInit(self, config_str, psub_str, event_handle, if_threaded=False, sleep_time=0.5):
        '''
        键事件监听初始化
        config_str: 键空间通知选项
        psub_str: 键事件通知订阅的主题
        event_handle: 键事件处理函数
        if_threaded: 消息轮询是否单独线程
        sleep_time: 消息轮询时间间隔，单位是秒
        '''
        pubsub_op = self.redis_op.pubsub()
        self.redis_op.config_set('notify-keyspace-events', config_str)
        pubsub_op.subscribe(**{psub_str: event_handle})
        if if_threaded:
            pubsub_op.run_in_thread(sleep_time=sleep_time)
        else:
            while True:
                pubsub_op.get_message(timeout=sleep_time)

    def AddHash(self, data, expired_time=10):
        '''
        添加散列数据data
        data样式:[
            {'key':'1',
             'value':'11',
             'hash_field':'redis'},
             ....
        ]
        '''
        try:
            for item in data:
                self.redis_op.hset(
                    item['hash_field'], item['key'], item['value'])
                self.redis_op.expire(item['hash_field'], expired_time)
        except Exception as e:
            print('error when add redis entry:', e)
