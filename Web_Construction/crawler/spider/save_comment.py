import datetime
import time

import browser_cookie3
import requests
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
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your views here.


@require_http_methods('GET')
def save_comment(request):
    response = {}
    response['back'] = 'success'


    save_CommentTable()

    return JsonResponse(response)


def save_CommentTable():
    tp_mid = TimePostTableAll.objects.all().values_list('tp_mid')
    tp_mid_list = [i[0] for i in tp_mid]
    # print(tp_mid_list)

    count = 1
    count_all = len(tp_mid_list)

    for j in tp_mid_list:
        data_now = TimeCommentTable.objects.filter(tc_mid=j).values()
        # print(len(data_now))

        mid = j
        if CommentTable.objects.filter(c_mid=mid):
            CommentTable.objects.filter(c_mid=mid).delete()

        try:
            comment_instance = PostTable.objects.get(p_mid=mid)
        except:
            comment_instance = ''

        # print(data_now)

        flag = False
        for i in data_now:
            try:
                CommentTable.objects.create(
                    c_audience_id=i['tc_audience_id'],
                    c_like_counts=i['tc_like_counts'],
                    c_screen_name=i['tc_screen_name'],
                    c_location=i['tc_location'],
                    c_gender=i['tc_gender'],
                    c_followers_count=i['tc_followers_count'],
                    c_friends_count=i['tc_friends_count'],
                    c_statuses_count=i['tc_statuses_count'],
                    c_text_raw=i['tc_text_raw'],
                    c_mid=comment_instance,
                )
            except:
                flag = True
                pass

        if flag:
            print(mid)

        progress = round(count / count_all * 100, 2)
        print(progress)
        return_progress('chat_saveCommentProgress', progress, count == count_all)
        count += 1

        # if count == 4:
        #     break


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






