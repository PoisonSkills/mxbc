import scrapy
from ..items import TxmoivesItem


class TxmsSpider(scrapy.Spider):
    name = 'txms'
    allowed_domains = ['v.qq.com']
    start_urls = [
        'https://v.qq.com/channel/cartoon?listpage=1&channel=cartoon&iarea=1']
    offset = 0

    def parse(self, response):
        items = TxmoivesItem()
        lists = response.xpath('//div[@class="list_item"]')
        for i in lists:
            items['name'] = i.xpath('./a/@title').get()
            items['desc'] = i.xpath('./div/div/@title').get()
            items['url'] = i.xpath('./div/a/@href').get()

            yield items

        if self.offset < 120:
            self.offset += 30
            url = 'https://v.qq.com/channel/cartoon?listpage=1&channel=cartoon&iarea=1'.format(
                str(self.offset))
            yield scrapy.Request(url=url, callback=self.parse)