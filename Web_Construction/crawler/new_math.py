# 自制算法包：id_to_mid(id)

import base62

# 通过62进制解码算法将微博的id转化为mid
def id_to_mid(id):
    id = str(id)[::-1]
    size = int(len(id) / 4) if len(id) % 4 == 0 else int(len(id) / 4 + 1)
    result = []
    for i in range(size):
        s = id[i * 4: (i + 1) * 4][::-1]
        s = str(base62.decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return ''.join(result)
# print(id_to_mid('O3K6Trcs7'))

# 得到一个时间区间内的所有日期编码
def get_the_date(before, after):
    day_31 = [1, 3, 5, 7, 8, 10, 12]
    the_data = []
    for mouth in range(int(before[0:2]), int(after[0:2])+1):
        print()
        if mouth == int(before[0:2]):
            start = int(before[2:4])
        else:
            start = 1

        if mouth == int(after[0:2]):
            end = int(after[2:4])
        else:
            if mouth in day_31:
                end = 31
            elif mouth == 2:
                end = 28
            else:
                end = 30

        if mouth < 10:
            mouth2 = "0" + str(mouth)
        else:
            mouth2 = str(mouth)

        for day in range(start, end+1):
            if day < 10:
                day = "0" + str(day)
            else:
                day = str(day)

            the_data.append(mouth2 + day)

    return the_data
# print(get_the_date("0101", "1231"))

# 产生随机代理
def get_ua():
    import random
    first_num = random.randint(55, 76)
    third_num = random.randint(0, 3800)
    fourth_num = random.randint(0, 140)
    os_type = ['(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)', '(Macintosh; Intel Mac OS X 10_14_5)']
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)
    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36', '(KHTML, like Gecko)', chrome_version, 'Safari/537.36'])
    return ua