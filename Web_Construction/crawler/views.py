import browser_cookie3
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from crawler.models import CookiesTable

# Create your views here.

@require_http_methods(["GET"])
def get_cookies(request):
    response = {}

    co_id = request.GET.get('id')
    # print(id)

    cookies = get_cookies2()
    s = ''
    for i in cookies:
        s += (i.name + '=' + i.value + ';')
    # print(s)
    response['cookie'] = s

    try:
        data = CookiesTable.objects.filter(co_id=co_id)
        if data:
            CookiesTable.objects.filter(co_id=co_id).update(
                co_cookie=s
            )
        else:
            CookiesTable.objects.create(
                co_id=co_id,
                co_cookie=s
            )
        response['back'] = 'success'
    except:
        response['back'] = 'failed'

    return JsonResponse(response)


# 获取火狐浏览器保存在本地的cookies
# 开发常用谷歌，但是新版谷歌运行会锁住cookies
def get_cookies2():
    cj = browser_cookie3.firefox(domain_name='weibo.com')
    return cj


@require_http_methods(["GET"])
def save_cookies(request):
    response = {}

    cookie = request.GET.get('cookie')
    # print(cookie)
    co_id = request.GET.get('id')
    # print(co_id)

    try:
        data = CookiesTable.objects.filter(co_id=co_id)
        if data:
            CookiesTable.objects.filter(co_id=co_id).update(
                co_cookie=cookie
            )
        else:
            CookiesTable.objects.create(
                co_id=co_id,
                co_cookie=cookie
            )
        response['back'] = 'success'
    except:
        response['back'] = 'failed'

    return JsonResponse(response)
