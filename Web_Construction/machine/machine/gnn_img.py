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


@require_http_methods(["GET"])
def get_machine_img(request):
    response = {}
    response['back'] = 'success'
    print('ok')

    # input_folder = './img/gnn_dataset/img_300'
    # output_file = './img/gnn_dataset/img_300_output'
    input_folder = './img/gnn_dataset/img_300/input/物品'
    output_file = './img/gnn_dataset/img_300/output/物品'
    train_gan(input_folder, output_file)

    return JsonResponse(response)


def train_gan(dataset_path, output_file):
    # 定义预处理操作
    transform = transforms.Compose([
        transforms.Resize(50),
        transforms.CenterCrop(50),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # 加载图像数据集
    dataset = ImageFolder(root=dataset_path, transform=transform)

    # 创建数据加载器
    data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

    # 定义生成器和鉴别器
    generator = Generator()
    discriminator = Discriminator()

    # 定义损失函数
    adversarial_loss = nn.BCELoss()  # 二元交叉熵损失函数

    # 定义优化器
    optimizer_G = optim.Adam(generator.parameters(), lr=0.0003, betas=(0.9, 0.999))  # 生成器的优化器
    optimizer_D = optim.Adam(discriminator.parameters(), lr=0.0003, betas=(0.9, 0.999))  # 鉴别器的优化器

    # 设置训练参数
    num_epochs = 15
    latent_dim = 100

    for epoch in range(num_epochs):
        for i, (imgs, _) in enumerate(data_loader):

            # 训练鉴别器
            optimizer_D.zero_grad()

            # 生成随机噪声数据
            z = torch.randn(imgs.size(0), latent_dim)
            fake_imgs = generator(z)

            real_loss = adversarial_loss(discriminator(imgs), torch.ones(imgs.size(0), 1))
            fake_loss = adversarial_loss(discriminator(fake_imgs.detach()), torch.zeros(imgs.size(0), 1))
            d_loss = (real_loss + fake_loss) / 2

            d_loss.backward()
            optimizer_D.step()

            # 训练生成器
            optimizer_G.zero_grad()

            # 重新生成随机噪声数据
            z = torch.randn(imgs.size(0), latent_dim)
            fake_imgs = generator(z)  # 使用相同的随机噪声数据z

            g_loss = adversarial_loss(discriminator(fake_imgs), torch.ones(imgs.size(0), 1))

            g_loss.backward()
            optimizer_G.step()

            if i % 100 == 0:
                print("[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f]" % (
                    epoch, num_epochs, i, len(data_loader), d_loss.item(), g_loss.item()))

        # 每个epoch结束后生成一张图片并保存
        # if epoch % 10 == 0:
        z = torch.randn(1, latent_dim)
        fake_img = generator(z)
        save_image(fake_img, f"{output_file}/imgs/generated_img_{epoch}.jpg")

    save_image(fake_img, f"{output_file}/result_img.jpg")

    # 保存生成器和鉴别器的模型参数
    torch.save(generator.state_dict(), f'{output_file}/generator.pth')
    torch.save(discriminator.state_dict(), f'{output_file}/discriminator.pth')


# 定义生成器模型
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(100, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 1024),
            nn.LeakyReLU(0.2),
            nn.Linear(1024, 7500),
            nn.Tanh()
        )

    def forward(self, z):
        img = self.model(z)
        img = img.view(img.size(0), 3, 50, 50)
        return img


# 定义鉴别器模型
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(7500, 1024),
            nn.LeakyReLU(0.2),
            nn.Linear(1024, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, img):
        img = img.view(img.size(0), -1)
        validity = self.model(img)
        return validity