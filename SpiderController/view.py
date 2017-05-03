from django.http import HttpResponse
from django.shortcuts import render

from login import isLogin,isAdmin

@isLogin
def system_info(request):
    return render(request,'system_info.html')

@isLogin
def spider_simple(request):
    return render(request,'spider_simple.html')

@isLogin
def spider_log(request):
    return render(request,'spider_log.html')

@isLogin
def spider_manual(request):
    return render(request,'spider_manual.html')

@isLogin
def spider_auto(request):
    return render(request,'spider_auto.html')

@isLogin
def data_list(request):
    return render(request,'data_list.html')

@isLogin
def data_format(request):
    return render(request,'data_format.html')

@isLogin
def admin_userlist(request):
    return render(request,'admin_userlist.html')

@isLogin
def admin_power(request):
    return render(request,'admin_power.html')

def login(request):
    return render(request,'login.html')

def test(request):
    return render(request,'test.html')