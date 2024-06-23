import browser_cookie3
import requests
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from crawler.models import CookiesTable, TimeTitleTable, TimePostTableAll, TimePostTable, TimeCommentTable
from crawler.new_math import get_ua, id_to_mid
import numpy as np
import pandas as pd
import re
from datetime import date
from lxml import etree, html
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from django.forms.models import model_to_dict


# Create your views here.


@require_http_methods(["GET"])
def get_detail(request):
    response = {}
    response['back'] = 'success'

    data = TimePostTableAll.objects.all().values()
    # print(data)
    df = pd.DataFrame(list(data))
    # print(df)
    df.columns = ['mid', 'auther', 'txt', 'transmit', 'comment', 'like', 'title', 'uid']
    df['birthday'] = ''
    df['constellation'] = ''
    df['created_at'] = ''
    df['gender'] = ''
    df['location'] = ''

    co_id = request.GET.get('id')
    # print(co_id)

    cookie = CookiesTable.objects.filter(co_id=co_id).values_list('co_cookie')[0][0]
    # print(cookie)

    get_detail2(df, cookie)

    return JsonResponse(response)


def get_detail2(df, cookie):
    headers = {
        'authority': 'weibo.com',
        'User-Agent': get_ua(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
        'Cookie': cookie
    }

    TimePostTable.objects.all().delete()
    TimeCommentTable.objects.all().delete()

    count = 1
    all_count = df.shape[0]

    for i in range(df.shape[0]):
    # for i in range(5):
        uid_url = 'https://weibo.com/ajax/profile/detail?uid=' + str(df['uid'][i])
        print(uid_url)

        uid_page = requests.get(uid_url, headers=headers).text
        # print(uid_page)

        auther_detail = clean_auther(uid_page)
        # print(auther_detail)

        df['birthday'] = auther_detail[0]
        df['constellation'] = auther_detail[1]
        df['created_at'] = auther_detail[2]
        df['gender'] = auther_detail[3]
        df['location'] = auther_detail[4]
        # for j in df:
        #     print(df[j][i])

        try:
            TimePostTable.objects.create(
                tlp_mid=df['mid'][i],
                tlp_auther=df['auther'][i],
                tlp_txt=df['txt'][i],
                tlp_transmit=df['transmit'][i],
                tlp_comment=df['comment'][i],
                tlp_like=df['like'][i],
                tlp_title=df['title'][i],
                tlp_uid=df['uid'][i],
                tlp_birthday=df['birthday'][i],
                tlp_constellation=df['constellation'][i],
                tlp_created_at=df['created_at'][i],
                tlp_gender=df['gender'][i],
                tlp_location=df['location'][i],
            )
        except:
            pass

        mid_url = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=' + \
                  str(df['mid'][i]) + '&is_show_bulletin=2&is_mix=0&count=10&uid=' + \
                  str(df['uid'][i]) + '&fetch_level=0&locale=zh-CN'
        print(mid_url)

        mid_page = requests.get(mid_url, headers=headers).text
        # print(mid_page)

        clean_audience(mid_page, df['mid'][i])

        progress = count / all_count
        print(progress)
        return_progress('chat_detailProgress', round(progress * 100, 2), count == all_count, df['title'][i])
        # print(progress)
        count += 1

        # break


def clean_auther(page):
    try:
        turn = re.findall('birthday":"(.*?)"', page)[0]
        # print(turn)
        if len(turn) == 14:
            birthday = turn[0:10]
            constellation = turn[11:]
        else:
            birthday = ''
            constellation = turn.strip()

        turn = re.findall('created_at":"(.*?)"', page)[0]
        created_at = turn[0:10]

        turn = re.findall('gender":"(.*?)"', page)[0]
        if turn == 'f':
            gender = 0
        elif turn == 'm':
            gender = 1

        turn = re.findall('location":"(.*?)"', page)[0]
        if turn[0:2] == 'IP':
            location = turn[5:7]
        else:
            location = turn[0:2]

        # turn = re.findall('"user":{"id":(.*?),"idstr"', page)
        # print(turn)
        # audience_id = ','.join(turn)
    except:
        birthday = ''
        constellation = ''
        created_at = ''
        gender = ''
        location = ''
        # audience_id = ''

    # print(birthday)
    # print(constellation)
    # print(created_at)
    # print(gender)
    # print(location)
    # print(audience_id)

    return [birthday, constellation, created_at, gender, location]


def clean_audience(page, mid):

    audience_id = []
    like_counts = []
    screen_name = []
    location = []
    gender = []
    followers_count = []
    friends_count = []
    statuses_count = []
    text_raw = []

    detail = page.split('"created_at"')
    for j in detail:
        turn = re.findall(',"user":{(.*?),"mid', j)
        for one in turn:
            audience_id.append(re.findall('"id":(.*?),"idstr"', one)[0])
            screen_name.append(re.findall('"screen_name":"(.*?)"', one)[0])
            location.append(re.findall('"location":"(.*?)"', one)[0][0:2])
            gender_flag = re.findall('"gender":"(.*?)"', one)[0]
            if gender_flag == 'f':
                gender.append(0)
            elif gender_flag == 'm':
                gender.append(1)
            followers_count.append(re.findall('"followers_count":(.*?),', one)[0])
            friends_count.append(re.findall('"friends_count":(.*?),', one)[0])
            statuses_count.append(re.findall('"statuses_count":(.*?),', one)[0])

        for kk in re.findall('like_count(.*?),', j):
            like_counts.append(kk.split(":")[1])

        # like_counts.extend(re.findall('like_count(.*?),', j))

        turn = re.findall('"text":"(.*?)","disable_reply"', j)
        for i in turn:
            text_raw.append(re.compile(r'[^\u4e00-\u9fff]').sub('', i))

    df2 = pd.DataFrame([audience_id, like_counts, screen_name, location, gender,
                        followers_count, friends_count, statuses_count, text_raw]).transpose()
    df2.columns = ['audience_id', 'like_counts', 'screen_name', 'location', 'gender',
                   'followers_count', 'friends_count', 'statuses_count', 'text_raw']
    df2['mid'] = mid

    # for i in df2:
    #     print(df2[i])

    # print(df2.shape[0])
    df2 = df2.dropna()
    df = df2.reset_index(drop=True)
    # print(df.shape[0])

    obj_list = []

    for j in range(df.shape[0]):
        obj = TimeCommentTable(
            tc_audience_id=df['audience_id'][j],
            tc_like_counts=df['like_counts'][j],
            tc_screen_name=df['screen_name'][j],
            tc_location=df['location'][j],
            tc_gender=df['gender'][j],
            tc_followers_count=df['followers_count'][j],
            tc_friends_count=df['friends_count'][j],
            tc_statuses_count=df['statuses_count'][j],
            tc_text_raw=df['text_raw'][j],
            tc_mid=df['mid'][j],
        )
        # print(obj)
        obj_list.append(obj)

    TimeCommentTable.objects.bulk_create(obj_list)


def return_progress(chat_name, progress, flag, data):

    response = {
        'progress': progress,
        'flag': flag,
        'data': data,
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        chat_name,
        {
            "type": "chat_message",
            "message": response
        }
    )











