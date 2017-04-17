import scrapy
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from disease.items import DiseaseItem

class DiseaseSpider(scrapy.Spider):
	name="disease"
	start_urls = ["http://jbk.39.net/bw_t1/"]
	def parse(self,response):
		# for i in response.css(""):
		# 	item = DiseaseItem()
		# 	try:
		# 		item["symptomAll"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["isProtect"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["name"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["people"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["section"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["clinicalExamination"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["infectiousness"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["synopsis"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["part"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["otherName"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	try:
		# 		item["symptom"] = i.css("#")[0].extract()
		# 	except:
		# 		pass
		# 	yield item
		href = response.css(".sp-a")[0]
		url = href.extract()
		print(url)
		yield scrapy.Request(url)

	def basePageParse(self,response):
		pass

	def synopsisPageParse(self,response):
		pass

	def symptomPageParse(self,response):
		pass

	def checkPageParse(self,response):
		pass