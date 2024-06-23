# 清洗热门帖子
# 保留所有有效数据

import pandas as pd
from Data_Proccess.WeiBo.Spider.new_math import id_to_mid
import re

# print(df.shape[0])
def clean_one(df2):
    # df2['transmit'] = df2['transmit'].astype('str')
    # df2['comment'] = df2['comment'].astype('str')
    # df2['like'] = df2['like'].astype('str')

    try:
        df2["transmit"] = df2["transmit"].str.strip()
        df2 = df2.drop(df2[df2['transmit'].str.contains(pat=r'[^0-9]+')].index)
        df2['transmit'] = df2['transmit'].astype('int')

        df2["comment"] = df2["comment"].str.strip()
        df2 = df2.drop(df2[df2['comment'].str.contains(pat=r'[^0-9]+')].index)
        df2['comment'] = df2['comment'].astype('int')

        df2["like"] = df2["like"].str.strip()
        df2 = df2.drop(df2[df2['like'].str.contains(pat=r'[^0-9]+')].index)
        df2['like'] = df2['like'].astype('float')
    except:
        pass

    # df = df[(df['transmit'] + df['comment'] + df['like']) > 10000]

    df2 = df2.reset_index(drop=True)
    df2['uid'] = ''
    for i in range(len(df2['auther_url'])):
        df2['uid'][i] = df2['auther_url'][i][12:22]

    df2['mid'] = ''
    for i in range(len(df2['the_url'])):
        # print(df2['the_url'][i])
        # print(re.findall(r'[0-9]+/(.*?)\?', df2['the_url'][i])[0])
        df2['mid'][i] = id_to_mid(re.findall(r'[0-9]+/(.*?)\?', df2['the_url'][i])[0])

    df2 = df2.drop(['auther_url', 'the_url'], axis=1)
    print(df2)

    df2.to_csv("../Data/to_database/post.csv", index=False, mode='a', header=None)


if __name__ == '__main__':
    k = 0
    while (k < 70000):
        df = pd.read_csv('../Data/add/post_add.csv', header=None, skiprows=k, nrows=10000)
        df.columns = ['auther', 'auther_url', 'the_url', 'txt2', 'transmit', 'comment', 'like', 'title']
        df = df.drop_duplicates()
        df = df.dropna()
        df = df.reset_index(drop=True)

        print(df.shape[0])

        clean_one(df)

        k += 10000
        print(str(k - 10000 + df.shape[0]) + "\tover" + "-" * 20)

        # break