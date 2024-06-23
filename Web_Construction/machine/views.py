import os
import random
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import torch
import torch.optim as optim
from PIL import Image
import torchvision.transforms as transforms
import torch.nn as nn
from skimage.metrics import structural_similarity as ssim
from skimage import io
import imagehash
import math
import os
import torch
import torch.nn as nn
import torch.optim as optim
from matplotlib import pyplot as plt
from PIL import Image
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import numpy as np
from torchvision.utils import save_image

# Create your views here.

@require_http_methods(["POST"])
def upload_img(request):
    response = {}
    response['back'] = 'success'
    # print('ok')

    try:
        # 从request.FILES中获取上传的文件
        uploaded_file = request.FILES['file']

        with open('./img/backend/upload_img/img.jpg', 'wb') as f:
            for i in uploaded_file.chunks():
                f.write(i)
    except:
        response['back'] = 'error'

    return JsonResponse(response)



@require_http_methods(["GET"])
def download_img(request):
    response = {}
    response['back'] = 'success'
    # print('ok')

    index = request.GET.get('index')

    image_path = f'./frontend/src/assets/img/output_img/{index}.jpg'
    if os.path.exists(image_path):
        image_file = open(image_path, 'rb')
        response = FileResponse(image_file)
        # 不要在这里关闭文件对象
        return response
    else:
        return JsonResponse({'error': 'Image not found'}, status=404)


@require_http_methods(["GET"])
def generate_img(request):
    response = {}
    response['back'] = 'success'

    # generate_img_2()

    input_file = './img/gnn_dataset/img_300/output/'
    folder_path = './img/gnn_dataset/img_300/input/'
    input_img_path = './img/backend/upload_img/img.jpg'
    name = '动物'
    min_img = 100
    for i in os.listdir(input_file):
        img = io.imread(input_file + i + '/result_img.jpg', as_gray=True)
        input_img = io.imread(input_img_path, as_gray=True)

        # 计算结构相似性指数（SSIM）
        ssim_index = ssim(img, input_img, data_range=input_img.max() - input_img.min())

        if abs(1-ssim_index) < min_img:
            min_img = abs(1-ssim_index)
            name = i

    folder_path = folder_path + name + '/1/'
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    random_images = random.sample(image_files, 9)

    count = 1
    for i in random_images:
        img = Image.open(i)
        # print(img)
        img.save(f'./frontend/src/assets/img/output_img/{count}.jpg')
        count += 1

    return JsonResponse(response)
