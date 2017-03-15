
BOT_NAME = 'S2'

SPIDER_MODULES = ['S2.spiders']
NEWSPIDER_MODULE = 'S2.spiders'

ITEM_PIPELINES = {
    'S2.pipelines.S2Pipeline': 800,
}
    