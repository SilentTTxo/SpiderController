
BOT_NAME = 'diease3'

SPIDER_MODULES = ['diease3.spiders']
NEWSPIDER_MODULE = 'diease3.spiders'

ITEM_PIPELINES = {
    'diease3.pipelines.Diease3Pipeline': 800,
}
    