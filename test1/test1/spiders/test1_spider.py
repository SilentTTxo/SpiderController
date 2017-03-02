import scrapy
from test1.items import Test1Item

class Test1Spider(scrapy.Spider):
	name="test1"
	start_urls = ["url"]
	def parse(self,response):
		for i in response.css('css'):
			item = Test1Item()
			yooo = i.css('1').extract()
			yu = i.css('2').extract()
			yield item
		for href in response.css('css'):
			url = href.extract()
			yield scrapy.Request(url)
