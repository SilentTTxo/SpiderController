
BOT_NAME = 'menuN6'

SPIDER_MODULES = ['menuN6.spiders']
NEWSPIDER_MODULE = 'menuN6.spiders'

ITEM_PIPELINES = {
    'menuN6.pipelines.Menun6Pipeline': 800,
}
    