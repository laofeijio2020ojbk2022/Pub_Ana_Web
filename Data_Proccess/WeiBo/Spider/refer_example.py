# 通过OAuth2授权，合法调用官方接口
# 1.接口friendships/friends和friendships/followers根据目标用户的uid查询目标用户的关注和粉丝列表：
# 这是一个失败的尝试，由于接口升级后uid只能为当前授权用户，也就是说是只能查自己，简直离谱！！！
# 2.接口comments/show根据微博ID返回某条微博的评论列表

import requests
from new_math import id_to_mid

# 通过sinaweibopy3获取access_token
# 授权时间为一天，所以需要每天跟新
# {
#     'access_token': '2.00nzmHQIPSBMNB14bb49a6018dlaRD',
#     'remind_in': '157679999',
#     'expires_in': 1867378750,
#     'uid': '7567340671',
#     'isRealName': 'true'
# }

# 将微博的id转化为mid
mid = id_to_mid('O3K6Trcs7')

params = {'access_token': '2.00nzmHQIPSBMNB14bb49a6018dlaRD', 'id': mid}
url = 'https://api.weibo.com/2/comments/show.json'
html = requests.get(url=url, params=params).text
print(html)
