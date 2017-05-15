
BOT_NAME = 'menu2'

SPIDER_MODULES = ['menu2.spiders']
NEWSPIDER_MODULE = 'menu2.spiders'

ITEM_PIPELINES = {
    'menu2.pipelines.Menu2Pipeline': 800,
}
    