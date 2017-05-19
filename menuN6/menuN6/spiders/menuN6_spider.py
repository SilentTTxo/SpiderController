import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from menuN6.items import Menun6Item

class Menun6Spider(scrapy.Spider):
	name="menuN6"
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
			item = Menun6Item()
			urlList = []
			try:
				pageHref2 = i.css(".son5")[2].css("a::attr(href)")[0].extract()
				url = pageHref2
				url = urljoin_rfc(get_base_url(response), url)
				urlList.append(url)
			except:
				pass
			try:
				pageHref1 = i.css(".son5")[1].css("a::attr(href)")[0].extract()
				url = pageHref1
				url = urljoin_rfc(get_base_url(response), url)
				urlList.append(url)
			except:
				pass
			try:
				pageHref0 = i.css(".son5")[0].css("a::attr(href)")[0].extract()
				url = pageHref0
				url = urljoin_rfc(get_base_url(response), url)
				urlList.append(url)
			except:
				pass
			yield scrapy.Request(urlList[0],self.pageHref2Parse,meta={'item':item,'urlList':urlList})
	def pageHref2Parse(self,response):
		item = response.meta["item"]
		urlList = response.meta["urlList"]

		try:
			item["jianshangg"] = response.css("h1::text")[0].extract()
		except:
				pass
		yield scrapy.Request(urlList[1],self.pageHref1Parse,meta={'item':item,'urlList':urlList})
	def pageHref1Parse(self,response):
		item = response.meta["item"]
		urlList = response.meta["urlList"]

		try:
			item["chuangzuobeijing"] = response.css("h1::text")[0].extract()
		except:
				pass
		yield scrapy.Request(urlList[2],self.pageHref0Parse,meta={'item':item,'urlList':urlList})
	def pageHref0Parse(self,response):
		item = response.meta["item"]
		urlList = response.meta["urlList"]

		try:
			item["yiwen"] = response.css("h1::text")[0].extract()
		except:
				pass
		yield item
