
BOT_NAME = 'disease'

SPIDER_MODULES = ['disease.spiders']
NEWSPIDER_MODULE = 'disease.spiders'

ITEM_PIPELINES = {
    'disease.pipelines.DiseasePipeline': 800,
}
    