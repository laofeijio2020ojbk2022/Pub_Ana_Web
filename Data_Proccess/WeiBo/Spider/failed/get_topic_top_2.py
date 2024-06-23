# 目标网站：榜眼数据
# https://www.tophubdata.com/
# 搜索费用太高，预计预算超标

import requests

params = {'Authorization': 'dc8502f3fb1029bbc02968055fb3b605'}
url = 'https://api.tophubdata.com/nodes?p=1'
html = requests.get(url=url, params=params).text
print(html)


