import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from GGG6.items import Ggg6Item

class Ggg6Spider(scrapy.Spider):
	name="GGG6"
	start_urls = ["http://www.runoob.com/django/django-model.html"]
	def parse(self,response):
		for i in response.css("html"):
			item = Ggg6Item()
			try:
				item["H1"] = i.css("h1::text")[0].extract()
			except:
				pass
			yield item
		for href in response.css("#leftcolumn > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
