
BOT_NAME = 'test1'

SPIDER_MODULES = ['test1.spiders']
NEWSPIDER_MODULE = 'test1.spiders'

ITEM_PIPELINES = {
    'test1.pipelines.Test1Pipeline': 800,
}
    