# 清洗微博热搜
# 保留所有有效数据

import pandas as pd
import re

def clean_one(df2):
    # 处理只有6行的数据
    df_6col = df2[df2['sort'] == 0]
    df_6col[['continue', 'sort', 'hot']] = df_6col[['time', 'host', 'continue']]
    df_6col['host'] = ""
    df_6col[['time']] = df_6col[['label']]
    df_6col['label'] = ""
    # print(df_6col)

    df2 = df2.drop(df2[df2['sort'] == 0].index)
    df2 = pd.concat([df2, df_6col])

    # 处理只有7行的数据
    df_7col = df2[df2['hot'] == 0]
    df_7col[['host', 'continue', 'sort', 'hot']] = df_7col[['time', 'host', 'continue', 'sort']]
    df_7col['host'] = ""
    for i in df_7col['label']:
        if len(i) == 23:
            df_7col = df_7col.drop(df_7col[df_7col['label'] == i].index)
    # print(df_7col)

    df2 = df2.drop(df2[df2['hot'] == 0].index)
    df2 = pd.concat([df2, df_7col])

    # 删除重复行
    df2 = df2.drop_duplicates()
    df2 = df2[df2['hot'] > 1000000]
    print(df2.shape[0])

    # 改变数据类型
    df2['continue'] = df2['continue'].fillna(0)
    df2['continue'] = df2['continue'].astype('int')
    df2['sort'] = df2['sort'].fillna(0)
    df2['sort'] = df2['sort'].astype('int')
    df2['hot'] = df2['hot'].fillna(0)
    df2['hot'] = df2['hot'].astype('int')

    # 其他bug
    df2 = df2.reset_index(drop=True)
    for i in range(len(df2['time'])):
        df2['time'][i] = df2['time'][i][7:17]

    for i in range(len(df2['time'])):
        if len(df2['time'][i]) < 5:
            # print(df['time'][i])
            df2['time'][i] = df2['host'][i][7:17]
            df2['host'][i] = ''

    for i in range(len(df2['time'])):
        df2['host'][i] = re.sub('主持人：', '', df2['host'][i])

    print(df2)
    # print(df2.dtypes)

    df2.to_csv("../Data/to_database/topic_add3.csv", index=False, mode='a', header=None)




if __name__ == '__main__':
    k = 0
    while (k < 60000):
        df = pd.read_csv('../Data/add2/topic_add2.csv', header=None, skiprows=k, nrows=10000)
        df = df.dropna()
        df = df.reset_index(drop=True)

        df.columns = ['title', 'label', 'time', 'host', 'continue', 'sort', 'hot']

        clean_one(df)

        k += 10000
        print(str(k - 10000 + df.shape[0]) + "\tover" + "-" * 20)

        # break

