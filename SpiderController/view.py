from django.http import HttpResponse
from django.shortcuts import render

from login import isLogin,isAdmin

@isLogin
def system_info(request):
    return render(request,'system_info.html')

@isLogin
def spider_simple(request):
    return render(request,'spider_simple.html')

def login(request):
    return render(request,'login.html')