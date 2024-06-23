import time
import pymysql
import pandas as pd
import numpy as np


def to_sql():
    try:
        sql = "insert into post_table_all ({}) values({})".format(col, the_sql)
        cursor.execute(sql)
        db.commit()
        # print(sql)
    except:
        print(sql)
        time.sleep(10)


if __name__ == '__main__':

    df = pd.read_csv('../../WeiBo/Data/to_database/post.csv')
    col = ['p_auther', 'p_txt', 'p_transmit', 'p_comment', 'p_like', 'p_title', 'p_uid', 'p_mid']
    df.columns = col
    df['p_like'] = df['p_like'].astype('int64')
    for i in range(df.shape[0]):
        try:
            int(df['p_uid'][i])
        except:
            df['p_uid'][i] = df['p_uid'][i][0:-2]
            print(df['p_uid'][i])
    df['p_uid'] = df['p_uid'].astype('int64')

    # print(df.dtypes)

    col = ','.join(col)
    # print(col)

    # 打开数据库连接
    db = pymysql.connect(host='localhost', user='root', password='12345678', database='pub_ana_web')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    for i in range(df.shape[0]):
        the_sql = []
        for j in df:
            if type(df[j][i]) == type('a'):
                the_sql.append("'" + df[j][i] + "'")
            elif np.isnan(df[j][i]):
                the_sql.append("''")
            else:
                the_sql.append(str(df[j][i]))
        the_sql = ','.join(the_sql)
        # print(the_sql)
        # print("insert into topic_table_all ({}) values({})".format(col, the_sql))

        to_sql()
        print(str(i) + '\tover' + '-' * 20)

    cursor.close()
    db.close()
