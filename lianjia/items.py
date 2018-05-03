# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# 自定义项目类的地方，也就是爬虫获取到数据之后，传入管道文件(piplines.py)的载体
import scrapy


class ZuFangItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    createYear = scrapy.Field()
    content = scrapy.Field()
    wuyeprice = scrapy.Field()
    wycompany = scrapy.Field()
    kaifa = scrapy.Field()
    dongshu = scrapy.Field()
    hushu = scrapy.Field()
    position = scrapy.Field()
