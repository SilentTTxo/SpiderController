from django.http import HttpResponse
from django.shortcuts import render

from login import isLogin,isAdmin

@isLogin
def system_info(request):
    return render(request,'system_info.html')

def login(request):
    return render(request,'login.html')