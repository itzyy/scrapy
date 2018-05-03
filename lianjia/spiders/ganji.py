#!/usr/bin/python
# coding=utf8
_author_ = 'zouyan'

import scrapy
from lianjia.items import ZuFangItem
from scrapy.linkextractors import LinkExtractor
import re


class GanjiSpdier(scrapy.Spider):
    name = "xiaoqu"
    start_urls = ['https://sh.lianjia.com/xiaoqu/']

    # 开始解析区域信息
    def parse(self, response):
        le_area = LinkExtractor(allow=r'/[a-zA-Z0-9]+/$', restrict_xpaths="//div[@data-role='ershoufang']/div[1]")
        links = le_area.extract_links(response)

        # 爬取区域信息
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_node)

    # 爬取节点信息
    def parse_node(self,response):
        le_node = LinkExtractor(allow=r'/[a-zA-Z0-9]+/$', restrict_xpaths="//div[@data-role='ershoufang']/div[2]")
        links = le_node.extract_links(response)
        # 爬取节点信息
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_info)

    # 爬取小区信息和下一页信息
    def parse_info(self,response):
        # 解析小区信息
        le_xiaoqu = LinkExtractor(allow=r'^https://sh.lianjia.com/xiaoqu/\d+/$', restrict_xpaths="//div[@class='content']")
        links = le_xiaoqu.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_item)
        # 解析下一页
        pagedata = response.xpath("//div/@page-data").re("\d+")
        totalPage = int(pagedata[0])
        curPage = int(pagedata[1])
        if totalPage > curPage:
            link = '%s%s%s%s' % (response.url.split("pg")[0], 'pg', curPage + 1, "/")
            yield scrapy.Request(link, callback=self.parse_info)

    # 爬取小区详细信息
    def parse_item(self,response):
        zuFangItem = ZuFangItem()
        # 获得标题
        name = response.xpath("//h1[@class='detailTitle']/text()").extract()[0]
        # 获取地址
        address = response.xpath('//div[@class="xiaoquDetailHeader"]//div[@class="detailHeader fl"]//div[@class="detailDesc"]/text()').extract()[0]
        # 获得房价(平米价)
        price = response.xpath("//span[@class='xiaoquUnitPrice']/text()").extract()
        # 小区坐标
        script = response.xpath("//script/text()").extract()
        position = re.findall(r"resblockPosition:'(\d+.\d+,\d+.\d+)'", script[11])[0]
        if price:
            price=price[0]
        else:
            price='暂无参考均价'
        l_content = response.xpath("//div[@class='xiaoquOverview']//div[@class='xiaoquInfo']/div/span[@class='xiaoquInfoContent']/text()").extract()
        zuFangItem['name'] = name.strip()
        zuFangItem['address'] = address.strip()
        zuFangItem['price'] = price.strip()
        zuFangItem['content'] = l_content[0].strip()
        zuFangItem['createYear'] = l_content[1].strip()
        zuFangItem['wuyeprice'] = l_content[2].strip()
        zuFangItem['wycompany'] = l_content[3].strip()
        zuFangItem['kaifa'] = l_content[4].strip()
        zuFangItem['dongshu'] = l_content[5].strip()
        zuFangItem['hushu'] = l_content[6].strip()
        zuFangItem['position'] = position
        yield zuFangItem

