# 多线程爬虫，预计时长4小时

import time

import requests
import pandas as pd
from new_math import get_ua
from lxml import etree, html
import threading

global num
num = 0

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
        url =" https://s.weibo.com/weibo?q=%23" + a + "%23&xsort=hot&Refer=hotmore"
        print(url)

        page = requests.get(url, headers=headers).text
        # print(page)
        page = html.fromstring(page)
        print(page)
        auther = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "info")]/div[2]/a/text()')
        # print(auther)
        auther_url = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "info")]/div[2]/a/@href')
        # print(auther_url)
        the_url = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "from")]/a[1]/@href')
        # print(the_url)
        txt2 = []
        for txt in page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "content")]/p'):
            txt2.append("".join(txt.xpath('text()')[1:-1]))
        # print(txt2)
        transmit = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "card-act")]/ul/li[1]/a/text()[2]')
        # print(transmit)
        comment = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "card-act")]/ul/li[2]/a/text()')
        # print(comment)
        like = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "woo-like-count")]/text()')
        # print(like)

        the_df = pd.DataFrame([auther, auther_url, the_url, txt2, transmit, comment, like]).transpose()
        the_df['title'] = a
        print(the_df)

        the_df.to_csv("../Data/add/post_add.csv", index=False, header=False, mode='a')
    except:
        time.sleep(5)
        with open("../Data/add/post_wrong.txt", "a") as f:
            f.write("失败:" + url + "\n")

# https://s.weibo.com/weibo?q=%23%E6%9D%8E%E5%B2%B1%E6%98%86%E9%87%8D%E7%B4%AB%E7%83%9F%E7%86%8F%E5%A6%86%23&xsort=hot&Refer=hotmore
df = pd.read_csv("../Data/add/topic_add_2.csv")
# df = df[df['hot'] > 1000000]

t_list = []
for i in range(len(df['title'])):
    num += 1
    t = threading.Thread(target=fetch(df['title'][i]), args=())
    t_list.append(t)
    t.start()
    print(str(num) + "\tover" + "-" * 10)

for t in t_list:
    t.join()




