
import sys
import codecs
import json
class TangshiPipeline(object):
    
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.file = codecs.open("..\\data\\tangshi.json","w",encoding="utf-8")

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False)
		if(line == "{}"):
			return item
		self.file.write(line+"\n")
		return item
