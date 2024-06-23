# 对detail_2.csv简单清洗
# 检查数据

import pandas as pd

df = pd.read_csv('../Data/add/detail_add_2.csv', header=None)
df.columns = ['auther', 'txt2', 'transmit', 'comment', 'like', 'title', 'uid', 'mid', 'birthday',
              'constellation', 'created_at', 'gender', 'location', 'audience_id']
print(df.shape[0])
df = df.drop_duplicates(subset='mid')
print(df.shape[0])

df.to_csv('../Data/to_database/detail.csv', mode='a', index=None, header=None)