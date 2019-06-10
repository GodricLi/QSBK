# -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from qiubaiFB.items import QiubaifbItem
"""获取糗百网站中糗图的所有url"""


class RedisqbSpider(RedisCrawlSpider):
    name = 'redisQB'
    # allowed_domains = ['www.qiushibaike.com']
    # start_urls = ['http://www.qiushibaike.com/']

    # 调度器队列名称，和start_url含义一样
    redis_key = 'qiushikaike'
    link = LinkExtractor(allow=r'/pic/page/\d+')  # /pic/page/35/?s=5143104,去掉s，正则\d+表示数字
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        div_list = response.xpath('//div[@id="content-left"]/div')
        for div in div_list:
            img_url = 'https:' + div.xpath('.//div[@class="thumb"]/a/img/@src').extract_first()
            item = QiubaifbItem()
            item['img_url'] = img_url

            yield item

