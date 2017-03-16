
BOT_NAME = 'S3'

SPIDER_MODULES = ['S3.spiders']
NEWSPIDER_MODULE = 'S3.spiders'

ITEM_PIPELINES = {
    'S3.pipelines.S3Pipeline': 800,
}
    