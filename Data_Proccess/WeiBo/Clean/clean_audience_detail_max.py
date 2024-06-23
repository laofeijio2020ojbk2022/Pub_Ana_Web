# 对comment.csv简单清洗
# 检查数据

import pandas as pd
import re
from string import punctuation

def clean_one(num):

    # print(df['text_raw'])
    for i in range(num):
        df['location'][i] = df['location'][i][0:2]

    for i in range(num):
        if df['gender'][i] == 'm':
            df['gender'][i] = 1
        elif df['gender'][i] == 'f':
            df['gender'][i] = 0
        # print(df['gender'][i])
    df['gender'] = df['gender'].astype('int64')

    df.to_csv('../Data/to_database/comment.csv', index=None, mode='a', header=None)


if __name__ == '__main__':
    k = 0
    while (k < 380000):
        df = pd.read_csv('../Data/add/comment_add_2.csv', header=None, skiprows=k, nrows=10000)
        df = df.dropna()
        df = df.reset_index(drop=True)

        df.columns = ['audience_id', 'like_counts', 'screen_name', 'location', 'gender',
                      'followers_count', 'friends_count', 'statuses_count', 'text_raw', 'mid']

        clean_one(df.shape[0])

        k += 10000
        print(str(k - 10000 + df.shape[0]) + "\tover" + "-" * 20)

        # break
