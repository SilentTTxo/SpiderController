"""SpiderController URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
import settings

from SpiderController.view import * 
from SpiderController.api import *

urlpatterns = [
    #static
    url(r'^media/(?P<path>.*)$',serve,{'document_root': settings.STATIC_URL}),

    #view
    url(r'^view/system_info.html', system_info),
    url(r'^view/login.html', login),

    #spider api
    url(r'^api/getSystemInfo', getSystemInfo),
    url(r'^api/createSpider', createSpider),
    url(r'^api/saveSpiderItem', saveSpiderItem),
    url(r'^api/getSpiderSetting', getSpiderSetting),
    url(r'^api/runSpider', runSpider),
    url(r'^api/stopSpider', stopSpider),
    url(r'^api/getSpiderInfo', getSpiderInfo),

    #user api
    url(r'^api/userlogin', userlogin),
    url(r'^api/userregist', userregist),
]
