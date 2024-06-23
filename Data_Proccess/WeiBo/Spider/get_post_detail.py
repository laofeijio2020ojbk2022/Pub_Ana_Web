# 已经获取了热门帖子post_2.csv，通过记录的两个url增加热门帖子的详细内容
# 采用多线程爬虫，耗时8小时左右，运行需谨慎！！！

import random
import time
import requests
import pandas as pd
from Data_Proccess.WeiBo.Spider.new_math import get_ua
import threading

df = pd.read_csv('../Data/add/post_add_2.csv')

df['auther_detail'] = ''
df['audience_detail'] = ''


def fetch(a):
    try:
        headers = {
            'User-Agent': get_ua(),
            'authority': 's.weibo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
            'Cookie': 'SCF=AqD86_2GgPKMnksxd_CPrP5KUvDmij-I9LNg0Tq5SdBUlgXGc3HBi4JISUtN2ZNt-To5i444fFIRB8-lQtH7bF4.; SINAGLOBAL=8141950821074.444.1706926835159; UOR=,,www.zhaoyizhe.com; ALF=1714029912; SUB=_2A25LBggIDeRhGeFL7VUS9C7KzD2IHXVoegXArDV8PUJbkNB-LVXjkW1NfdkS_wyKQ4OhqFX_3Mt5oybtIyVVsqc5; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWOEmiqUVKMyTY74eQXjnU5JpX5KMhUgL.FoMfSoM0Sh5cS022dJLoIEnLxKML1KBLBo-LxK-LB-BL1K5LxK.LBKqL1KzLxK-LBKBLBoBEeh5p; _s_tentry=-; Apache=374968595494.0651.1711437921441; ULV=1711437921443:8:6:1:374968595494.0651.1711437921441:1710913696418'
        }
        uid_url = 'https://weibo.com/ajax/profile/detail?uid=' + str(df['uid'][a])
        print(uid_url)
        mid_url = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=' + \
                  str(df['mid'][a]) + '&is_show_bulletin=2&is_mix=0&count=10&uid=' + \
                  str(df['uid'][a]) + '&fetch_level=0&locale=zh-CN'
        print(mid_url)

        uid_page = requests.get(uid_url, headers=headers).text
        print(uid_page)
        df['auther_detail'][a] = uid_page
        # print(df['auther_detail'][i])

        # time.sleep(random.uniform(0.15, 0.35))

        mid_page = requests.get(mid_url, headers=headers).text
        # print(mid_page)
        df['audience_detail'][a] = mid_page
        # print(df['audience_detail'][i])

        # time.sleep(random.uniform(0.15, 0.35))

        if (a + 1) % 20 == 0 or a == len(df['uid']) - 1:
            df[a - 19:a + 1].to_csv('../Data/add/detail_add.csv', index=False, header=False, mode='a')

    except:
        if (a + 1) % 20 == 0 or a == len(df['uid']) - 1:
            df[a - 19:a + 1].to_csv('../Data/add/detail_add.csv', index=False, header=False, mode='a')

        time.sleep(5)
        with open("../Data/add/detail_wrong.txt", "a") as f:
            f.write("失败:" + uid_url + "\n")
            f.write("失败:" + mid_url + "\n")
            f.write("-" * 20 + "\n")


t_list = []
num = 0
for i in range(0, len(df['uid'])):
    num += 1
    t = threading.Thread(target=fetch(i), args=())
    t_list.append(t)
    t.start()
    print(str(num) + "\tover" + "-" * 10)

for t in t_list:
    t.join()
