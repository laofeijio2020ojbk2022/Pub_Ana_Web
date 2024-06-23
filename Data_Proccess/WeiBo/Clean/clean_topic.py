# 清洗微博热搜
# 原数据太多导致下一步爬取估计时间超过30小时，因此只使用100万热度以上的数据，爬取时间降到4小时左右
# 本步骤处理的数据仅用于下一步，通过热搜爬取热帖
# 保留所有热搜的清洗见clean_topic_2.py

import pandas as pd

df = pd.read_csv("../Data/add2/topic_add2.csv", header=None)
df.columns = ['title', 'label', 'time', 'host', 'continue', 'sort', 'hot']

df_6col = df[df['sort'] == 0]
df_6col[['continue', 'sort', 'hot']] = df_6col[['time', 'host', 'continue']]
df_6col['host'] = ""
df_6col[['time']] = df_6col[['label']]
df_6col['label'] = ""
# print(df_6col)

df = df.drop(df[df['sort'] == 0].index)
df = pd.concat([df, df_6col])

df_7col = df[df['hot'] == 0]
df_7col[['host', 'continue', 'sort', 'hot']] = df_7col[['time', 'host', 'continue', 'sort']]
df_7col['host'] = ""
for i in df_7col['label']:
    if len(i) == 23:
        df_7col = df_7col.drop(df_7col[df_7col['label'] == i].index)
# print(df_7col)

df = df.drop(df[df['hot'] == 0].index)
df = pd.concat([df, df_7col])

df = df.drop_duplicates()
df = df[df['hot'] > 1000000]

df['continue'] = df['continue'].fillna(0)
df['continue'] = df['continue'].astype('int')

df['sort'] = df['sort'].fillna(0)
df['sort'] = df['sort'].astype('int')

df['hot'] = df['hot'].fillna(0)
df['hot'] = df['hot'].astype('int')

df = df.reset_index(drop=True)
for i in range(len(df['time'])):
    df['time'][i] = df['time'][i][7:17]

for i in range(len(df['time'])):
    if df['time'][i] == '':
        # print(df['time'][i])
        df['time'][i] = df['host'][i][7:17]
        df['host'][i] = ''

print(df.shape[0])

df.to_csv("../Data/add2/topic_add2_2.csv", index=False, mode='w')



