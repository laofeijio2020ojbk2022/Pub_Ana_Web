# 清洗评论细节信息
# 数据来源detail.csv，数据存储comment.csv
# 暴力清洗

import numpy as np
import pandas as pd
import re


def read_one(page):

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

        num = 0
        audience_id = []
        like_counts = []
        screen_name = []
        location = []
        gender = []
        followers_count = []
        friends_count = []
        statuses_count = []
        text_raw = []

        # print(df['audience_detail'][i])
        detail = df['audience_detail'][i].split('"created_at"')
        for j in detail:
            turn = re.findall(',"user":{(.*?),"mid', j)
            if turn:
                num += 1
            for one in turn:
                audience_id.append(re.findall('"id":(.*?),"idstr"', one)[0])
                screen_name.append(re.findall('"screen_name":"(.*?)"', one)[0])
                location.append(re.findall('"location":"(.*?)"', one)[0])
                gender.append(re.findall('"gender":"(.*?)"', one)[0])
                followers_count.append(re.findall('"followers_count":(.*?),', one)[0])
                friends_count.append(re.findall('"friends_count":(.*?),', one)[0])
                statuses_count.append(re.findall('"statuses_count":(.*?),', one)[0])

            for kk in re.findall('like_count(.*?),', j):
                like_counts.append(kk.split(":")[1])

            # like_counts.extend(re.findall('like_count(.*?),', j))

            text_raw.extend(re.findall('"text":"(.*?)","disable_reply"', j))

        # print(num)
        # print(i)

        # print(len(audience_id))
        # print(len(like_counts))
        # print(len(screen_name))
        # print(len(location))
        # print(len(gender))
        # print(len(followers_count))
        # print(len(friends_count))
        # print(len(statuses_count))
        # print(len(text_raw))

        # print(audience_id)
        # print(like_counts)
        # print(screen_name)
        # print(location)
        # print(gender)
        # print(followers_count)
        # print(friends_count)
        # print(statuses_count)
        # print(text_raw)

        if num != len(like_counts) or num != len(text_raw):
            with open("../Data/add/comment_wrong.txt", "a") as f:
                f.write(str(df['mid'][i]) + '\n')
                f.write(str(df['uid'][i]) + '\n')
                f.write('failed:\t' + str(i) + '-' * 20 + '\n')
            # print(detail)
            # num = len(like_counts)
            continue  # 长度不一致提示bug，跳过

        df2 = pd.DataFrame([audience_id, like_counts, screen_name, location, gender,
                            followers_count, friends_count, statuses_count, text_raw]).transpose()
        df2.columns = ['audience_id', 'like_counts', 'screen_name', 'location', 'gender',
                       'followers_count', 'friends_count', 'statuses_count', 'text_raw']
        df2['mid'] = df['mid'][i]
        df2 = df2.dropna()
        df2 = df2.reset_index(drop=True)

        df2.to_csv("../Data/add/comment_add.csv", index=None, mode='a', header=None)

        # print(df2)


if __name__ == '__main__':
    k = 0
    while (k < 5000):
        df = pd.read_csv('../Data/add/detail_add.csv', header=None, skiprows=k, nrows=1000)
        df.columns = ['auther', 'auther_url', 'the_url', 'txt2', 'transmit', 'comment',
                      'like', 'title', 'uid', 'mid', 'auther_detail', 'audience_detail']

        df = df[['auther', 'txt2', 'transmit', 'comment', 'like', 'title', 'uid', 'mid',
                 'auther_detail', 'audience_detail']]
        df = df.dropna()
        df = df.reset_index(drop=True)
        read_one(len(df['auther']))

        k += 1000
        print(str(k - 1000 + len(df['auther'])) + "\tover" + "-" * 20)

        # break
