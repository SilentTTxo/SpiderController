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
		self.file = codecs.open("..\\data\\%s.json","w",encoding="utf-8")

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