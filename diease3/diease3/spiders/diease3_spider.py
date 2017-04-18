import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from diease3.items import Diease3Item

class Diease3Spider(scrapy.Spider):
	name="diease3"
	start_urls = ["http://zzk.xywy.com/p/a.html"]
	def parse(self,response):
		# for i in response.css(""):
		# 	item = Diease3Item()
		# 	try:
		# 		item["keShi"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["jianJie"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["mingCheng"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	yield item
		for diseasePageHref in response.css(".ks-ill-txt > div > ul > li > a::attr(href)"):
			url = diseasePageHref.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url,self.basePageParse)

		for href in response.css(".zm-list > li > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)

	def basePageParse(self,response):
		url = response.css(".dep-nav > li > a::attr(href)")[1].extract()
		url = urljoin_rfc(get_base_url(response), url)
		yield scrapy.Request(url,self.xiangXiJieShaoParse)

	def xiangXiJieShaoParse(self,response):
		item = Diease3Item()

		item["keShi"] = response.css(".nav-bar > a::text")[-2].extract()
		item["mingCheng"] = response.css(".jb-name::text")[0].extract()

		str = ""
		for i in response.css(".zz-articl > p::text"):
			str+=i.extract()

		item["jianJie"] = str
		yield item
