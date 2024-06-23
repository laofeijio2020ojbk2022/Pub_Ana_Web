
import pandas as pd

df = pd.read_csv('../WeiBo/Data/to_database/post.csv')
df.columns = ['auther', 'txt2', 'transmit', 'comment', 'like', 'title', 'uid', 'mid']
df['like'] = df['like'].astype('int64')
for i in range(df.shape[0]):
    try:
        int(df['uid'][i])
    except:
        df['uid'][i] = df['uid'][i][0:-2]
        print(df['uid'][i])
df['uid'] = df['uid'].astype('int64')

print(df['like'][0])

print(df.dtypes)

