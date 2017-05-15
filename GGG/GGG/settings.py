
BOT_NAME = 'GGG'

SPIDER_MODULES = ['GGG.spiders']
NEWSPIDER_MODULE = 'GGG.spiders'

ITEM_PIPELINES = {
    'GGG.pipelines.GggPipeline': 800,
}
    