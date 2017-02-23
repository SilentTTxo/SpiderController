from django.http import HttpResponse
from django.shortcuts import render

def system_info(request):
    return render(request,'system_info.html')