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
from crawler.views import get_cookies, save_cookies
from crawler.spider import get_title, get_post, get_detail, save_title, save_post, save_comment

urlpatterns = [
    re_path("getCookies", get_cookies, ),
    re_path("saveCookies", save_cookies, ),
    re_path("getTitle", get_title.get_title, ),
    re_path("getPost", get_post.get_post, ),
    re_path("getDetail", get_detail.get_detail, ),
    re_path("saveTitle", save_title.save_title, ),
    re_path("savePost", save_post.save_post, ),
    re_path("saveComment", save_comment.save_comment, ),
]

