# 对comment.csv简单清洗
# 检查数据
# 数据保存到comment_2.csv

import pandas as pd
import re
from string import punctuation

def clean_one(num):
    for i in range(num):
        df['text_raw'][i] = re.sub('[{}a-zA-Z0-9 \\\\]'.format(punctuation), '', df['text_raw'][i])

    # print(df['text_raw'])
    df.to_csv('../Data/add/comment_add_2.csv', index=None, mode='a', header=None)

if __name__ == '__main__':
    k = 0
    while (k < 380000):
        df = pd.read_csv('../Data/add/comment_add.csv', header=None, skiprows=k, nrows=10000)
        df = df.dropna()
        df = df.reset_index(drop=True)

        df.columns = ['audience_id', 'like_counts', 'screen_name', 'location', 'gender',
                      'followers_count', 'friends_count', 'statuses_count', 'text_raw', 'mid']

        clean_one(df.shape[0])

        k += 10000
        print(str(k - 10000 + df.shape[0]) + "\tover" + "-" * 20)

        # break
