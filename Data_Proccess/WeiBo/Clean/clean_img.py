# 清洗评论细节信息
# 数据来源detail.csv，数据存储comment.csv
# 暴力清洗

import numpy as np
import pandas as pd
import re

import requests


def read_one(page):

    img_url = []
    audience_id = []
    screen_name = []

    for i in range(page):
        detail = df['audience_detail'][i].split('"created_at"')
        for j in detail:
            turn = re.findall(',"user":{(.*?),"mid', j)
            for one in turn:
                audience_id.append(re.findall('"id":(.*?),"idstr"', one)[0])
                screen_name.append(re.findall('"screen_name":"(.*?)"', one)[0])
                img_url.append(re.findall('"profile_image_url":"(.*?)",', one)[0])

        # for k in range(len(audience_id)):
        #     r = requests.get(img_url[k])
        #     # print(r)
        #     with open(f'../../../Web_Construction/img/gnn_dataset/img_300/{audience_id[k]}_{screen_name[k]}.jpg', 'wb') as f:
        #         f.write(r.content)

        # break

    # print(len(audience_id))
    # print(len(screen_name))
    # print(len(img_url))
    df2 = pd.DataFrame([audience_id, screen_name, img_url]).transpose()
    df2.columns = ['audience_id', 'screen_name', 'img_url']
    df2 = df2.drop_duplicates(subset=['audience_id'])
    df2 = df2.reset_index(drop=None)
    print(df2.shape[0])

    for i in range(df2.shape[0]):
        print(i)
        r = requests.get(df2['img_url'][i])
        # print(r)
        with open(f'../../../Web_Construction/img/gnn_dataset/img_300/{df2["audience_id"][i]}_{df2["screen_name"][i]}.jpg', 'wb') as f:
            f.write(r.content)



if __name__ == '__main__':
    k = 0
    while (k < 13000):
        df = pd.read_csv('../Data/detail.csv', header=None, skiprows=k, nrows=300)
        df.columns = ['auther', 'auther_url', 'the_url', 'txt2', 'transmit', 'comment',
                      'like', 'title', 'uid', 'mid', 'auther_detail', 'audience_detail']

        df = df[['auther', 'audience_detail']]
        df = df.dropna()
        df = df.reset_index(drop=True)
        read_one(len(df['auther']))

        k += 300
        print(str(k - 300 + len(df['auther'])) + "\tover" + "-" * 20)

        break
