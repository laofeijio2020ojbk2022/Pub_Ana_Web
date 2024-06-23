from django.urls import re_path

from crawler import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.MyConsumer.as_asgi()),
]

