
BOT_NAME = 'GGG5'

SPIDER_MODULES = ['GGG5.spiders']
NEWSPIDER_MODULE = 'GGG5.spiders'

ITEM_PIPELINES = {
    'GGG5.pipelines.Ggg5Pipeline': 800,
}
    