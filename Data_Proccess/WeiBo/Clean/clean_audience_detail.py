# 清洗评论细节信息
# 数据来源detail.csv，数据存储comment.csv
# 数据太混乱了，结构不一致，解决办法详细见clean_audience_detail_2.py暴力清洗

import numpy as np
import pandas as pd
import re


def read_one(page):
    audience_id = []
    like_counts = []
    screen_name = []
    location = []
    gender = []
    followers_count = []
    friends_count = []
    statuses_count = []
    text_raw = []

    # "id":6587582020
    # "like_counts":6434 评论获赞
    # "screen_name":"雾川海盐泡甜俊"
    # "location":"宁夏 银川"
    # "gender": "f"
    # "followers_count": 2321 粉丝数
    # "friends_count": 330 关注数
    # "statuses_count": 7252 微博数
    # "text_raw": "图片评论 http://t.cn/A6lm2duJ"

    for i in range(page):
        # print(df['audience_detail'][i])

        turn = re.findall(',"user":{(.*?),"mid"', df['audience_detail'][i])
        for one in turn:
            audience_id.append(re.findall('"id":(.*?),"idstr"', one)[0])
            screen_name.append(re.findall('"screen_name":"(.*?)"', one)[0])
            location.append(re.findall('"location":"(.*?)"', one)[0])
            gender.append(re.findall('"gender":"(.*?)"', one)[0])
            followers_count.append(re.findall('"followers_count":(.*?),', one)[0])
            friends_count.append(re.findall('"friends_count":(.*?),', one)[0])
            statuses_count.append(re.findall('"statuses_count":(.*?),', one)[0])

        like_counts.extend(re.findall('like_counts":(.*?),"text_raw"', df['audience_detail'][i]))

        text_raw.extend(re.findall('[0-9]*,"text_raw":"(.*?)"', df['audience_detail'][i]))

        print(len(audience_id))
        if(len(audience_id) != len(text_raw)):
            print(df['mid'][i])
            print(df['uid'][i])
            print(i)
            break

        # break

    print(len(audience_id))
    print(len(like_counts))
    print(len(screen_name))
    print(len(location))
    print(len(gender))
    print(len(followers_count))
    print(len(friends_count))
    print(len(statuses_count))
    print(len(text_raw))

    # df2 = pd.DataFrame([audience_id, like_counts, screen_name, location, gender,
    #                     followers_count, friends_count, statuses_count, text_raw]).transpose()
    # print(df2)


if __name__ == '__main__':
    k = 0
    while (k < 13000):
        df = pd.read_csv('../Data/detail.csv', header=None, skiprows=k, nrows=1000)
        df.columns = ['auther', 'auther_url', 'the_url', 'txt2', 'transmit', 'comment',
                      'like', 'title', 'uid', 'mid', 'auther_detail', 'audience_detail']

        df = df[['auther', 'txt2', 'transmit', 'comment', 'like', 'title', 'uid', 'mid',
                 'auther_detail', 'audience_detail']]
        df = df.dropna()
        df = df.reset_index(drop=True)
        read_one(len(df['auther']))

        k += 1000
        print(str(k - 1000 + len(df['auther'])) + "\tover" + "-" * 20)

        break
