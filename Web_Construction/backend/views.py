import math

import pandas as pd
from django.shortcuts import render

# Create your views here.

import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from backend.models import TopicTable, CommentTable, PostTable, PostTableAll, TopicTableAll, UserTable
from django.core import serializers


@require_http_methods(["GET"])
def test(request):
    response = {}
    try:
        response['back'] = request.GET.get('text')
        response['respMsg'] = 'success'
        response['respCode'] = '000000'
    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'
    return JsonResponse(response)
    # back = TopicTable.objects.filter(t_time='2023-12-31')
    # back = serializers.serialize("json", back)
    # print(type(HttpResponse(back)))
    # return HttpResponse(back)
    # back = TopicTable.objects.filter(t_time='2023-12-31')
    # back = serializers.serialize("json", back)
    # print(back)
    # return JsonResponse({'status': True, 'data': back})


def change_name(name):
    if name in ['北京', '天津', '上海', '重庆']:
        name = name + '市'
    elif name == '内蒙':
        name = '内蒙古自治区'
    elif name == '广西':
        name = '广西壮族自治区'
    elif name == '西藏':
        name = '西藏自治区'
    elif name == '宁夏':
        name = '宁夏回族自治区'
    elif name == '新疆':
        name = '新疆维吾尔自治区'
    elif name == '香港':
        name = '香港特别行政区'
    elif name == '澳门':
        name = '澳门特别行政区'
    elif name == '黑龙':
        name = '黑龙江省'
    elif name in ['河北', '台湾', '青海', '甘肃', '陕西', '云南', '贵州', '四川', '海南', '广东', '湖南', '湖北', '河南',
                  '山东', '江西', '福建', '安徽', '浙江', '江苏', '吉林', '辽宁', '山西']:
        name = name + '省'
    else:
        name = '海外'
    return name


from collections import Counter


@require_http_methods(["GET"])
def get_map_data(request):
    response = {}

    model = request.GET.get('model')
    time_start = request.GET.get('time_start')
    time_end = request.GET.get('time_end')
    province = request.GET.get('province')
    topic = request.GET.get('topic')

    title_list = []
    if topic == '':
        data = TopicTable.objects \
            .filter(t_time__lte=time_end, t_time__gte=time_start) \
            .values_list("t_title", "t_hot")
        for i in data:
            title_list.append(i[0])
    else:
        title_list.append(topic)
    # print(title_list)
    mid_list = []
    data2 = PostTable.objects \
        .filter(t_title__in=title_list) \
        .values_list("p_mid")
    for i in data2:
        mid_list.append(i[0])
    # print(mid_list)
    data3 = CommentTable.objects \
        .filter(c_mid__in=mid_list) \
        .values_list("c_location", "c_gender", "c_like_counts", "c_followers_count", "c_friends_count", "c_statuses_count")

    the_list = []
    male_list = []
    female_list = []
    if model == 'like':
        like_dict = {}
        like_dict_male = {}
        like_dict_female = {}
        for i in data3:
            try:
                like_dict[i[0]] += i[2]
            except:
                like_dict[i[0]] = 0
            if i[1] == 1:
                try:
                    like_dict_male[i[0]] += i[2]
                except:
                    like_dict_male[i[0]] = 0
            elif i[1] == 0:
                try:
                    like_dict_female[i[0]] += i[2]
                except:
                    like_dict_female[i[0]] = 0

        # print(like_dict)
        # print(like_dict_male)
        # print(like_dict_female)

        back1 = like_dict
        back2 = like_dict_male
        back3 = like_dict_female
    elif model == 'weight':
        like_dict = {}
        like_dict_male = {}
        like_dict_female = {}

        # followers_count = []
        # friends_count = []
        # statuses_count = []
        # for i in data3:
        #     followers_count.append(i[3])
        #     friends_count.append(i[4])
        #     statuses_count.append(i[5])
        # max1 = max(followers_count) + 1
        # max2 = max(friends_count) + 1
        # max3 = max(statuses_count) + 1

        for i in data3:
            try:
                # like_dict[i[0]] += (i[3]/max1 + i[4]/max2 + i[5]/max3) * 100
                like_dict[i[0]] += math.pow(i[3] + i[4] + i[5] + 1, 1/2)
            except:
                like_dict[i[0]] = 0
            if i[1] == 1:
                try:
                    # like_dict_male[i[0]] += (i[3]/max1 + i[4]/max2 + i[5]/max3) * 100
                    like_dict_male[i[0]] += math.pow(i[3] + i[4] + i[5] + 1, 1/2)
                except:
                    like_dict_male[i[0]] = 0
            elif i[1] == 0:
                try:
                    # like_dict_female[i[0]] += (i[3]/max1 + i[4]/max2 + i[5]/max3) * 100
                    like_dict_female[i[0]] += math.pow(i[3] + i[4] + i[5] + 1, 1/2)
                except:
                    like_dict_female[i[0]] = 0

        # print(like_dict)
        # print(like_dict_male)
        # print(like_dict_female)

        back1 = like_dict
        back2 = like_dict_male
        back3 = like_dict_female
    elif model == 'all':
        for i in data3:
            the_list.append(i[0])
            if i[1] == 1:
                male_list.append(i[0])
            elif i[1] == 0:
                female_list.append(i[0])
        back1 = Counter(the_list)
        back2 = Counter(male_list)
        back3 = Counter(female_list)

    back1 = [{'name': change_name(key), 'value': round(value, 1), 'position': get_position(key, 0)} for key, value in back1.items() if key != '其他']
    back2 = [{'name': change_name(key), 'value': round(value, 1), 'position': get_position(key, 1)} for key, value in back2.items() if key != '其他']
    back3 = [{'name': change_name(key), 'value': round(value, 1), 'position': get_position(key, 2)} for key, value in back3.items() if key != '其他']
    # print(back2)
    response['map'] = back1
    response['map2'] = {
        'male': back2,
        'female': back3,
    }

    return JsonResponse(response)


