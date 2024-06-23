# 检查数据
# post去重

import pandas as pd
import re

# df = pd.read_csv('../Data/to_database/post.csv')
# df.columns = df.columns = ['auther', 'txt2', 'transmit', 'comment', 'like', 'title', 'uid', 'mid']
# print(df.shape[0])
# df = df.drop_duplicates(subset='mid')
# print(df.shape[0])
# df = df.reset_index(drop=True)
# for i in range(df.shape[0]):
#     df['txt2'][i] = df['txt2'][i].replace("'", " ")
# df.to_csv('../Data/to_database/post.csv', mode='w', index=None)

# df = pd.read_csv('../Data/to_database/topic.csv')
# df.columns = df.columns = ['title', 'label', 'time', 'host', 'continue', 'sort', 'hot']
# print(df.shape[0])
# df = df.drop_duplicates()
# print(df.shape[0])
#
# df.to_csv('../Data/to_database/topic.csv', mode='w', index=None)

# df = pd.read_csv('../Data/to_database/topic_index.csv')
# df.columns = df.columns = ['title', 'label', 'time', 'host', 'continue', 'sort', 'hot']
# print(df.shape[0])
# df = df.drop_duplicates(subset='title')
# print(df.shape[0])
# # df['host'] = df['host'].fillna('')
# # for i in range(len(df['time'])):
# #     df['host'][i] = re.sub('主持人：', '', df['host'][i])
# # df['time'][12310] = df['host'][12310][7:17]
# # df['host'][12310] = ''
# # print(df[12310:12311])
#
# df.to_csv('../Data/to_database/topic_index.csv', mode='w', index=None)

# df = pd.read_csv('../Data/to_database/detail.csv')
# df.columns = df.columns = ['auther', 'txt2', 'transmit', 'comment', 'like', 'title', 'uid', 'mid',
#                            'birthday', 'constellation', 'created_at', 'gender', 'location', 'audience_id']
# print(df.shape[0])
# df = df.drop_duplicates(subset='mid')
# df = df.reset_index(drop=True)
# print(df.shape[0])
# for i in range(df.shape[0]):
#     df['txt2'][i] = df['txt2'][i].replace("'", " ")
#
# for i in range(df.shape[0]):
#     if df['gender'][i] == 'm':
#         df['gender'][i] = 1
#     elif df['gender'][i] == 'f':
#         df['gender'][i] = 0
#     # print(df['gender'][i])
# df['gender'] = df['gender'].astype('int64')
#
# df.to_csv('../Data/to_database/detail.csv', mode='w', index=None)
#
# print(df.dtypes)

# df = pd.read_csv('../Data/to_database/comment.csv')
# df.columns = ['audience_id', 'like_counts', 'screen_name', 'location', 'gender',
#               'followers_count', 'friends_count', 'statuses_count', 'text_raw', 'mid']
# print(df.shape[0])
# # df = df.drop_duplicates(subset='mid')
# print(df.shape[0])
#
# # df.to_csv('../Data/to_database/detail.csv', mode='w', index=None)
#
# print(df.dtypes)
