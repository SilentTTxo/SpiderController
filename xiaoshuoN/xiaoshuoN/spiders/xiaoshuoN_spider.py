import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from xiaoshuoN.items import XiaoshuonItem

class XiaoshuonSpider(scrapy.Spider):
	name="xiaoshuoN"
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
			item = XiaoshuonItem()
			urlList = []
			try:
				pageHref2 = i.css(".chapter:nth-child(3) > a::attr(href)")[0].extract()
				url = pageHref2
				url = urljoin_rfc(get_base_url(response), url)
				urlList.append(url)
			except:
				pass
			try:
				pageHref1 = i.css(".chapter:nth-child(2) > a::attr(href)")[0].extract()
				url = pageHref1
				url = urljoin_rfc(get_base_url(response), url)
				urlList.append(url)
			except:
				pass
			try:
				pageHref0 = i.css(".chapter:nth-child(1) > a::attr(href)")[0].extract()
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
			item["disanzhang"] = response.css("#content")[0].extract()
		except:
				pass
		yield scrapy.Request(urlList[1],self.pageHref1Parse,meta={'item':item,'urlList':urlList})
	def pageHref1Parse(self,response):
		item = response.meta["item"]
		urlList = response.meta["urlList"]

		try:
			item["dierzhang"] = response.css("#content")[0].extract()
		except:
				pass
		yield scrapy.Request(urlList[2],self.pageHref0Parse,meta={'item':item,'urlList':urlList})
	def pageHref0Parse(self,response):
		item = response.meta["item"]
		urlList = response.meta["urlList"]

		try:
			item["diyizhang"] = response.css("#content")[0].extract()
		except:
				pass
		yield item
