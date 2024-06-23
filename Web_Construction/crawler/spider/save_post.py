import datetime

import browser_cookie3
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from crawler.models import CookiesTable, TimeTitleTable, TimePostTableAll, TimePostTable, TimeCommentTable
from backend.models import TopicTable, CommentTable, PostTable, PostTableAll, TopicTableAll, UserTable
from crawler.new_math import get_ua
import numpy as np
import pandas as pd
import re
from datetime import date

# Create your views here.


@require_http_methods('GET')
def save_post(request):
    response = {}
    response['back'] = 'success'

    save_PostTableAll()
    save_PostTable()

    return JsonResponse(response)


def save_PostTableAll():
    data_new = TimePostTableAll.objects.all().values()

    for i in data_new:
        mid = i['tp_mid']
        if PostTableAll.objects.filter(p_mid=mid):
            if PostTable.objects.filter(p_mid=mid):
                PostTable.objects.filter(p_mid=mid).delete()
            PostTableAll.objects.filter(p_mid=mid).delete()

        try:
            PostTableAll.objects.create(
                p_mid=i['tp_mid'],
                p_auther=i['tp_auther'],
                p_txt=i['tp_txt'],
                p_transmit=i['tp_transmit'],
                p_comment=i['tp_comment'],
                p_like=i['tp_like'],
                p_title=i['tp_title'],
                p_uid=i['tp_uid'],
            )
        except:
            pass


def save_PostTable():
    data_new = TimePostTable.objects.all().values()
    # print(data_new)

    count = 1
    count_all = len(data_new)

    for i in data_new:
        mid = i['tlp_mid']
        title = i['tlp_title']
        # print(mid)
        if PostTable.objects.filter(p_mid=mid):
            # print(mid)
            PostTable.objects.filter(p_mid=mid).delete()

        post_table_all_instance = PostTableAll.objects.get(p_mid=mid)  # 获取相关的PostTableAll实例
        topic_instance = TopicTable.objects.get(t_title=title)  # 获取相关的TopicTable实例

        try:
            PostTable.objects.create(
                p_mid=post_table_all_instance,
                p_auther=i['tlp_auther'],
                p_txt=i['tlp_txt'],
                p_transmit=i['tlp_transmit'],
                p_comment=i['tlp_comment'],
                p_like=i['tlp_like'],
                t_title=topic_instance,
                p_uid=i['tlp_uid'],
                p_birthday=i['tlp_birthday'],
                p_constellation=i['tlp_constellation'],
                p_created_at=i['tlp_created_at'],
                p_gender=i['tlp_gender'],
                p_location=i['tlp_location'],
                p_audence_id=i['tlp_audence_id'],
            )
        except:
            pass

        progress = round(count / count_all * 100, 2)
        print(progress)
        return_progress('chat_savePostProgress', progress, count == count_all)
        count += 1

def return_progress(chat_name, progress, flag):
    response = {
        'progress': progress,
        'flag': flag,
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        chat_name,
        {
            "type": "chat_message",
            "message": response
        }
    )









