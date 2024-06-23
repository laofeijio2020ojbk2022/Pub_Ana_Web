# 找到中国地图每个省的中心点

import json
import numpy as np
from scipy.spatial import ConvexHull

with open('china.json') as f:
    china = json.load(f)

position = []

for i in china['features']:
    # print(i)

    province = i['properties']['name']
    print(province)

    if province == '内蒙古自治区':
        coordinates = i['geometry']['coordinates'][0]
    else:
        coordinates = i['geometry']['coordinates'][0][0]

    print(len(coordinates))

    coordinates = np.array(coordinates)
    # print(coordinates)

    # 计算凸包
    hull = ConvexHull(coordinates)
    # print(hull)

    # 找到凸包的顶点
    vertices = coordinates[hull.vertices]
    # print(vertices)

    # 计算凸包顶点的中心
    center = np.mean(vertices, axis=0)
    print(center)
    # print(i['properties']['center'])

    position.append({
        'name': province,
        'position': list(center),
    })

    # break

# print(position[:-1])

result = {
    'data': position[:-1],
}

result = json.dumps(result, ensure_ascii=False, indent=4)
print(result)

with open('center.json', 'w') as f:
    f.write(result)






