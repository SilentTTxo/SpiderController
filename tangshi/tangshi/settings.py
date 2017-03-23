
BOT_NAME = 'tangshi'

SPIDER_MODULES = ['tangshi.spiders']
NEWSPIDER_MODULE = 'tangshi.spiders'

ITEM_PIPELINES = {
    'tangshi.pipelines.TangshiPipeline': 800,
}
    