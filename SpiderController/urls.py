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
    url(r'^view/spider_log.html', spider_log),
    url(r'^view/spider_manual.html', spider_manual),
    url(r'^view/spider_auto.html', spider_auto),
    url(r'^view/spider_new.html', spider_new),
    url(r'^view/spider_proxy.html', spider_proxy),
    url(r'^view/spider_proxyIpList.html', spider_proxyIpList),
    url(r'^view/data_list.html', data_list),
    url(r'^view/data_format.html', data_format),
    url(r'^view/admin_userlist.html', admin_userlist),
    url(r'^view/admin_power.html', admin_power),
    url(r'^view/test.html', test),

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
    url(r'^api/getSpiderLog$', getSpiderLog),
    url(r'^api/getSpiderData$', getSpiderData),
    url(r'^api/getSpiderFile$', getSpiderFile),
    url(r'^api/setSpiderFile$', setSpiderFile),
    url(r'^api/spiderDataDownload$', spiderDataDownload),
    url(r'^api/spiderDataDelete$', spiderDataDelete),
    url(r'^api/setSpiderSettingByUser$', setSpiderSettingByUser),
    url(r'^api/getSpiderSettingByUser$', getSpiderSettingByUser),
    url(r'^api/switchSpiderProxy$', switchSpiderProxy),
    

    #data api
    url(r'^api/DataTransformatDownload$', DataTransformatDownload),

    #user api
    url(r'^api/userlogin', userlogin),
    url(r'^api/userregist', userregist),
    url(r'^api/getUserInfo', getUserInfo),
    url(r'^api/getAllUser', getAllUser),
    url(r'^api/fixUserPower', fixUserPower),

    #ipproxy api
    url(r'^api/getIpInfo', getIpInfo),
    url(r'^api/addIp', addIp),
    # url(r'^api/getIpList', getIpList),

    #other api
    url(r'^api/getHtmlPage', getHtmlPage),
]
