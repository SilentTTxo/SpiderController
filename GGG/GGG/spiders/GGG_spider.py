import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from GGG.items import GggItem

class GggSpider(scrapy.Spider):
	name="GGG"
	start_urls = ["http://www.runoob.com/django/django-model.html"]
	def parse(self,response):
		for i in response.css("html"):
			item = GggItem()
			try:
				item["H1"] = i.css("h1::text")[0].extract()
			except:
				pass
			yield item
		for href in response.css("#leftcolumn > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
