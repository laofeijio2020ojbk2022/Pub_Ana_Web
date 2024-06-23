# 清洗热门帖子
# 为节约时间，排除转发、评论、点赞之和小于10000的帖子
# 本步骤处理的数据仅用于下一步，通过热帖爬取评论
# 保留所有热帖的清洗见clean_post_2.py

import pandas as pd
from Data_Proccess.WeiBo.Spider.new_math import id_to_mid

df = pd.read_csv('../Data/add/post_add.csv', header=None)
df.columns = ['auther', 'auther_url', 'the_url', 'txt2', 'transmit', 'comment', 'like', 'title']
df = df.drop_duplicates()
df = df.dropna()

df["transmit"] = df["transmit"].str.strip()
df = df.drop(df[df['transmit'].str.contains(pat=r'[^0-9]+')].index)
df['transmit'] = df['transmit'].astype('int')

df["comment"] = df["comment"].str.strip()
df = df.drop(df[df['comment'].str.contains(pat=r'[^0-9]+')].index)
df['comment'] = df['comment'].astype('int')

df["like"] = df["like"].str.strip()
df = df.drop(df[df['like'].str.contains(pat=r'[^0-9]+')].index)
df['like'] = df['like'].astype('int')

df = df[(df['transmit'] + df['comment'] + df['like']) > 10000]

df = df.reset_index(drop=True)
df['uid'] = ''
for i in range(len(df['auther_url'])):
    df['uid'][i] = df['auther_url'][i][12:22]

df['mid'] = ''
for i in range(len(df['the_url'])):
    df['mid'][i] = id_to_mid(df['the_url'][i][23:32])

print(df)

df.to_csv("../Data/add/post_add_2.csv", index=False, mode='w')
