
BOT_NAME = 'yongzhe'

SPIDER_MODULES = ['yongzhe.spiders']
NEWSPIDER_MODULE = 'yongzhe.spiders'

ITEM_PIPELINES = {
    'yongzhe.pipelines.YongzhePipeline': 800,
}
    