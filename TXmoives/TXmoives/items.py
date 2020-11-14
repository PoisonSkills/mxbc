# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TxmoivesItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() # 名称
    desc = scrapy.Field() # 描述
    url = scrapy.Field() # 资源地址
    pass
