# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：     urls.py
   Description :
   Author :         laofeiji
   date ：          2024-03-12
-------------------------------------------------
"""

from django.urls import re_path
from machine.machine import gnn_img
from machine.views import upload_img, generate_img, download_img

urlpatterns = [
    re_path("getMachineImg", gnn_img.get_machine_img, ),
    re_path("uploadImg", upload_img, ),
    re_path("generateImg", generate_img, ),
    re_path("downloadImg", download_img, ),
]

