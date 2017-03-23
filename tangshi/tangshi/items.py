import scrapy

class TangshiItem(scrapy.Item):
	content = scrapy.Field()
	author = scrapy.Field()
	name = scrapy.Field()
	dynasty = scrapy.Field()
