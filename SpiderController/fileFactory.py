# coding=utf-8
import sys
import os
import codecs

import json
import csv
import xlwt

def spiderFile(base,name,startUrl,param,item,href,mode):
    #write to SpiderFile
    spfile = open(base+name+'\\'+name+'\\spiders\\'+name+'_spider.py', 'w')

    baseData = "import scrapy\nfrom scrapy.utils.url import urljoin_rfc\nfrom scrapy.utils.response import get_base_url\n" + "from %s.items import %sItem\n\n" %(name, name.capitalize()) + \
    "class %sSpider(scrapy.Spider):\n\tname=\"%s\"\n\tstart_urls = [\"%s\"]\n" %(name.capitalize(),name,startUrl) +\
    "\tdef parse(self,response):\n"

    if(param == "-1"):
        baseData += "\t\tpass\n"

        spfile.write(baseData)
        spfile.close()
        return
    
    # classicMode
    if(mode == 1):
        if(item != -1 and param != -1):
            baseData += '\t\tfor i in response.css("%s"):\n' %item +\
            "\t\t\titem = %sItem()\n" %name.capitalize() 
            for i in param:
                baseData += '\t\t\ttry:\n'
                baseData += '\t\t\t\titem["%s"] = i.css("%s")[0].extract()\n' %(i,param[i])
                baseData += '\t\t\texcept:\n\t\t\t\tpass\n'

            baseData += "\t\t\tyield item\n"

        if(href != -1):
            baseData += '\t\tfor href in response.css("%s"):\n' %href +\
            "\t\t\turl = href.extract()\n" + \
            "\t\t\turl = urljoin_rfc(get_base_url(response), url)\n" + \
            "\t\t\tyield scrapy.Request(url)\n"
    
    #menu1
    elif(mode == 2):
        baseData += '\t\tfor href in response.css("%s"):\n' %href +\
            "\t\t\turl = href.extract()\n" + \
            "\t\t\turl = urljoin_rfc(get_base_url(response), url)\n" + \
            "\t\t\tyield scrapy.Request(url,self.dataParse)\n"
        
        baseData += '\n\t\tfor nexthref in response.css("%s"):\n' %param['nextHref'] +\
            "\t\t\turl = nexthref.extract()\n" + \
            "\t\t\turl = urljoin_rfc(get_base_url(response), url)\n" + \
            "\t\t\tyield scrapy.Request(url)\n"
        
        param.pop('nextHref')

        baseData += "\tdef dataParse(self,response):\n" 

        if(item != -1 and param != -1):
            baseData += '\t\tfor i in response.css("%s"):\n' %item +\
            "\t\t\titem = %sItem()\n" %name.capitalize() 
            for i in param:
                baseData += '\t\t\ttry:\n'
                baseData += '\t\t\t\titem["%s"] = i.css("%s")[0].extract()\n' %(i,param[i])
                baseData += '\t\t\texcept:\n\t\t\t\tpass\n'

            baseData += "\t\t\tyield item\n"
        
    #menuN
    elif(mode == 3):
        baseData += '\t\tfor href in response.css("%s"):\n' %href +\
            "\t\t\turl = href.extract()\n" + \
            "\t\t\turl = urljoin_rfc(get_base_url(response), url)\n" + \
            "\t\t\tyield scrapy.Request(url,self.dataParse)\n"
        
        baseData += '\n\t\tfor nexthref in response.css("%s"):\n' %param['nextHref'] +\
            "\t\t\turl = nexthref.extract()\n" + \
            "\t\t\turl = urljoin_rfc(get_base_url(response), url)\n" + \
            "\t\t\tyield scrapy.Request(url)\n"
        
        param.pop('nextHref')

        baseData += "\tdef dataParse(self,response):\n" 

        if(item != -1 and param != -1):
            ikey = 0
            pageList = []
            baseData += '\t\tfor i in response.css("%s"):\n' %item +\
            "\t\t\titem = %sItem()\n" %name.capitalize() + \
            "\t\t\turlList = []\n"

            for i in param:
                baseData += '\t\t\ttry:\n'
                baseData += '\t\t\t\t%s = i.css("%s")[0].extract()\n' %(i,param[i]['href'])
                baseData += "\t\t\t\turl = %s\n" %i +\
            "\t\t\t\turl = urljoin_rfc(get_base_url(response), url)\n" 
                baseData += '\t\t\t\turlList.append(url)\n'
                baseData += '\t\t\texcept:\n\t\t\t\tpass\n'
                param[i].pop('href')
                pageList.append(i)
                
            
            baseData += "\t\t\tyield scrapy.Request(urlList[%s],self.%sParse,meta={'item':item,'urlList':urlList})\n" %(ikey,pageList[0])
            ikey += 1
            
            for i in param:
                baseData +='\tdef %sParse(self,response):\n' %i + \
                '\t\titem = response.meta["item"]\n' + \
                '\t\turlList = response.meta["urlList"]\n\n'
                for j in param[i]:
                    baseData += '\t\ttry:\n'
                    baseData += '\t\t\titem["%s"] = response.css("%s")[0].extract()\n' %(j,param[i][j])
                    baseData += '\t\texcept:\n\t\t\t\tpass\n'
                
                if(ikey == len(param)):
                    baseData += "\t\tyield item\n"
                else:
                    baseData += "\t\tyield scrapy.Request(urlList[%s],self.%sParse,meta={'item':item,'urlList':urlList})\n" %(ikey,pageList[pageList.index(i)+1])
                ikey +=1
        
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
		if(line == "{}"):
			return item
		self.file.write(line+"\\n")
		return item
"""
    baseData = baseData %(name.capitalize(),name)
    pipfile.write(baseData)
    pipfile.close()

def settingFile(base,name,isProxy,ipList):
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
    if(isProxy):
        baseData += """
