import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from tangshi.items import TangshiItem

class TangshiSpider(scrapy.Spider):
	name="tangshi"
	start_urls = ["http://so.gushiwen.org/gushi/songsan.aspx"]
	def parse(self,response):
		for i in response.css(".shileft"):
			item = TangshiItem()
			try:
				item["content"] = i.css("#cont::text")[0].extract()
			except:
				pass
			try:
				item["author"] = i.css(".son2 > p:nth-child(3)  > a::text")[0].extract()
			except:
				pass
			try:
				item["name"] = i.css(".son1 > h1::text")[0].extract()
			except:
				pass
			try:
				item["dynasty"] = i.css(".son2 > p:nth-child(2)::text")[0].extract()
			except:
				pass
			yield item
		for href in response.css(".son2 > span > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
