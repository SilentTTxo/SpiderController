import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from S3.items import S3Item

class S3Spider(scrapy.Spider):
	name="S3"
	start_urls = ["http://www.w3school.com.cn/html5/html_5_intro.asp"]
	def parse(self,response):
		for i in response.css("#maincontent >div"):
			item = S3Item()
			try:
				item["H2"] = i.css("h2::text")[0].extract()
			except:
				pass
			yield item
		for href in response.css("li.next > a::attr(href)"):
			url = href.extract()
			url = urljoin_rfc(get_base_url(response), url)
			yield scrapy.Request(url)
