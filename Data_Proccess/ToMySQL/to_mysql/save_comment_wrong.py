import pandas as pd
import pymysql
import time
import numpy as np


def to_sql():
    col = ['c_audience_id', 'c_like_counts', 'c_screen_name', 'c_location', 'c_gender',
           'c_followers_count', 'c_friends_count', 'c_statuses_count', 'c_text_raw', 'c_mid']
    col = ','.join(col)
    with open("./comment_wrong.txt") as f:
        lines = f.readlines()
        for line in lines:
            row = line.split("),(")
            for i in row:
                try:
                    sql = "insert into comment_table ({}) values({})".format(col, i)
                    cursor.execute(sql)
                    db.commit()
                except:
                    print(sql)
                # print(1)
            # break


if __name__ == '__main__':

    # 打开数据库连接
    db = pymysql.connect(host='localhost', user='root', password='12345678', database='pub_ana_web')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    to_sql()

    cursor.close()
    db.close()

        # break
