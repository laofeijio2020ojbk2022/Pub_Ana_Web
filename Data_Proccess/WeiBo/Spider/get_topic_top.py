# 目标网站：热搜引擎
# https://weibo.zhaoyizhe.com/
# 充值两个月会员共计36元，启动浏览器后需手动登录选择时间区间，代码耗时2小时左右，运行需谨慎

import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Firefox("D:\软件下载\geckodriver")
driver.get("https://weibo.zhaoyizhe.com/")

time.sleep(60)

j = 0
while j < 69:
    time.sleep(5)
    df = pd.DataFrame(columns=['title', 'label', 'time', 'host', 'continue', 'sort', 'hot'])
    elements = driver.find_elements("class name", "el-table__row")
    eles = []
    for ele in elements:
        eles.append(ele.text.split("\n"))
    print(len(eles))
    num = 0
    for i in eles:
        if len(i) < 8:
            for g in range(8 - len(i)):
                i.append(0)
        elif len(i) > 8:
            continue
        df.loc[num] = i[1:]
        num += 1
    print(df)
    df.to_csv("../Data/add2/topic_add2.csv", index=False, header=False, mode='a')

    for k in range(5):
        try:
            js = 'window.scrollTo(0, document.body.scrollHeight);'  # 网页拉倒最下方
            driver.execute_script(js)
            print("move")
            time.sleep(random.randint(5, 7))
            position = driver.find_element("class name", "btn-next")
            ActionChains(driver).click(position).perform()
            break
        except:
            continue

    j += 1
    print(str(j) + " page over " + "-" * 10)
