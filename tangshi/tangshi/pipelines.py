
import sys
import codecs
import json
class TangshiPipeline(object):
    
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.file = codecs.open("..\\data\\tangshi.json","w",encoding="utf-8")

	def process_item(self, item, spider):
		if(json.dumps(dict(item), ensure_ascii=False) == "{}"):
			return item
		line = item['author'] + '\t' + item['dynasty'] + '\t' + item['name'] + '\t' + item['content']
		self.file.write(line+"\n")
		return item
