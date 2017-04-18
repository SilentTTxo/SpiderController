
BOT_NAME = 'disease2'

SPIDER_MODULES = ['disease2.spiders']
NEWSPIDER_MODULE = 'disease2.spiders'

ITEM_PIPELINES = {
    'disease2.pipelines.Disease2Pipeline': 800,
}
    