DOWNLOADER_MIDDLEWARES = {
    '%s.middlewares.RandomUserAgent': 1,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    '%s.middlewares.ProxyMiddleware': 100,
}
""" %(name,name)

        ipStr = ""
        for i in ipList:
            ipStr += "{'ip_port': '%s', 'user_pass': ''}," % i.value
        baseData += """
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
PROXIES = [
    %s
]
""" % ipStr
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
    mode = jdata['mode']

    if(mode == 1):
        for i in param:
            print i + " : " + param[i]
            baseData += "\t%s = scrapy.Field()\n" %i
    elif(mode == 2):
        param.pop("nextHref")
        for i in param:
            print i + " : " + param[i]
            baseData += "\t%s = scrapy.Field()\n" %i
    elif(mode == 3):
        param.pop("nextHref")
        for i in param:
            param[i].pop('href')

            for j in param[i]:
                baseData += "\t%s = scrapy.Field()\n" %j

    output.write(baseData)
    output.close()

def getFile(name,type):
    path = os.path.dirname(os.path.dirname(__file__)) + "\\"
    filepath = path
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

def middlewaresFile(sp,isProxy):
    name = sp.name
    base =  os.path.dirname(os.path.dirname(__file__)) + "\\"
    output = open(base+name+'\\'+name+'\\middlewares.py', 'w')

    baseData = """

from scrapy import signals
from settings import PROXIES
import random
import base64

class %sSpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        return None

    def process_spider_output(response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        pass

    def process_start_requests(start_requests, spider):

        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %%s' %% spider.name)
""" %name
    print(isProxy)
    if(isProxy):
        baseData += """
class RandomUserAgent(object):
	def __init__(self, agents):
		self.agents = agents
	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))
	def process_request(self, request, spider):
		#print "**************************" + random.choice(self.agents)
		request.headers.setdefault('User-Agent', random.choice(self.agents))
class ProxyMiddleware(object):
	def process_request(self, request, spider):
		proxy = random.choice(PROXIES)
		if proxy['user_pass'] != '':
			request.meta['proxy'] = "http://%s" % proxy['ip_port']
			encoded_user_pass = base64.encodestring(proxy['user_pass'])
			request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
			print "**************ProxyMiddleware have pass************" + proxy['ip_port']
		else:
			print "**************ProxyMiddleware no pass************" + proxy['ip_port']
			request.meta['proxy'] = "http://%s" % proxy['ip_port']
"""

    output.write(baseData)
    output.close()

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

def json2txt(oripath,targetpath):
    reload(sys)   
    sys.setdefaultencoding('utf8')

    rdata = ""
    head = []
    fs = 0
    with open(oripath, 'r') as f:
        for line in f:
            temp = json.loads(line)
            for i in temp:
                if(fs == 0):
                    head.append(i)
                
                rdata += "%s\t" % temp[i]
            fs = 1
            rdata += "\r\n"
    
    print(head)
    out = file(targetpath,"w")
    out.write(("\t").join(head) + "\r\n\r\n" + rdata)
    return rdata

def json2csv(oripath,targetpath):
    reload(sys)   
    sys.setdefaultencoding('utf8')

    rdata = []
    head = []
    fs = 0

    csvfile = file(targetpath, 'w')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)

    with open(oripath, 'r') as f:
        for line in f:
            temp = json.loads(line)
            linedata = []
            for i in temp:
                if(fs == 0):
                    head.append(i)
                linedata.append(temp[i])
            fs += 1
            if(fs == 1):
                writer.writerow(head)
                writer.writerow([])
            writer.writerow(linedata)
    
    return rdata

# def json2xls(oripath,targetpath):
#     reload(sys)   
#     sys.setdefaultencoding('utf8')

#     rdata = []
#     head = []
#     fs = 0

#     workbook = xlwt.Workbook(encoding = 'utf-8')
#     sheet = workbook.add_sheet("data")
#     style = xlwt.XFStyle()
#     font = xlwt.Font()
#     font.name = 'SimSun' # 指定“宋体”
#     style.font = font
#     sheet.write(0,0,1)

#     with open(oripath, 'r') as f:
#         for line in f:
#             temp = json.loads(line)
#             linedata = []
#             for i in temp:
#                 if(fs == 0):
#                     head.append(i)
#                 linedata.append(temp[i])
#             fs += 1
#             if(fs == 1):
#                 dd = 0
#                 for i in head:
#                     sheet.write(0,dd,i)
#                     print ("0 %s %s" % (dd,i))
#                 dd += 1
#             for i in linedata:
#                 dd = 0
#                 sheet.write(fs,dd,i)
#                 print ("%s %s %s" % (fs,dd,i))
#                 dd +=1
    
#     workbook.save(targetpath)
    
#     return rdata

def json2sql(oripath,targetpath):
    reload(sys)   
    sys.setdefaultencoding('utf8')

    createTable = """
CREATE TABLE TEMP_TABLE (
    ID  INT AUTO_INCREMENT PRIMARY KEY,
%s
);

"""
    head = ""
    insertSql = ""
    fs = 0
    with open(oripath, 'r') as f:
        for line in f:
            temp = json.loads(line)
            rdata = []
            for i in temp:
                if(fs == 0):
                    if(head == ""):
                        head +="    %s    Text" % i
                    else:
                        head +=",\n    %s    Text" % i
                rdata.append("'%s'" % temp[i].replace("\n",""))
                #rdata += "insert into TEMP_TABLE VALUES (%s)" % 
            insertSql += "insert into TEMP_TABLE VALUES (NULL,%s);\n" % ",".join(rdata)
            fs = 1
    
    createTable = createTable % head
    out = file(targetpath,"w")
    out.write(createTable + insertSql)
    return rdata