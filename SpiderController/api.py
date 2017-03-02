from django.http import HttpResponse
import json
import os
import sys
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from TTsys import *
from SpiderModel.models import *


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

    output = open(base+name+'\\'+name+'\\spiders\\'+name+'_spider.py', 'w')

    baseData = "import scrapy\n" + "from %s.items import %sItem\n\n" %(name, name.capitalize()) + \
    "class %sSpider(scrapy.Spider):\n\tname=\"%s\"\n\tstart_urls = [\"%s\"]\n" %(name.capitalize(),name,startUrl) +\
    "\tdef parse(self,response):\n"

    if(sp.param == "-1"):
        baseData += "\t\tpass\n"
    else:
        if(item != -1 and param != -1):
            baseData += "\t\tfor i in response.css('%s'):\n" %item +\
            "\t\t\titem = %sItem()\n" %name.capitalize() 
            for i in param:
                baseData += "\t\t\t%s = i.css('%s').extract()\n" %(i,param[i])
            baseData += "\t\t\tyield item\n"
        if(href != -1):
            baseData += "\t\tfor href in response.css('%s'):\n" %href +\
            "\t\t\turl = href.extract()\n" + \
            "\t\t\tyield scrapy.Request(url)\n"

        
    #sys.path.append(base+name+'\\'+name)
    #item = getattr(__import__("items"),name.capitalize()+"Item")
    #key = item.__dict__['fields'].keys()

    output.write(baseData)
    output.close()

def getSpiderItemSetting(id):
    pass

#####  spiderApi

def createSpider(request):
    name = request.GET['name']

    try:
        temp = Spider.objects.get(name = name)
        return HttpResponse(json.dumps({"code":0,"msg":"the spider has exist"}))
    except ObjectDoesNotExist:
        pass
    code = os.system("scrapy startproject "+name)
    rs = {"code":code}

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
    pass

######