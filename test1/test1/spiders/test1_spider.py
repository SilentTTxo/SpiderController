import scrapy
from test1.items import Test1Item

class Test1Spider(scrapy.Spider):
	name = "test1"
	allowed_domains = ["yicang.com"]
	start_urls = [
		"http://www.yicang.com/airports.html"
	]

	def parse(self,response):
		for href1 in response.css("ul.r2 > li > a::attr(href)"):
			url = response.urljoin(href1.extract())
			yield scrapy.Request(url, callback=self.getHref2)
		#for href in response.css("div.c_page_list.layoutfix > a::attr('href')"):
			#url = response.urljoin(response.url, href.extract())
			#if(url == "javascript:;") continue
			#yield scrapy.Request(url, callback=self.getData)

	def getHref2(self,response):
		if(len(response.css("li.next > a::attr(href)").extract()) == 0):
			return

		for sel in response.css("li.listnr7 > a::text"):
			item = Test1Item()
			item['name'] = sel.extract()
			yield item

		nexturl = response.css("li.next > a::attr(href)").extract()[0]
		nexturl = response.urljoin(nexturl)
		#print(nexturl+"\n"+response.url)
		if(nexturl != response.url):
			yield scrapy.Request(nexturl, callback=self.getHref2)
