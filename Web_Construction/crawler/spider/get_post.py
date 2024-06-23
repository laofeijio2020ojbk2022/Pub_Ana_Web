import browser_cookie3
import requests
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from crawler.models import CookiesTable, TimeTitleTable, TimePostTableAll
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
def get_post(request):
    response = {}
    response['back'] = 'success'

    data = TimeTitleTable.objects.all().values_list('ti_title')
    # print(data)

    title_list = []
    for i in data:
        title_list.append(i[0])
    # print(title_list)

    co_id = request.GET.get('id')
    # print(co_id)

    cookie = CookiesTable.objects.filter(co_id=co_id).values_list('co_cookie')[0][0]
    # print(cookie)

    get_post2(title_list, cookie)

    return JsonResponse(response)


def get_post2(title_list, cookie):
    headers = {
        'authority': 'weibo.com',
        'User-Agent': get_ua(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
        'Cookie': cookie
    }

    df = pd.DataFrame(columns=['auther', 'txt2', 'transmit', 'comment', 'like', 'title', 'uid', 'mid'])
    # print(df)

    count = 1
    all_count = len(title_list)

    TimePostTableAll.objects.all().delete()

    for i in title_list:
        # print(i)
        url = 'https://s.weibo.com/weibo?q=%23' + i + '%23&xsort=hot&Refer=hotmore'
        # print(url)

        page = requests.get(url, headers=headers).text
        page = html.fromstring(page)
        # print(page)

        auther = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "info")]/div[2]/a/text()')
        # print(auther)
        auther_url = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "info")]/div[2]/a/@href')
        # print(auther_url)
        the_url = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "from")]/a[1]/@href')
        # print(len(the_url))
        txt2 = []
        for txt in page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "content")]/p[1]'):
            txt2.append("".join(txt.xpath('text()')).strip())
        # print(len(txt2))
        # for j in txt2:
        #     print(j)
        transmit = page.xpath(
            '//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "card-act")]/ul/li[1]/a/text()[2]')
        # print(transmit)
        comment = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "card-act")]/ul/li[2]/a/text()')
        # print(comment)
        like = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "woo-like-count")]/text()')
        # print(like)

        the_df = pd.DataFrame([auther, auther_url, the_url, txt2, transmit, comment, like]).transpose()
        the_df.columns = ['auther', 'auther_url', 'the_url', 'txt2', 'transmit', 'comment', 'like']
        the_df['title'] = i
        # print(the_df)

        the_df = the_df.dropna()
        the_df = the_df.reset_index(drop=True)

        # print(the_df)

        df = clean_post(the_df)
        # df = pd.concat([df, clean_post(the_df)], axis=0)

        progress = count / all_count
        # print(progress)
        return_progress('chat_postProgress', round(progress * 100, 2), count == all_count, df.to_dict(orient='records'))
        # print(progress)
        count += 1
        print(progress)

        try:
            obj_list = []

            for j in range(df.shape[0]):
                obj = TimePostTableAll(
                    tp_mid=df['mid'][j],
                    tp_auther=df['auther'][j],
                    tp_txt=re.compile(r'[^\u4e00-\u9fff]').sub('', df['txt2'][j]),
                    tp_transmit=df['transmit'][j],
                    tp_comment=df['comment'][j],
                    tp_like=df['like'][j],
                    tp_title=df['title'][j],
                    tp_uid=df['uid'][j],
                )
                # print(obj)
                obj_list.append(obj)

            TimePostTableAll.objects.bulk_create(obj_list)
        except:
            for j in range(df.shape[0]):
                try:
                    TimePostTableAll.objects.bulk_create([obj_list[j]])
                except:
                    pass
                    # row = df.iloc[j]
                    # row.to_csv('error.csv', index=False, mode='a')
                    # print(df['txt2'][j])
            # break

        # if count == 8:
        #     break

    # print(df)


def clean_post(df2):
    try:
        df2["transmit"] = df2["transmit"].str.strip()
        df2 = df2.drop(df2[df2['transmit'].str.contains(pat=r'[^0-9]+')].index)
        df2['transmit'] = df2['transmit'].astype('int')

        df2["comment"] = df2["comment"].str.strip()
        df2 = df2.drop(df2[df2['comment'].str.contains(pat=r'[^0-9]+')].index)
        df2['comment'] = df2['comment'].astype('int')

        df2["like"] = df2["like"].str.strip()
        df2 = df2.drop(df2[df2['like'].str.contains(pat=r'[^0-9]+')].index)
        df2['like'] = df2['like'].astype('int')
    except:
        pass

    df2 = df2.reset_index(drop=True)
    # print(df2)

    df2['uid'] = ''
    for i in range(df2.shape[0]):
        # print(df2['auther_url'][i])
        df2['uid'][i] = re.findall(r'weibo.com/(.*?)\?', df2['auther_url'][i])[0]

    df2['mid'] = ''
    for i in range(df2.shape[0]):
        # print(df2['the_url'][i])
        # print(re.findall(r'[0-9]+/(.*?)\?', df2['the_url'][i])[0])
        df2['mid'][i] = id_to_mid(re.findall(r'[0-9]+/(.*?)\?', df2['the_url'][i])[0])

    df2 = df2.drop(['auther_url', 'the_url'], axis=1)
    # for i in df2:
    #     print(df2[i])

    return df2


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
    # async_to_sync(channel_layer.close())
    # async_to_sync(channel_layer.group_discard)("chat_postProgress", "channel_name")

    # response = {}
    # response['data'] = i
    # response['back'] = 'success'
    #
    # return JsonResponse(response)
