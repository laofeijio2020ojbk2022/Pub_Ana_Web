import browser_cookie3
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from crawler.models import CookiesTable, TimeTitleTable
from crawler.new_math import get_ua
import numpy as np
import pandas as pd
import re
from datetime import date

# Create your views here.

@require_http_methods(["GET"])
def get_title(request):
    response = {}
    response['back'] = 'success'

    co_id = request.GET.get('id')
    # print(co_id)

    cookie = CookiesTable.objects.filter(co_id=co_id).values_list('co_cookie')[0][0]
    # print(cookie)

    data = get_title2(cookie)

    response['data'] = data

    return JsonResponse(response)


def get_title2(cookie):
    headers = {
        'authority': 'weibo.com',
        'User-Agent': get_ua(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
        'Cookie': cookie
    }

    url = 'https://weibo.com/ajax/side/hotSearch'
    # 文娱榜只是根据娱乐圈热度排序，这里不要了
    # url2 = 'https://weibo.com/ajax/statuses/entertainment'

    page = requests.get(url, headers=headers).text
    # print(page)

    data = clean_page(page)

    return data

def clean_page(page):
    # print(page)

    title_list = []
    hot_list = []
    label_list = []
    obj_list = []

    part = page.split('},{')
    # print(len(part))

    for i in part:
        try:
            title = re.findall('word_scheme":"(.*?)"', i)[0].strip('#')
            # print(title)
            title_list.append(title)
        except:
            title_list.append(np.NAN)

        try:
            hot = re.findall('num":(.*?),', i)[0]
            # print(hot)
            hot_list.append(hot)
        except:
            hot_list.append(np.NAN)

        try:
            label = re.findall('category":"(.*?)"', i)[0]
            # print(label)
            label_list.append(label)
        except:
            label_list.append(np.NAN)

    # print(title_list)
    # print(hot_list)
    # print(label_list)

    df = pd.DataFrame([title_list, label_list, hot_list]).transpose()
    df.columns = ['title', 'label', 'hot']

    df['title'] = df['title'].str.strip()
    df['title'] = np.where(df['title'].str.strip() == '', np.NAN, df['title'])
    df = df.dropna(subset=['title', 'hot'])
    # df = df.drop_duplicates(subset=['title'])
    df = df.reset_index(drop=True)

    df['time'] = str(date.today())
    # df['time'] = '2024-05-17'

    for i in range(df.shape[0]):
        obj = TimeTitleTable(
            ti_title=df['title'][i],
            ti_label=df['label'][i],
            ti_hot=df['hot'][i],
            ti_time=df['time'][i]
        )
        # print(obj)
        obj_list.append(obj)

    # print(obj_list)

    TimeTitleTable.objects.all().delete()
    TimeTitleTable.objects.bulk_create(obj_list)

    return df.to_dict(orient='records')