with open('machine/machine/center.json') as f:
    centerJSON = json.load(f)
def get_position(name, model):
    if model == 0:
        for i in centerJSON['data']:
            if i['name'][:2] == name:
                return i['position']
    elif model == 1:
        for i in centerJSON['data']:
            if i['name'][:2] == name:
                return [i['position'][0]-0.5, i['position'][1]]
    elif model == 2:
        for i in centerJSON['data']:
            if i['name'][:2] == name:
                return [i['position'][0]+0.5, i['position'][1]]

    return [0, 0]



@require_http_methods(["GET"])
def get_time_data(request):
    response = {}

    model = request.GET.get('model')
    time_start = request.GET.get('time_start')
    time_end = request.GET.get('time_end')
    province = request.GET.get('province')
    topic = request.GET.get('topic')

    male_dict = {}
    female_dict = {}
    df = pd.DataFrame(columns=['gender', 'like', 'follower', 'friend', 'status', 'id', 'name', 'location'])
    result1 = {}
    result2 = {}
    result3 = {}
    df_topic = pd.DataFrame(columns=['name', 'gender', 'value'])
    topic1 = []
    topic2 = []
    topic3 = []

    if topic == '':
        data = TopicTable.objects \
            .filter(t_time__lte=time_end, t_time__gte=time_start) \
            .values_list("t_title", "t_hot", "t_time")
    else:
        data = TopicTable.objects \
            .filter(t_title=topic) \
            .values_list("t_title", "t_hot", "t_time")

    for i in data:
        mid_list = []
        data2 = PostTable.objects \
            .filter(t_title=i[0]) \
            .values_list("p_mid")
        for j in data2:
            mid_list.append(j[0])
        # print(mid_list)
        if province == '':
            data3 = CommentTable.objects \
                .filter(c_mid__in=mid_list) \
                .values_list("c_gender", "c_like_counts", "c_followers_count", "c_friends_count", "c_statuses_count",
                             "c_audience_id", "c_screen_name", "c_location")
        else:
            data3 = CommentTable.objects \
                .filter(c_mid__in=mid_list, c_location=province[:2]) \
                .values_list("c_gender", "c_like_counts", "c_followers_count", "c_friends_count", "c_statuses_count",
                             "c_audience_id", "c_screen_name", "c_location")

        df2 = pd.DataFrame(list(data3),
                           columns=['gender', 'like', 'follower', 'friend', 'status', 'id', 'name', 'location'])
        # print(df2)
        df = pd.concat([df, df2])

        if model == 'like':
            for j in data3:
                if j[0] == 1:
                    try:
                        male_dict[i[2]] += j[1]
                    except:
                        male_dict[i[2]] = 0
                elif j[0] == 0:
                    try:
                        female_dict[i[2]] += j[1]
                    except:
                        female_dict[i[2]] = 0

            all_topic = []
            default_topic = {'name': i[0], 'gender': 'none', 'value': 0}
            try:
                all_topic.append({'name': i[0], 'gender': 'male', 'value': df2.groupby('gender')['like'].sum()[1]})
            except:
                all_topic.append(default_topic)
            try:
                all_topic.append({'name': i[0], 'gender': 'female', 'value': df2.groupby('gender')['like'].sum()[0]})
            except:
                all_topic.append(default_topic)
            try:
                all_topic.append({'name': i[0], 'gender': 'all', 'value': df2['like'].sum()})
            except:
                all_topic.append(default_topic)
            df_topic = pd.concat([df_topic, pd.DataFrame(all_topic)])
        elif model == 'weight':
            # try:
            #     max1 = max(df2['follower']) + 1
            # except:
            #     max1 = 1
            # try:
            #     max2 = max(df2['friend']) + 1
            # except:
            #     max2 = 1
            # try:
            #     max3 = max(df2['status']) + 1
            # except:
            #     max3 = 1

            for j in data3:
                if j[0] == 1:
                    try:
                        # male_dict[i[2]] += (j[2]/max1 + j[3]/max2 + j[4]/max3) * 100
                        male_dict[i[2]] += math.log(j[2] + j[3] + j[4] + 1, 10)
                    except:
                        male_dict[i[2]] = 0
                elif j[0] == 0:
                    try:
                        # female_dict[i[2]] += (j[2]/max1 + j[3]/max2 + j[4]/max3) * 100
                        female_dict[i[2]] += math.log(j[2] + j[3] + j[4] + 1, 10)
                    except:
                        female_dict[i[2]] = 0

            def calculate_data(group):
                result = group['follower'] + group['friend'] + group['status'] + 1
                result = result.apply(lambda x: math.pow(x, 1 / 2))
                return result.sum()

            all_topic = []
            try:
                male_value = df2.groupby('gender').apply(calculate_data)[1].sum()
            except:
                male_value = 0
            try:
                female_value = df2.groupby('gender').apply(calculate_data)[0].sum()
            except:
                female_value = 0

            all_topic.append({'name': i[0], 'gender': 'male', 'value': male_value})
            all_topic.append({'name': i[0], 'gender': 'female', 'value': female_value})
            all_topic.append({'name': i[0], 'gender': 'all', 'value': male_value + female_value})

            df_topic = pd.concat([df_topic, pd.DataFrame(all_topic)])
        elif model == 'all':
            for j in data3:
                if j[0] == 1:
                    try:
                        male_dict[i[2]] += 1
                    except:
                        male_dict[i[2]] = 0
                elif j[0] == 0:
                    try:
                        female_dict[i[2]] += 1
                    except:
                        female_dict[i[2]] = 0

            all_topic = []
            default_topic = {'name': i[0], 'gender': 'none', 'value': 0}
            try:
                all_topic.append({'name': i[0], 'gender': 'male', 'value': df2.groupby('gender')['like'].count()[1]})
            except:
                all_topic.append(default_topic)
            try:
                all_topic.append({'name': i[0], 'gender': 'female', 'value': df2.groupby('gender')['like'].count()[0]})
            except:
                all_topic.append(default_topic)
            try:
                all_topic.append({'name': i[0], 'gender': 'all', 'value': df2['like'].count()})
            except:
                all_topic.append(default_topic)
            df_topic = pd.concat([df_topic, pd.DataFrame(all_topic)])

    if model == 'like':
        def calculate_data(group):
            return (group['like']).sum()

        try:
            result1 = pd.Series(df.groupby('name').apply(calculate_data))
        except:
            pass
        try:
            result2 = pd.Series(df[df['gender'] == 1].groupby('name').apply(calculate_data))
        except:
            pass
        try:
            result3 = pd.Series(df[df['gender'] == 0].groupby('name').apply(calculate_data))
        except:
            pass
    elif model == 'weight':
        def calculate_data(group):
            return ((group['follower']/max1 + group['friend']/max2 + group['status']/max3) * 100).sum()

        max1 = max(df['follower']) + 1
        max2 = max(df['friend']) + 1
        max3 = max(df['status']) + 1

        try:
            result1 = pd.Series(df.groupby('name').apply(calculate_data))
        except:
            pass
        try:
            result2 = pd.Series(df[df['gender'] == 1].groupby('name').apply(calculate_data))
        except:
            pass
        try:
            result3 = pd.Series(df[df['gender'] == 0].groupby('name').apply(calculate_data))
        except:
            pass
    elif model == 'all':
        try:
            result1 = pd.Series(df.groupby('name').size())
        except:
            pass
        try:
            result2 = pd.Series(df[df['gender'] == 1].groupby('name').size())
        except:
            pass
        try:
            result3 = pd.Series(df[df['gender'] == 0].groupby('name').size())
        except:
            pass

    default_data = [{'name': '无', 'value': 0, 'info': {}}]
    try:
        result1 = [{'name': key, 'value': value, 'info': df[df['name'] == key].iloc[0].to_dict()} for key, value in result1.nlargest(10).round(1).items()]
    except:
        result1 = default_data
    try:
        result2 = [{'name': key, 'value': value, 'info': df[df['name'] == key].iloc[0].to_dict()} for key, value in result2.nlargest(10).round(1).items()]
    except:
        result2 = default_data
    try:
        result3 = [{'name': key, 'value': value, 'info': df[df['name'] == key].iloc[0].to_dict()} for key, value in result3.nlargest(10).round(1).items()]
    except:
        result3 = default_data

    back1 = [{'name': key, 'value': round(value, 1)} for key, value in male_dict.items()]
    back2 = [{'name': key, 'value': round(value, 1)} for key, value in female_dict.items()]

    df_topic['value'] = pd.to_numeric(df_topic['value'], errors='coerce')
    topic1 = df_topic[df_topic['gender'] == 'all'].nlargest(n=10, columns='value').to_dict(orient='records')
    topic2 = df_topic[df_topic['gender'] == 'male'].nlargest(n=10, columns='value').to_dict(orient='records')
    topic3 = df_topic[df_topic['gender'] == 'female'].nlargest(n=10, columns='value').to_dict(orient='records')

    response = {
        'male': back1,
        'female': back2,
        'sort': {
            'all': result1,
            'male': result2,
            'female': result3,
        },
        'topic': {
            'all': topic1,
            'male': topic2,
            'female': topic3,
        },
        'province': province,
        'title': topic,
        'time': [time_start, time_end],
    }
    print(response)

    return JsonResponse(response)


