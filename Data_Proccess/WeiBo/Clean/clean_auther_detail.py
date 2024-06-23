# 清洗作者细节信息
# 数据来源detail.csv，数据存储detail_2.csv

import numpy as np
import pandas as pd
import re

def read_one(page):

    birthday = []
    constellation = []
    created_at = []
    gender = []
    location = []
    audience_id = []

    # "birthday":"2014-04-06 白羊座"
    # "created_at":"2014-04-06 01:07:14"
    # "gender":"m"
    # "ip_location": "IP属地：浙江"；"location":"江苏"

    for i in range(page):
        try:
            # print(df['auther_detail'][i])
            turn = re.findall('birthday":"(.*?)"', df['auther_detail'][i])[0]
            # print(turn)
            if len(turn) == 14:
                birthday.append(turn[0:10])
                constellation.append(turn[11:])
            else:
                birthday.append('')
                constellation.append(turn.strip())

            turn = re.findall('created_at":"(.*?)"', df['auther_detail'][i])[0]
            created_at.append(turn[0:10])

            turn = re.findall('gender":"(.*?)"', df['auther_detail'][i])[0]
            gender.append(turn)

            turn = re.findall('location":"(.*?)"', df['auther_detail'][i])[0]
            if turn[0:2] == 'IP':
                location.append(turn[5:7])
            else:
                location.append(turn[0:2])

            turn = re.findall('"user":{"id":(.*?),"idstr"', df['audience_detail'][i])
            # print(df['audience_detail'][i])
            # print(turn)
            audience_id.append(','.join(turn))
        except:
            birthday.append(np.NAN)
            constellation.append(np.NAN)
            created_at.append(np.NAN)
            gender.append(np.NAN)
            location.append(np.NAN)
            audience_id.append(np.NAN)
            # print(birthday[i])

    # print(len(birthday))
    # print(len(constellation))
    # print(created_at)
    # print(gender)
    # print(location)
    # print((audience_id))

    df2 = pd.DataFrame([birthday, constellation, created_at, gender, location, audience_id]).transpose()
    df2.columns = ['birthday', 'constellation', 'created_at', 'gender', 'location', 'audience_id']
    # print(df2)
    for i in df2:
        df[i] = df2[i]
    df2 = df.drop(columns=['auther_detail', 'audience_detail'])
    df2 = df2.dropna()
    df2 = df2.reset_index(drop=True)
    print(df2)
    df2.to_csv("../Data/add/detail_add_2.csv", mode='a', header=None, index=None)

if __name__ == '__main__':
    k = 0
    while(k < 5000):
        df = pd.read_csv('../Data/add/detail_add.csv', header=None, skiprows=k, nrows=1000)
        df.columns = ['auther', 'auther_url', 'the_url', 'txt2', 'transmit', 'comment',
                      'like', 'title', 'uid', 'mid', 'auther_detail', 'audience_detail']

        df = df[['auther', 'txt2', 'transmit', 'comment', 'like', 'title', 'uid', 'mid', 'auther_detail',
                 'audience_detail']]
        df = df.dropna()
        df = df.reset_index(drop=True)
        read_one(len(df['auther']))

        k += 1000
        print(str(k-1000+len(df['auther'])) + "\tover" + "-"*20)









