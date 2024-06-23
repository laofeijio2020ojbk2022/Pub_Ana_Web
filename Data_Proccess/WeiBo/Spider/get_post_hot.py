# 通过热搜获取相应热搜的热帖
# 预计爬取时间超过30小时，应尝试缩短时间
# 详细代码请见：get_post_hot_2

import time

import requests
import pandas as pd
from new_math import get_ua
from lxml import etree, html

# https://s.weibo.com/weibo?q=%23%E6%9D%8E%E5%B2%B1%E6%98%86%E9%87%8D%E7%B4%AB%E7%83%9F%E7%86%8F%E5%A6%86%23&xsort=hot&Refer=hotmore
df = pd.read_csv("../Data/topic_2.csv")
num = 0
for i in df['title']:
    num += 1
    try:
        headers = {
            'User-Agent': get_ua(),
            'authority': 's.weibo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
            'Cookie': 'SCF=AqD86_2GgPKMnksxd_CPrP5KUvDmij-I9LNg0Tq5SdBUlgXGc3HBi4JISUtN2ZNt-To5i444fFIRB8-lQtH7bF4.; SINAGLOBAL=8141950821074.444.1706926835159; login_sid_t=70d89b583596b4171987124be73eba95; cross_origin_proto=SSL; _s_tentry=www.google.com.hk; Apache=5463332342355.261.1709693114451; ULV=1709693114454:3:1:1:5463332342355.261.1709693114451:1707047771690; ALF=1712285230; SUB=_2A25I46l-DeRhGeFL7VUS9C7KzD2IHXVrgKS2rDV8PUJbkNANLU_mkW1NfdkS_5O2oKCWZ8rMvJRv3pPVlonVpNUG; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWOEmiqUVKMyTY74eQXjnU5JpX5KzhUgL.FoMfSoM0Sh5cS022dJLoIEnLxKML1KBLBo-LxK-LB-BL1K5LxK.LBKqL1KzLxK-LBKBLBoBEeh5p; UOR=,,www.zhaoyizhe.com'
        }
        url =" https://s.weibo.com/weibo?q=%23" + i + "%23&xsort=hot&Refer=hotmore"
        print(url)

        page = requests.get(url, headers=headers).text
        # print(page)
        page = html.fromstring(page)
        print(page)
        auther = page.xpath('//*[@id="pl_feedlist_index"]/div[4]//*[contains(@class, "info")]/div[2]/a/text()')
        # print(auther)
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

        the_df = pd.DataFrame([auther, the_url, txt2, transmit, comment, like]).transpose()
        the_df['title'] = i
        print(the_df)

        the_df.to_csv("../Data/post.csv", index=False, header=False, mode='a')
        print(str(num) + "\tover" + "-"*10)
    except:
        time.sleep(5)
        with open("../Data/post_wrong.txt", "a") as f:
            f.write("失败:" + url + "\n")

    # break


