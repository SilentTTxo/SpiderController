import json
import os
import sys

from subprocess import Popen, PIPE ,CREATE_NEW_PROCESS_GROUP
import ctypes
import signal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from TTsys import *
from SpiderModel.models import *

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

    #write to SpiderFile
    spfile = open(base+name+'\\'+name+'\\spiders\\'+name+'_spider.py', 'w')

    baseData = "import scrapy\nfrom scrapy.utils.url import urljoin_rfc\nfrom scrapy.utils.response import get_base_url\n" + "from %s.items import %sItem\n\n" %(name, name.capitalize()) + \
    "class %sSpider(scrapy.Spider):\n\tname=\"%s\"\n\tstart_urls = [\"%s\"]\n" %(name.capitalize(),name,startUrl) +\
    "\tdef parse(self,response):\n"

    if(sp.param == "-1"):
        baseData += "\t\tpass\n"
    else:
        if(item != -1 and param != -1):
            baseData += '\t\tfor i in response.css("%s"):\n' %item +\
            "\t\t\titem = %sItem()\n" %name.capitalize() 
            for i in param:
                baseData += '\t\t\titem["%s"] = i.css("%s")[0].extract()\n' %(i,param[i])
            baseData += "\t\t\tyield item\n"

        if(href != -1):
            baseData += '\t\tfor href in response.css("%s"):\n' %href +\
            "\t\t\turl = href.extract()\n" + \
            "\t\t\turl = urljoin_rfc(get_base_url(response), url)\n" + \
            "\t\t\tyield scrapy.Request(url)\n"

        
    #sys.path.append(base+name+'\\'+name)
    #item = getattr(__import__("items"),name.capitalize()+"Item")
    #key = item.__dict__['fields'].keys()

    spfile.write(baseData)
    spfile.close()

    #write to pipelines
    pipfile = open(base+name+'\\'+name+'\\pipelines.py', 'w')

    baseData = """
import sys
import codecs
import json
class %sPipeline(object):
    
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.file = codecs.open("%s.json","w",encoding="utf-8")

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False)
		self.file.write(line+"\\n")
		return item
"""
    baseData = baseData %(name.capitalize(),name)
    pipfile.write(baseData)
    pipfile.close()

    #add pipline setting
    settingfile = open(base+name+'\\'+name+'\\settings.py', 'w')
    baseData = """
BOT_NAME = '%s'

SPIDER_MODULES = ['%s.spiders']
NEWSPIDER_MODULE = '%s.spiders'

ITEM_PIPELINES = {
    '%s.pipelines.%sPipeline': 800,
}
    """
    baseData = baseData %(name,name,name,name,name.capitalize())
    settingfile.write(baseData)
    settingfile.close()

def getSpiderStatusById(sid):
    global runningSpider
    if(runningSpider.get(sid,-1) == -1):
        return 0 #not running
    if(runningSpider.get(sid,-1).poll() != None):
        runningSpider.pop(sid)
        return 0 #not running
    return 1 #running
    
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
    
    base =  os.path.dirname(os.path.dirname(__file__)) + "\\"
    os.chdir(base + temp.name)

    print("scrapy crawl "+temp.name + " > " + base + "log\\" + temp.name + ".log")
    p = Popen("scrapy crawl "+temp.name +" > " + base + "log\\" + temp.name + ".log 2>&1",shell=True,creationflags=CREATE_NEW_PROCESS_GROUP)

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
    data = Spider.objects.get(id = request.GET['id'])

    return HttpResponse(data.param)

def getSpiderInfo(request):
    sp = Spider.objects.filter(uid = request.session['uid'])
    data = {"code":1}
    y = []
    for i in sp:
        item = {"sid":i.id,"name":i.name,"status":getSpiderStatusById(str(i.id)),"other":i.other}
        y.append(item)
    data['data'] = y
    return HttpResponse(json.dumps(data))

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