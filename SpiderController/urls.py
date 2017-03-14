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
    url(r'^view/login.html', login),
    url(r'^view/system_info.html', system_info),
    url(r'^view/spider_simple.html', spider_simple),

    #spider api
    url(r'^api/getSystemInfo$', getSystemInfo),
    url(r'^api/createSpider$', createSpider),
    url(r'^api/saveSpiderItem$', saveSpiderItem),
    url(r'^api/getSpiderSetting$', getSpiderSetting),
    url(r'^api/runSpider$', runSpider),
    url(r'^api/stopSpider$', stopSpider),
    url(r'^api/getSpiderInfo$', getSpiderInfo),
    url(r'^api/delSpider$', delSpider),
    url(r'^api/getDataCount$', getDataCount),
    url(r'^api/setSpiderSettingByUser$', setSpiderSettingByUser),
    url(r'^api/getSpiderSettingByUser$', getSpiderSettingByUser),

    #user api
    url(r'^api/userlogin', userlogin),
    url(r'^api/userregist', userregist),
    url(r'^api/getUserInfo', getUserInfo),
]
