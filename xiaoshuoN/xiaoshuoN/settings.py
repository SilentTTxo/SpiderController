
BOT_NAME = 'xiaoshuoN'

SPIDER_MODULES = ['xiaoshuoN.spiders']
NEWSPIDER_MODULE = 'xiaoshuoN.spiders'

ITEM_PIPELINES = {
    'xiaoshuoN.pipelines.XiaoshuonPipeline': 800,
}
    