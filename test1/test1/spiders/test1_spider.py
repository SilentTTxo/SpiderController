import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from test1.items import Test1Item

class Test1Spider(scrapy.Spider):
	name="test1"
	start_urls = ["http://www.runoob.com/django/django-model.html"]
	def parse(self,response):
		for i in response.css("#content > h1"):
			item = Test1Item()
			item["H2"] = i.css("h1::text")[0].extract()
			yield item
		for href in response.css("#leftcolumn > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
