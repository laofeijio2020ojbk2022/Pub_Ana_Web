import os
import random
from PIL import Image

# 指定文件夹路径
path = "../../img/gnn_dataset/img_300/input/"  # 替换为包含图片文件的文件夹路径

# 定义大图的大小
big_width = 10 * 50  # 一行10张图片，每张图片宽为50像素
big_height = 5 * 50   # 一共5行图片，每张图片高为50像素
big_image = Image.new('RGB', (big_width, big_height), (255, 255, 255))  # 创建一个白色背景的大图

count = 0
for i in os.listdir(path):
    if i != '物品':
        folder_path = path + i + '/1/'
        image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if
                       file.endswith(('jpg', 'jpeg', 'png', 'gif'))]
        random_images = random.sample(image_files, 10)

        count2 = 0
        for j in random_images:
            print(j)
            x_offset = count2 * 50  # 水平偏移量
            y_offset = count * 50  # 垂直偏移量

            img = Image.open(j)
            big_image.paste(img, (x_offset, y_offset))

            count2 += 1

        count += 1

# 保存拼接后的大图
path = '../../img/gnn_dataset/img_300/big_img.jpg'
big_image.save(path)