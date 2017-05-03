
BOT_NAME = 't1'

SPIDER_MODULES = ['t1.spiders']
NEWSPIDER_MODULE = 't1.spiders'

ITEM_PIPELINES = {
    't1.pipelines.T1Pipeline': 800,
}
    