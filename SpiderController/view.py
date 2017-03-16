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
def data_list(request):
    return render(request,'data_list.html')

def login(request):
    return render(request,'login.html')