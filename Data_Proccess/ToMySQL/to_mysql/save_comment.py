import pandas as pd
import pymysql
import time
import numpy as np


def to_sql(num):
    try:
        value = []
        for i in range(num):
            the_sql = []
            for j in df:
                if type(df[j][i]) == type('a'):
                    the_sql.append("'" + df[j][i] + "'")
                elif np.isnan(df[j][i]):
                    the_sql.append("''")
                else:
                    the_sql.append(str(df[j][i]))
            the_sql = ','.join(the_sql)
            value.append(the_sql)
        value = '),('.join(value)

        sql = "insert into comment_table ({}) values({})".format(col, value)
        cursor.execute(sql)
        db.commit()
        # print(sql)
        # time.sleep(10)
    except:
        print("失败：\t" + str(k))
        with open("./comment_wrong.txt", "a") as f:
            f.write(value + "\n")
        # time.sleep(10)


if __name__ == '__main__':
    k = 0

    # 打开数据库连接
    db = pymysql.connect(host='localhost', user='root', password='12345678', database='pub_ana_web')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    while (k < 524000):
        df = pd.read_csv('../../WeiBo/Data/to_database/comment.csv', header=None, skiprows=k, nrows=1000)
        df = df.dropna()
        df = df.reset_index(drop=True)

        col = ['c_audience_id', 'c_like_counts', 'c_screen_name', 'c_location', 'c_gender',
               'c_followers_count', 'c_friends_count', 'c_statuses_count', 'c_text_raw', 'c_mid']
        df.columns = col

        col = ','.join(col)
        # print(col)

        to_sql(df.shape[0])

        k += 1000
        print(str(k - 1000 + df.shape[0]) + "\tover" + "-" * 20)

    cursor.close()
    db.close()

        # break
