
BOT_NAME = 'GGG2'

SPIDER_MODULES = ['GGG2.spiders']
NEWSPIDER_MODULE = 'GGG2.spiders'

ITEM_PIPELINES = {
    'GGG2.pipelines.Ggg2Pipeline': 800,
}
    