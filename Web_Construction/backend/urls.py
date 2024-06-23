# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：     urls.py
   Description :
   Author :         laofeiji
   date ：          2024-03-12
-------------------------------------------------
"""

from django.urls import re_path

from backend.views import test, get_map_data, get_time_data, get_map_data2, get_title, get_emotion, get_participle,\
    get_register, get_login, change_user, get_user, delete_user

urlpatterns = [
    re_path("test", test, ),
    re_path("map", get_map_data, ),
    re_path("time", get_time_data, ),
    re_path("blogger", get_map_data2, ),
    re_path("title", get_title, ),
    re_path("emotion", get_emotion, ),
    re_path("participle", get_participle, ),
    re_path("register", get_register, ),
    re_path("login", get_login, ),
    re_path("changeUser", change_user, ),
    re_path("getUser", get_user, ),
    re_path("deleteUser", delete_user, ),
]