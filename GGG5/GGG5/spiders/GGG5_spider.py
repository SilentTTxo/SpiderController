import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from GGG5.items import Ggg5Item

class Ggg5Spider(scrapy.Spider):
	name="GGG5"
	start_urls = ["http://www.runoob.com/django/django-model.html"]
	def parse(self,response):
		for i in response.css("#content > h1"):
			item = Ggg5Item()
			try:
				item["H2"] = i.css("h1::text")[0].extract()
			except:
				pass
			yield item
		for href in response.css("#leftcolumn > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
