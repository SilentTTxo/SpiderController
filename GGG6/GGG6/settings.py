
BOT_NAME = 'GGG6'

SPIDER_MODULES = ['GGG6.spiders']
NEWSPIDER_MODULE = 'GGG6.spiders'

ITEM_PIPELINES = {
    'GGG6.pipelines.Ggg6Pipeline': 800,
}
    