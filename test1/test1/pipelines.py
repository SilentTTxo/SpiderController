
import sys
import codecs
import json
class Test1Pipeline(object):
    
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.file = codecs.open("test1.json","w",encoding="utf-8")

	def process_item(self, item, spider):
		line = json.dumps(item)
		self.file.write(line)
		return item
