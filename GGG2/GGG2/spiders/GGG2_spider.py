import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from GGG2.items import Ggg2Item

class Ggg2Spider(scrapy.Spider):
	name="GGG2"
	start_urls = ["http://www.runoob.com/django/django-model.html"]
	def parse(self,response):
		for i in response.css("html"):
			item = Ggg2Item()
			try:
				item["h1"] = i.css("h1::text")[0].extract()
			except:
				pass
			yield item
		for href in response.css("#leftcolumn > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
