'''
提供mqtt相关方法
'''

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import random
import json


class MqttOperation:
    action_map = {}         # 存储所有action与其对应处理函数的映射关系
    subscribe_topics = []   # 存储所有要订阅的topic
    client = {}             # 存储mqtt client

    def init_subscribe_topics(self, topics):
        self.subscribe_topics = topics

    def on_connect(self, client, userdata, flags, rc):
        '''
        连接建立时的回调函数
        '''
        print("Connected with result code "+str(rc))
        for topic in self.subscribe_topics:
            client.subscribe(topic)

    def on_disconnect(self, client, userdata, rc):
        '''
        连接断开时的回调函数
        '''
        print('Disconnect for :'+client._client_id.decode())
        print('The result code:'+str(rc))

    def on_message(self, client, userdata, msg):
        '''
        消息到达时的回调函数
        '''
        payload = json.loads(msg.payload.decode(
            encoding="utf-8", errors="ignore"))
        function = self.action_map.get(payload["action"])
        if function:
            function(client, payload)
        else:
            print('have not the process of this action ')
            print('payload["action"] = '+payload["action"])
            print('action_map : ')
            print(self.action_map)

    def add_actions(self, action_name, action_procedure):
        '''
        添加一个action与其处理函数的映射关系
        '''
        if hasattr(action_procedure, '__call__'):
            self.action_map[action_name] = action_procedure
        else:
            print('the input arguement [' +
                  action_procedure+'is not a procedure!')

    def init_mqtt_client(self, hostname, port, username, password,
                         client_id,
                         if_new_thread, userdata, on_connect,
                         on_disconnect, on_message):
        '''
        hostname : broker ip 或 域名
        port : broker 端口号
        username : broker 用户名
        password : broker 密码
        client_id : 传递给mosquitto服务器的唯一的client id
        if_new_thread : 是否在新的线程启动此client
        userdata : 传递给mqtt
        on_connect : 建立连接的回调函数
        on_disconnect : 断开连接的回调函数
        on_message : 消息到达时的回调函数
        '''
        global client
        client = mqtt.Client(client_id, True, userdata)
        client.username_pw_set(username, password)
        if not on_connect:
            client.on_connect = self.on_connect
        else:
            client.on_connect = on_connect
        if not on_message:
            client.on_message = self.on_message
        else:
            client.on_message = on_message
        if not on_disconnect:
            client.on_disconnect = self.on_disconnect
        else:
            client.on_disconnect = on_disconnect
        print(str(hostname) + ' ' + str(port))
        client.connect(hostname, port, 120)
        if if_new_thread:
            client.loop_start()
        else:
            client.loop_forever()

    def publish(self, topic, payload):
        global client
        client.publish(topic, payload)

    def generate_client_id(self):
        return ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 10))
