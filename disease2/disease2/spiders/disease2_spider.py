import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from disease2.items import Disease2Item

class Disease2Spider(scrapy.Spider):
	name="disease2"
	start_urls = ["http://jib.xywy.com/html/a.html"]
	def parse(self,response):
		# for i in response.css(""):
		# 	item = Disease2Item()
		# 	try:
		# 		item["zhengZhuang"] = i.css("#")[0].extract()
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
		# 	try:
		# 		item["huanBingBiLv"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["zhiYuLv"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["keShi"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["yiGanRenQun"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["jianCha"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["yiBaoJiBing"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["jiuZhenKeShi"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	yield item
		for diseasePageHref in response.css(".fl.jblist-con-ear > div > ul > li > a::attr(href)"):
			url = diseasePageHref.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url,self.basePageParse)

		for href in response.css(".zm-list.mt10 > li > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)


	def basePageParse(self,response):
		item = Disease2Item()

		item["keShi"] = response.css(".nav-bar > a::text")[-1].extract()
		item["mingCheng"] = response.css(".jb-name::text")[0].extract()

		url = response.css(".dep-nav > li > a::attr(href)")[1].extract()
		url = urljoin_rfc(get_base_url(response), url)
		yield scrapy.Request(url,self.gaiShuParse,meta={'item':item})

	def gaiShuParse(self,response):
		item = response.meta['item']

		item["jianJie"] = response.css(".jib-articl-con > p::text")[0].extract()
		item["yiBaoJiBing"] = response.css(".articl-know")[0].css("p")[0].css("span::text")[1].extract()
		item["huanBingBiLv"] = response.css(".articl-know")[0].css("p")[1].css("span::text")[1].extract()
		item["yiGanRenQun"] = response.css(".articl-know")[0].css("p")[2].css("span::text")[1].extract()
		item["jiuZhenKeShi"] = response.css(".articl-know")[1].css("p")[0].css("span::text")[1].extract()
		item["zhiYuLv"] = response.css(".articl-know")[1].css("p")[3].css("span::text")[1].extract()

		url = response.css(".jib-nav-list")[1].css("li > a::attr(href)")[0].extract()
		url = urljoin_rfc(get_base_url(response), url)
		yield scrapy.Request(url,self.zhengZhuangParse,meta={'item':item})
		# yield items

	def zhengZhuangParse(self,response):
		item = response.meta['item']

		str = ""
		for i in response.css(".f12 > a.gre"):
			text = i.css("a::text")[0].extract()
			href = i.css("a::attr(href)")[0].extract()

			str += text + "|" + href + " "
		item["zhengZhuang"] = str

		url = response.css(".jib-nav-list")[1].css("li > a::attr(href)")[1].extract()
		url = urljoin_rfc(get_base_url(response), url)
		yield scrapy.Request(url,self.checkParse,meta={'item':item})

	def checkParse(self,response):
		item = response.meta['item']

		str = ""
		for i in response.css(".check-item > a::text"):
			str += i.extract() + " "

		item["jianCha"] = str

		yield item