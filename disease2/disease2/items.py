import scrapy

class Disease2Item(scrapy.Item):
	zhengZhuang = scrapy.Field()
	jianJie = scrapy.Field()
	mingCheng = scrapy.Field()
	huanBingBiLv = scrapy.Field()
	zhiYuLv = scrapy.Field()
	keShi = scrapy.Field()
	yiGanRenQun = scrapy.Field()
	jianCha = scrapy.Field()
	yiBaoJiBing = scrapy.Field()
	jiuZhenKeShi = scrapy.Field()
