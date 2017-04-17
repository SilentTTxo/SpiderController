import scrapy

class DiseaseItem(scrapy.Item):
	symptomAll = scrapy.Field()
	isProtect = scrapy.Field()
	name = scrapy.Field()
	people = scrapy.Field()
	section = scrapy.Field()
	clinicalExamination = scrapy.Field()
	infectiousness = scrapy.Field()
	synopsis = scrapy.Field()
	part = scrapy.Field()
	otherName = scrapy.Field()
	symptom = scrapy.Field()
