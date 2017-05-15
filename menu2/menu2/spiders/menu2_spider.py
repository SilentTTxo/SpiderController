import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from menu2.items import Menu2Item

class Menu2Spider(scrapy.Spider):
	name="menu2"
	start_urls = ["http://so.gushiwen.org/type.aspx"]
	def parse(self,response):
		for href in response.css(".sons > p > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url,self.dataParse)

		for nexthref in response.css(".pages > a::attr(href)"):
			url = nexthref.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
	def dataParse(self,response):
		for i in response.css("html"):
			item = Menu2Item()
			try:
				item["H1"] = i.css("h1::text")[0].extract()
			except:
				pass
			yield item
