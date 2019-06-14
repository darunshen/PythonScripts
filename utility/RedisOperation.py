import redis
import traceback


class RedisOperations:
    redis_op = {}

    def ConnectDB(self, password=None, host="127.0.0.1", port=6379, db=0):
        '''
        连接到redis，db为redis数据库编号
        '''
        self.redis_op = redis.Redis(
            host=host, port=port, password=password, db=db)

    def KeyEventInit(self, config_str, psub_event_handle_map, if_threaded=False, sleep_time=0.5):
        '''
        键事件监听初始化
        config_str: 键空间通知选项
        if_threaded: 消息轮询是否单独线程
        sleep_time: 消息轮询时间间隔，单位是秒
        psub_event_handle_map: 键事件通知订阅的主题 与 键事件处理函数的映射，是字典
        '''
        pubsub_op = self.redis_op.pubsub()
        self.redis_op.config_set('notify-keyspace-events', config_str)
        pubsub_op.psubscribe(**psub_event_handle_map)
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
                if expired_time > 0:
                    self.redis_op.expire(item['hash_field'], expired_time)
        except Exception as e:
            print('error when add redis hash entry:', e)
            traceback.print_exc()

    def Increase(self, data):
        '''
        执行INCR指令
        data样式:[
            {'key':'1',
             'value':'11',
             'expire_time':5},
             ....
        ]
        '''
        try:
            for item in data:
                self.redis_op.incr(item['key'])
                if item.get('expire_time'):
                    self.redis_op.expire(item['key'], item['expire_time'])
        except Exception as e:
            print('error when increase or expire redis entry:', e)
            traceback.print_exc()

    def GetData(self, data):
        '''
        执行GET指令
        data样式:[
            {'key':'1'},
             ....
        ]
        '''
        result = []
        try:
            for item in data:
                result.append(self.redis_op.get(item['key']))
        except Exception as e:
            print('error when get redis entry:', e)
            traceback.print_exc()
        finally:
            return result

    def SetData(self, data):
        '''
        执行GET指令
        data样式:[
            {'key':'1','value':'test'},
             ....
        ]
        '''
        try:
            for item in data:
                self.redis_op.set(item['key'], item['value'])
        except Exception as e:
            print('error when set redis entry:', e)
            traceback.print_exc()

    def GetKeys(self, key_pattern):
        try:
            return self.redis_op.keys(key_pattern)
        except Exception as e:
            print('error when get redis keys:', e)
            traceback.print_exc()

    def ClearDB(self, if_all=False):
        '''
        清空当下的所有数据
        若if_all = True,则清空所有数据库的所有数据,但此为风险操作
        '''
        if if_all == True:
            self.redis_op.flushall()
        else:
            self.redis_op.flushdb()
