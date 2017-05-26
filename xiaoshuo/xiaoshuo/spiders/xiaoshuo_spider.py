import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from xiaoshuo.items import XiaoshuoItem

class XiaoshuoSpider(scrapy.Spider):
	name="xiaoshuo"
	start_urls = ["http://quanxiaoshuo.com/xuanhuan/1/"]
	def parse(self,response):
		for href in response.css(".list_content > .cc2 > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url,self.dataParse)

		for nexthref in response.css("#pagenav > a::attr(href)"):
			url = nexthref.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
	def dataParse(self,response):
		for i in response.css("html"):
			item = XiaoshuoItem()
			try:
				item["zuozhe"] = i.css(".w2 > a::text")[0].extract()
			except:
				pass
			try:
				item["timu"] = i.css("h1 > a::text")[0].extract()
			except:
				pass
			yield item