from datetime import datetime


def birth_to_age(birthdate):
    # 将生日字符串转换为日期对象
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    # 获取日期
    current_date = datetime.now()
    # 计算年龄
    age = current_date.year - birthdate.year - (
            (current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    return age


def age_to_group(age, reason):
    age = age // reason * reason
    if age >= 100:
        back = '99岁以上'
    else:
        back = str(age) + '-' + str(age + reason - 1) + '岁'
    return back


from wordcloud import WordCloud
import matplotlib.pyplot as plt


def get_word_cloud(data):
    # 将数据转换为词云所需的格式
    text = ' '.join([entry['name'] for entry in data])
    wordcloud = WordCloud(width=500, height=500, font_path='simsun.ttc', background_color=None, mode="RGBA") \
        .generate(text)
    # 显示词云图
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 隐藏坐标轴
    # plt.show()
    wordcloud.to_file("wordcloud.png")
    return


@require_http_methods(["GET"])
def get_map_data2(request):
    response = {}

    model = request.GET.get('model')
    time_start = request.GET.get('time_start')
    time_end = request.GET.get('time_end')
    province = request.GET.get('province')
    topic = request.GET.get('topic')

    title_list = []
    if topic == '':
        data = TopicTable.objects \
            .filter(t_time__lte=time_end, t_time__gte=time_start) \
            .values_list("t_title", "t_hot", "t_time")
        for i in data:
            title_list.append(i[0])
    else:
        data = TopicTable.objects \
            .filter(t_title=topic) \
            .values_list("t_title", "t_hot", "t_time")
        for i in data:
            title_list.append(i[0])
    if province != '':
        data2 = PostTable.objects.filter(t_title__in=title_list, p_location=province[:2]).values()
        data2 = pd.DataFrame(list(data2))
        data2.columns = ['mid', 'auther', 'txt', 'transmit', 'comment', 'like',
                         'title', 'uid', 'birthday', 'constellation', 'created_at',
                         'gender', 'location', 'audence_id']
    else:
        data2 = PostTable.objects.filter(t_title__in=title_list).values()
        data2 = pd.DataFrame(list(data2))
        data2.columns = ['mid', 'auther', 'txt', 'transmit', 'comment', 'like',
                         'title', 'uid', 'birthday', 'constellation', 'created_at',
                         'gender', 'location', 'audence_id']
    data4 = PostTable.objects.filter(t_title__in=title_list).values()
    data4 = pd.DataFrame(list(data4))
    data4.columns = ['mid', 'auther', 'txt', 'transmit', 'comment', 'like',
                     'title', 'uid', 'birthday', 'constellation', 'created_at',
                     'gender', 'location', 'audence_id']

    default_data = pd.Series({'无': 0})
    # print(default_data)

    data2['birthday'] = data2['birthday'].apply(lambda x: age_to_group(birth_to_age(x), 10) if x != '' else x)

    if model == 'like':
        def calculate_data(group):
            # max1 = max(group['transmit']) + 1
            # max2 = max(group['comment']) + 1
            # max3 = max(group['like']) + 1
            # return (group['transmit'] / max1 * 10 + group['comment'] / max2 * 50 + group['like'] / max3 * 100).sum()
            return (group['transmit'] * 10 + group['comment'] + group['like'] / 10).sum()

        location = data4.groupby('location').apply(calculate_data)
        location2 = data4[data4['gender'] == 1].groupby('location').apply(calculate_data)
        location3 = data4[data4['gender'] == 0].groupby('location').apply(calculate_data)

        title = data2.groupby('title').apply(calculate_data).nlargest(10)
        try:
            title2 = data2[data2['gender'] == 1].groupby('title').apply(calculate_data).nlargest(10)
        except:
            title2 = default_data
        try:
            title3 = data2[data2['gender'] == 0].groupby('title').apply(calculate_data).nlargest(10)
        except:
            title3 = default_data

        sort = data2.groupby('auther').apply(calculate_data).nlargest(10)
        try:
            sort2 = data2[data2['gender'] == 1].groupby('auther').apply(calculate_data).nlargest(10)
        except:
            sort2 = default_data
        try:
            sort3 = data2[data2['gender'] == 0].groupby('auther').apply(calculate_data).nlargest(10)
        except:
            sort3 = default_data

        birthday2 = data2[data2['gender'] == 1].groupby('birthday').apply(calculate_data)
        birthday3 = data2[data2['gender'] == 0].groupby('birthday').apply(calculate_data)
    elif model == 'all':
        location = data4.groupby('location').size()
        location2 = data4[data4['gender'] == 1].groupby('location').size()
        location3 = data4[data4['gender'] == 0].groupby('location').size()

        title = data2['title'].value_counts().nlargest(10)
        try:
            title2 = data2[data2['gender'] == 1].groupby('title').size().nlargest(10)
        except:
            title2 = default_data
        try:
            title3 = data2[data2['gender'] == 0].groupby('title').size().nlargest(10)
        except:
            title3 = default_data

        sort = data2['auther'].value_counts().nlargest(10)
        try:
            sort2 = data2[data2['gender'] == 1].groupby('auther').size().nlargest(10)
        except:
            sort2 = default_data
        try:
            sort3 = data2[data2['gender'] == 0].groupby('auther').size().nlargest(10)
        except:
            sort3 = default_data

        birthday2 = data2[data2['gender'] == 1].groupby('birthday').size()
        birthday3 = data2[data2['gender'] == 0].groupby('birthday').size()

    try:
        location = [{'name': change_name(key), 'value': round(value, 1), 'position': get_position(key, 0)} for key, value in location.items()]
        location = [item for item in location if item['name'] != '海外']
        # print(location)
        location2 = [{'name': change_name(key), 'value': round(value, 1), 'position': get_position(key, 1)} for key, value in location2.items()]
        location2 = [item for item in location2 if item['name'] != '海外']
        # print(location2)
        location3 = [{'name': change_name(key), 'value': round(value,1), 'position': get_position(key, 2)} for key, value in location3.items()]
        location3 = [item for item in location3 if item['name'] != '海外']
        # print(location3)
    except:
        location = []
        location2 = []
        location3 = []

    title = [{'name': key, 'value': value} for key, value in title.items()]
    title2 = [{'name': key, 'value': value} for key, value in title2.items()]
    title3 = [{'name': key, 'value': value} for key, value in title3.items()]

    sort = [{'name': key, 'value': round(value, 1), 'info': data2[data2['auther'] == key].iloc[0].to_dict()} for key, value in sort.items()]
    sort2 = [{'name': key, 'value': round(value, 1), 'info': data2[data2['auther'] == key].iloc[0].to_dict()} for key, value in sort2.items()]
    sort3 = [{'name': key, 'value': round(value, 1), 'info': data2[data2['auther'] == key].iloc[0].to_dict()} for key, value in sort3.items()]

    date2 = {}
    date3 = {}
    for i in data:
        try:
            data3 = PostTable.objects.filter(t_title=i[0]).values()
            data3 = pd.DataFrame(list(data3))
            data3.columns = ['mid', 'auther', 'txt', 'transmit', 'comment', 'like',
                             'title', 'uid', 'birthday', 'constellation', 'created_at',
                             'gender', 'location', 'audence_id']
            if model == 'all':
                for j in range(data3.shape[0]):
                    if data3['gender'][j] == 1:
                        try:
                            date2[i[2]] += 1
                        except:
                            date2[i[2]] = 0
                    elif data3['gender'][j] == 0:
                        try:
                            date3[i[2]] += 1
                        except:
                            date3[i[2]] = 0
            elif model == 'like':
                max1 = max(data3['transmit']) + 1
                max2 = max(data3['comment']) + 1
                max3 = max(data3['like']) + 1
                for j in range(data3.shape[0]):
                    if data3['gender'][j] == 1:
                        try:
                            date2[i[2]] += data3['transmit'][j]/max1*10 + data3['comment'][j]/max2*50 + data3['like'][j]/max3*100
                        except:
                            date2[i[2]] = 0
                    elif data3['gender'][j] == 0:
                        try:
                            date3[i[2]] += data3['transmit'][j]/max1*10 + data3['comment'][j]/max2*50 + data3['like'][j]/max3*100
                        except:
                            date3[i[2]] = 0
        except:
            pass

    date2 = [{'name': key, 'value': round(value, 1)} for key, value in date2.items()]
    date3 = [{'name': key, 'value': round(value, 1)} for key, value in date3.items()]

    # birthday2 = [{'name': key, 'value': value} for key, value in birthday2.items() if key != '']
    # birthday3 = [{'name': key, 'value': value} for key, value in birthday3.items() if key != '']
    birthday_2 = []
    birthday_3 = []
    for i in ['0-9岁', '10-19岁', '20-29岁', '30-39岁', '40-49岁', '50-59岁', '60-69岁', '70-79岁', '80-89岁', '90-99岁', '99岁以上']:
        flag1 = False
        flag2 = False
        for key, value in birthday2.items():
            if key == i:
                flag1 = True
                birthday_2.append({'name': i, 'value': value})
                break
        for key, value in birthday3.items():
            if key == i:
                flag2 = True
                birthday_3.append({'name': i, 'value': value})
                break
        if not flag1:
            birthday_2.append({'name': i, 'value': 0})
        if not flag2:
            birthday_3.append({'name': i, 'value': 0})


    response = {
        'map': {
            'all': location,
            'male': location2,
            'female': location3,
        },
        'date': {
            'male': date2,
            'female': date3,
        },
        'title': {
            'all': title,
            'male': title2,
            'female': title3,
        },
        'sort': {
            'all': sort,
            'male': sort2,
            'female': sort3,
        },
        'age': {
          'male': birthday_2,
          'female': birthday_3,
        },
        'time': [time_start, time_end],
        'province': province,
    }

    print(response)

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_title(request):
    response = {}
    time_start = request.GET.get('time_start')
    time_end = request.GET.get('time_end')

    the_list = []
    data = TopicTable.objects \
        .filter(t_time__lte=time_end, t_time__gte=time_start) \
        .values_list("t_title", "t_label", "t_time", "t_hot", "t_host", "t_continue", "t_hot")
    data = [{'title': i[0], 'label': i[1], 'time': i[2], 'hot': i[3], 'host': i[4], 'continue': i[5], 'hot': i[6]} for i
            in data]
    # print(data)

    return JsonResponse(data, safe=False)


def emo_analysis(data):
    from snownlp import SnowNLP
    positive = 0
    negative = 0
    neutral = 0
    s = SnowNLP(data)
    for i in s.sentences:
        ss = SnowNLP(i)
        if ss.sentiments > 0.7:
            positive += 1
        elif ss.sentiments < 0.3:
            negative += 1
        else:
            neutral += 1
    return [positive, neutral, negative]


@require_http_methods(["GET"])
def get_emotion(request):
    response = {}
    titles = request.GET.get('titles')
    titles = titles.split(', ')
    # print(titles)

    data = PostTableAll.objects \
        .filter(p_title__in=titles) \
        .values_list("p_txt")

    txt_list = []
    for i in data:
        txt_list.append(i[0])
    txt = '。'.join(txt_list)
    # print(txt)
    emo_count = emo_analysis(txt)
    emo_result = (emo_count[0] * 0.85 + emo_count[1] * 0.5 + emo_count[2] * 0.15 + 1) / (sum(emo_count) + 1)
    emo_result = round(emo_result, 2)
    # print(emo_count)
    # print(emo_result)

    mid_list = []
    data2 = PostTable.objects \
        .filter(t_title__in=titles) \
        .values_list("p_mid")
    for i in data2:
        mid_list.append(i[0])
    # print(mid_list)
    data3 = CommentTable.objects \
        .filter(c_mid__in=mid_list) \
        .values_list("c_text_raw")
    txt_list = []
    for i in data3:
        txt_list.append(i[0])
    txt = '。'.join(txt_list)
    # print(txt)
    emo_count2 = emo_analysis(txt)
    emo_result2 = (emo_count2[0] * 0.85 + emo_count2[1] * 0.5 + emo_count2[2] * 0.15 + 1) / (sum(emo_count2) + 1)
    emo_result2 = round(emo_result2, 2)
    # print(emo_count2)
    # print(emo_result2)

    emo1 = {'emo1': [{'name': '积极', 'value': emo_count[0]},
                     {'name': '一般', 'value': emo_count[1]},
                     {'name': '消极', 'value': emo_count[2]}],
            'result1': [{'name': '开心', 'value': emo_result},
                        {'name': '难过', 'value': round(1 - emo_result, 2)}]
            }
    emo2 = {'emo2': [{'name': '积极', 'value': emo_count2[0]},
                     {'name': '一般', 'value': emo_count2[1]},
                     {'name': '消极', 'value': emo_count2[2]}],
            'result2': [{'name': '开心', 'value': emo_result2},
                        {'name': '难过', 'value': round(1 - emo_result2, 2)}]
            }

    back = {'data1': emo1, 'data2': emo2}
    print(back)
    return JsonResponse(back, safe=False)


def part_analysis(data, name):
    # print(data)
    import jieba
    mytext = " ".join(jieba.cut(data)).split(" ")
    the_list = []
    for i in mytext:
        if (len(i) > 1):
            the_list.append(i)

    text = ' '.join(the_list)

    wordcloud = WordCloud(width=500, height=500, font_path='simsun.ttc', background_color=None, mode="RGBA") \
        .generate(text)
    # 显示词云图
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 隐藏坐标轴
    # plt.show()
    wordcloud.to_file(name)

    return


@require_http_methods(["GET"])
def get_participle(request):
    response = {}
    titles = request.GET.get('titles')
    titles = titles.split(', ')
    # print(titles)

    data = PostTableAll.objects \
        .filter(p_title__in=titles) \
        .values_list("p_txt")

    txt_list = []
    for i in data:
        txt_list.append(i[0])
    txt = '。'.join(txt_list)
    # print(txt)
    part_analysis(txt.replace(" ", ""), "the_wordcloud1.png")

    mid_list = []
    data2 = PostTable.objects \
        .filter(t_title__in=titles) \
        .values_list("p_mid")
    for i in data2:
        mid_list.append(i[0])
    # print(mid_list)
    data3 = CommentTable.objects \
        .filter(c_mid__in=mid_list) \
        .values_list("c_text_raw")
    txt_list = []
    for i in data3:
        txt_list.append(i[0])
    txt = '。'.join(txt_list)
    # print(txt)
    part_analysis(txt.replace(" ", ""), "the_wordcloud2.png")

    return JsonResponse(response, safe=False)


@require_http_methods(["POST"])
def get_register(request):
    response = {}
    response['back'] = 'success'
    data = json.loads(request.body)
    name = data.get('name')
    password = data.get('pass')
    print(name)
    print(password)
    try:
        UserTable.objects.create(u_name=name, u_password=password, u_admin=0)
    except:
        response['back'] = 'failed'

    return JsonResponse(response)


@require_http_methods(["POST"])
def get_login(request):
    response = {}
    response['back'] = 'success'
    data = json.loads(request.body)
    name = data.get('name')
    password = data.get('pass')
    # print(name)
    try:
        data = UserTable.objects.filter(u_name=name)\
            .values_list('u_id', 'u_name', 'u_password', 'u_sex', 'u_birth', 'u_txt', 'u_admin')[0]
        # print(data)
        password2 = data[1]
        if password == password2:
            response['back'] = 'success'
        else:
            response['back'] = 'wrong pass'
        response['data'] = {
            'id': data[0],
            'name': data[1],
            'password': data[2],
            'sex': data[3],
            'birth': data[4],
            'txt': data[5],
            'admin': data[6]
        }
    except:
        response['back'] = 'no user'

    return JsonResponse(response)


@require_http_methods(["POST"])
def change_user(request):
    response = {}
    data = json.loads(request.body)
    print(data)
    try:
        UserTable.objects.filter(u_id=data.get('id')).update(
            u_name=data.get('name'),
            u_password=data.get('password'),
            u_sex=data.get('sex'),
            u_birth=data.get('birth'),
            u_txt=data.get('txt'),
            u_admin=data.get('admin')
        )
        response['back'] = 'success'
    except:
        response['back'] = 'failed'

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_user(request):
    response = {}
    u_id = request.GET.get('id')
    # print(text)
    if u_id == '':
        data = list(UserTable.objects.filter().values())
        # print(data)
        response['value'] = data
    else:
        data = list(UserTable.objects.filter(u_id=u_id).values())
        # print(data)
        response['value'] = data

    response['back'] = 'success'

    return JsonResponse(response)


@require_http_methods(["GET"])
def delete_user(request):
    response = {}
    u_id = request.GET.get('u_id')
    print(u_id)
    try:
        data = UserTable.objects.get(u_id=u_id)
        data.delete()
        response['back'] = 'success'
    except:
        response['back'] = 'failed'

    return JsonResponse(response)
















