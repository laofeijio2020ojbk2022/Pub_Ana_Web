# 目标网站：热搜时光机
# https://www.weibotop.cn/2.0/
# 长时间爬取数据ip被封

import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from new_math import get_the_date

driver = webdriver.Firefox("D:\软件下载\geckodriver")
driver.get("https://www.weibotop.cn/2.0/")

position = driver.find_element('id', 'selectDateTime')
position.send_keys("0020230101235959")
time.sleep(10)

the_date = get_the_date("0314", "1231")
for day in the_date:
    # 由于目标网站不够稳定，常常出错，最多尝试5次，否则输出问题存在在日期
    for cyclic in range(5):
        try:
            position = driver.find_element('id', 'selectDateTime')
            ActionChains(driver).click(position).perform()
            time.sleep(1)
            position.send_keys("002023" + day + "235959")
            time.sleep(random.randint(5, 7))

            elements = driver.find_elements('class name', 'mb-1')
            title = []
            hot = []
            flag = 0
            for i in elements:
                if flag % 2 == 0 and flag != 0:
                    hot.append(i.text)
                elif flag % 2 == 1:
                    title.append(i.text)
                flag += 1

            if title[0] != "高源批评江一燕" and title[0] != "十四届全国人大一次会议闭幕会":
                break
            elif cyclic == 4:
                with open("../../Data/failed/topic_wrong_date.txt", "a") as f:
                    f.write("bug:" + day + "\n")
        except:
            time.sleep(5)
            with open("../../Data/failed/topic_wrong_date.txt", "a") as f:
                f.write("失效:" + day + "\n")

    the_dict = dict(zip(title, hot))
    # print(the_dict)
    df = pd.DataFrame(list(the_dict.items()))
    df['time'] = "2023-" + day[0:2] + "-" + day[2:4]
    df.to_csv("../Data/topic.csv", index=False, header=False, mode='a')

    print(df)

# time.sleep(1)


# ActionChains(driver).context_click(element).perform()
