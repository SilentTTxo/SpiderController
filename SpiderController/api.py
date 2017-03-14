import json
import os
import sys

from subprocess import Popen, PIPE ,CREATE_NEW_PROCESS_GROUP
import ctypes
import signal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from SpiderModel.models import *
from fileFactory import *
from TTsys import *

runningSpider = {} # to save the thread which is running Spider

def getSystemInfo(request):
    rs = {"CPU":getCPUstate(),"RAM":getMemorystate(),"NET":getNetsate()}
    return HttpResponse(json.dumps(rs))

######  spiderfun

def spiderFactoryUpdate(sp):
    name = sp.name
    startUrl = ""
    param = -1
    item = -1
    href = -1

    if(sp.param != "-1"):
        data = json.loads(sp.param)
        startUrl = data['startUrl']
        param = data['param']
        item = data['item']
        href = data['href']

    base =  os.path.dirname(os.path.dirname(__file__)) + "\\"

    spiderFile(base,name,startUrl,param,item,href)
    pipelinesFile(base,name)
    settingFile(base,name)
    

def getSpiderStatusById(sid):
    global runningSpider
    if(runningSpider.get(sid,-1) == -1):
        return 0 #not running
    if(runningSpider.get(sid,-1).poll() != None):
        runningSpider.pop(sid)
        return 0 #not running
    return 1 #running

def countSpiderData(sp):
    name = sp.name
    thefilepath = "data\\"+name+".json"
    
    count = 0
    for count, line in enumerate(open(thefilepath, 'rU')):
        pass
    return count
#####  spiderApi

def createSpider(request):
    name = request.GET['name']

    try:
        temp = Spider.objects.get(name = name)
        return HttpResponse(json.dumps({"code":0,"msg":"the spider has exist"}))
    except ObjectDoesNotExist:
        pass
    code = os.system("scrapy startproject "+name)
    rs = {"code":1}

    sp = Spider.objects.create(name = name,uid=-1,param='-1')
    spiderFactoryUpdate(sp)
    return HttpResponse(json.dumps(rs))

@csrf_exempt
def saveSpiderItem(request):

    sid = request.POST['sid']
    data = request.POST['param']
    sp = Spider.objects.get(id=sid)
    name = sp.name

    #fix file
    base =  os.path.dirname(os.path.dirname(__file__)) + "\\"
    output = open(base+name+'\\'+name+'\\items.py', 'w')

    baseData = "import scrapy\n\nclass %sItem(scrapy.Item):\n" %(name.capitalize())
    jdata = json.loads(data)
    param = jdata['param']
    for i in param:
        print i + " : " + param[i]
        baseData += "\t%s = scrapy.Field()\n" %i

    output.write(baseData)
    output.close()

    #save to mysql
    sp.param = data
    sp.save()

    spiderFactoryUpdate(sp)

    rs = {"code":1}
    return HttpResponse(json.dumps(rs))

def runSpider(request):
    sid = request.GET.get('sid',-1)
    if(sid == -1):
        return HttpResponse(json.dumps({"code":0,"msg":"param error"}))
    try:
        temp = Spider.objects.get(id = sid)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"code":0,"msg":"the spider has not exist"}))
    
    origin = os.path.abspath('.')
    base =  os.path.dirname(os.path.dirname(__file__)) + "\\"
    os.chdir(base + temp.name)

    print("scrapy crawl "+temp.name + " > " + base + "log\\" + temp.name + ".log")
    p = Popen("scrapy crawl "+temp.name +" > " + base + "log\\" + temp.name + ".log 2>&1",shell=True,creationflags=CREATE_NEW_PROCESS_GROUP)

    #checkout to origin path
    os.chdir(origin)

    global runningSpider
    runningSpider[sid] = p
    return HttpResponse(json.dumps({"code":1}))

