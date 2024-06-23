import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class MyConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        # print(self.room_name)
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # print(self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        # self.room_group_name = self.room_name

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 接受所有websocket请求
        self.accept()

        # self.send(text_data=json.dumps({
        #     'message': 'connected'
        # }))

    # websocket断开时执行方法
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        pass

    # 从频道组接收到消息后执行方法
    def chat_message(self, event):
        message = event['message']

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': message
        }))

        if message['flag']:
            self.close()