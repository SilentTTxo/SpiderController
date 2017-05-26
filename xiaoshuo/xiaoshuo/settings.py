
BOT_NAME = 'xiaoshuo'

SPIDER_MODULES = ['xiaoshuo.spiders']
NEWSPIDER_MODULE = 'xiaoshuo.spiders'

ITEM_PIPELINES = {
    'xiaoshuo.pipelines.XiaoshuoPipeline': 800,
}
    