def stopSpider(request):
    sid = request.GET.get('sid',-1)
    if(sid == -1):
        return HttpResponse(json.dumps({"code":0,"msg":"param error"}))
    try:
        temp = Spider.objects.get(id = sid)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"code":0,"msg":"the spider has not exist"}))
    
    global runningSpider
    if(runningSpider.get(sid,-1) == -1):
        return HttpResponse(json.dumps({"code":0,"msg":"the spider has been done"}))

    os.system("taskkill /PID %s /T /F" %runningSpider[sid].pid) 
    runningSpider.pop(sid)
    return HttpResponse(json.dumps({"code":1}))

def delSpider(request):
    sid = request.GET.get('sid',-1)
    if(sid == -1):
        return HttpResponse(json.dumps({"code":0,"msg":"param error"}))
    try:
        temp = Spider.objects.get(id = sid)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"code":0,"msg":"the spider has not exist"}))
    
    name = temp.name
    temp.delete()
    os.system("rmdir /s /q " + name)
    return HttpResponse(json.dumps({"code":1}))

def getSpiderSetting(request):
    data = Spider.objects.get(id = request.GET['sid'])

    return HttpResponse(data.param)

def getSpiderInfo(request):
    sp = Spider.objects.filter(uid = request.session['uid'])
    data = {"code":1}
    y = []
    for i in sp:
        item = {"sid":i.id,"name":i.name,"status":getSpiderStatusById(str(i.id)),"other":i.other,"datasum":"No data"}
        path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + i.name + ".json"
        if os.path.exists(path):
            size = os.path.getsize(path)
            item['datasum'] = formatSize(size)
        y.append(item)
    data['data'] = y
    return HttpResponse(json.dumps(data))

def getDataCount(request):
    sp = Spider.objects.get(id = request.GET['sid'])
    count = countSpiderData(sp)

    return HttpResponse(json.dumps({"code":1,"count":count}))

@csrf_exempt
def setSpiderSettingByUser(request):
    sp = Spider.objects.get(id = request.POST['sid'])
    type = request.POST['type']  #0.spider 1.piplines 2.setting
    content = request.POST['content']
    base =  os.path.dirname(os.path.dirname(__file__)) + "\\"

    code = setFile(base,sp.name,int(type),content)

    return HttpResponse(json.dumps({"code":code}))

@csrf_exempt
def getSpiderSettingByUser(request):
    sp = Spider.objects.get(id = request.POST['sid'])
    type = request.POST['type']  #0.spider 1.piplines 2.setting
    base =  os.path.dirname(os.path.dirname(__file__)) + "\\"

    content = getFile(base,sp.name,int(type))

    return HttpResponse(json.dumps({"code":1,"content":content}))

###### userApi
@csrf_exempt
def userlogin(request):
    username = request.POST.get('username',-1)
    password = request.POST.get('password',-1)

    if(username == -1 or password == -1):
        return HttpResponse(json.dumps({"code":0,"msg":"param error"}))

    try:
        user = User.objects.get(username = username)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"code":0,"msg":"username error"}))

    if(user.password == password):
        request.session['username'] = user.username
        request.session['uid'] = user.id
        request.session['power'] = user.power
        return HttpResponse(json.dumps({"code":1}))
    else:
        return HttpResponse(json.dumps({"code":0,"msg":"password error"}))

@csrf_exempt
def userregist(request):
    username = request.POST.get('username',-1)
    password = request.POST.get('password',-1)

    if(username == -1 or password == -1):
        return HttpResponse(json.dumps({"code":0,"msg":"param error"}))

    try:
        user = User.objects.get(username = username)
        return HttpResponse(json.dumps({"code":0,"msg":"username has already exist"}))
    except ObjectDoesNotExist:
        pass

    User.objects.create(username = username,password = password,power = 0)
    return HttpResponse(json.dumps({"code":1}))

def getUserInfo(request):
    data = {"id":request.session['uid'],"username":request.session['username'],"power":request.session['power']}

    return HttpResponse(json.dumps(data))