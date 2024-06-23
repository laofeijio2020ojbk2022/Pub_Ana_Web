import datetime

import browser_cookie3
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from crawler.models import CookiesTable, TimeTitleTable
from backend.models import TopicTable, CommentTable, PostTable, PostTableAll, TopicTableAll, UserTable
from crawler.new_math import get_ua
import numpy as np
import pandas as pd
import re
from datetime import date

# Create your views here.

@require_http_methods('GET')
def save_title(request):
    response = {}
    response['back'] = 'success'

    update_TopicTableAll()
    update_TopicTable()

    return JsonResponse(response)


def update_TopicTableAll():
    the_date = str(date.today())
    # the_date = '2024-05-17'
    # print(the_date)

    data_new = TimeTitleTable.objects.filter(ti_time=the_date).values()
    print(data_new)

    data_old = TopicTableAll.objects.filter(t_time=the_date).values()
    if data_old:
        TopicTableAll.objects.filter(
            t_time=the_date).delete()

    for i in data_new:
        # print(data_new['ti_title'])
        try:
            TopicTableAll.objects.create(
                t_title=i['ti_title'],
                t_label=i['ti_label'],
                t_hot=i['ti_hot'],
                t_time=i['ti_time'],
            )
        except:
            pass


def update_TopicTable():
    the_date = str(date.today())
    # the_date = '2024-05-17'
    # print(the_date)

    data_new = TimeTitleTable.objects.filter(ti_time=the_date).values()
    # print(data_new)

    data_old = TopicTable.objects.filter(t_time=the_date).values()
    if data_old:
        TopicTable.objects.filter(t_time=the_date).delete()

    for i in data_new:
        try:
            TopicTable.objects.create(
                t_title=i['ti_title'],
                t_label=i['ti_label'],
                t_hot=i['ti_hot'],
                t_time=i['ti_time'],
            )
        except:
            pass







