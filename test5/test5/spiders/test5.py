import scrapy
from test5.items import DmozItem

class Test5Spider(scrapy.Spider):
	name="test5"
	start_urls = ["url"]
	def parse(self,response):
		pass
