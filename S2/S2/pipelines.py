
import sys
import codecs
import json
class S2Pipeline(object):
    
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.file = codecs.open("..\\data\\S2.json","w",encoding="utf-8")

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False)
		self.file.write(line+"\n")
		return item
