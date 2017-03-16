import os
import json

def spiderFile(base,name,startUrl,param,item,href):
    #write to SpiderFile
    spfile = open(base+name+'\\'+name+'\\spiders\\'+name+'_spider.py', 'w')

    baseData = "import scrapy\nfrom scrapy.utils.url import urljoin_rfc\nfrom scrapy.utils.response import get_base_url\n" + "from %s.items import %sItem\n\n" %(name, name.capitalize()) + \
    "class %sSpider(scrapy.Spider):\n\tname=\"%s\"\n\tstart_urls = [\"%s\"]\n" %(name.capitalize(),name,startUrl) +\
    "\tdef parse(self,response):\n"

    if(param == "-1"):
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

def pipelinesFile(base,name):
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
		self.file = codecs.open("..\\\\data\\\\%s.json","w",encoding="utf-8")

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False)
		self.file.write(line+"\\n")
		return item
"""
    baseData = baseData %(name.capitalize(),name)
    pipfile.write(baseData)
    pipfile.close()

def settingFile(base,name):
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

def itemFile(sp):
    #fix file
    data = sp.param
    name = sp.name
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

def getFile(name,type):
    path = os.path.dirname(os.path.dirname(__file__)) + "\\"
    filepath = path;
    if(type == 1): #spider
        filepath += name + "\\"+name+"\\spiders\\"+name+"_spider.py"
    if(type == 2): #piplines
        filepath += name + "\\"+name+"\\pipelines.py"
    if(type == 3): #items
        filepath += name + "\\"+name+"\\items.py"
    if(type == 4): #setting
        filepath += name + "\\"+name+"\\settings.py"
    
    file = open(filepath,'r')
    content = file.read()
    file.close()
    
    return content

def saveFile(name,type,content):
    path = os.path.dirname(os.path.dirname(__file__)) + "\\"
    filepath = path;
    if(type == 1): #spider
        filepath += name + "\\"+name+"\\spiders\\"+name+"_spider.py"
    if(type == 2): #piplines
        filepath += name + "\\"+name+"\\pipelines.py"
    if(type == 3): #items
        filepath += name + "\\"+name+"\\items.py"
    if(type == 4): #setting
        filepath += name + "\\"+name+"\\settings.py"
    
    file = open(filepath,'w')
    file.write(content)
    file.close()
    
    return 1

def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2f G" % (G)
        else:
            return "%.2f M" % (M)
    else:
        return "%.2f kb" % (kb)

def ReadLog(sp,lines):
    path = os.path.dirname(os.path.dirname(__file__)) + "\\log\\" + sp.name + ".log"
    with open(path, 'r') as f:  
        first_line = f.readline()
        f.seek(0,2)
        sum = f.tell() 
        off = -10
        data = -1   
        while True:
            f.seek(off, 2) 
            l = f.readlines()
            if len(l)>=lines or off * -1 > sum / 2:
                data = l[1-len(l):] 
                break
            off *= 2
    return data

def ReadData(sp,lines):
    path = os.path.dirname(os.path.dirname(__file__)) + "\\data\\" + sp.name + ".json"
    with open(path, 'r') as f:  
        first_line = f.readline()
        f.seek(0,2)
        sum = f.tell() 
        off = -10
        data = -1   
        while True:
            f.seek(off, 2) 
            l = f.readlines()
            if len(l)>=lines or off * -1 > sum / 2:
                data = l[1-len(l):] 
                break
            off *= 2
    return data