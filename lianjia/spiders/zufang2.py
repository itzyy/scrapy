# -*- coding: utf-8 -*-
# 1、获取各个区域的链接：东城区、西城区、朝阳区
# 2、获取各个区域下面的节点信息：东城-东单，西城-阜成门
# 3、获取各个节点：东单、阜成门等节点中的小区url、下一页url
# 4、获取小区的详细信息，小区的配套信息
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Zufang2Spider(CrawlSpider):
    name = 'zufang2'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://sh.lianjia.com/xiaoqu/']

    # LinkExtrator
    le_area = LinkExtractor(allow=r'/[a-zA-Z0-9]+/$',restrict_xpaths="//div[@data-role='ershoufang']/div[1]")
    # le_xiaoqu = LinkExtractor(allow=r'^https://bj.lianjia.com/xiaoqu/\d+/$', restrict_xpaths="//div[@class='content']")
    le_next = LinkExtractor(allow=r'^https://bj.lianjia.com/xiaoqu/[a-zA-Z]+/pg\d+/$',restrict_xpaths="//a")

    rules = (
        Rule(le_area,callback='parse_page'),
        # Rule(le_xiaoqu, callback='parse_item', follow=False),
        Rule(le_next,callback='parse_next'),
    )
    def parse_page(self,response):
        context = response.body_as_unicode()
        print(response.url)

    # 获取各个区域的链接
    def parse_next(self,response):
        print('==',response.url)

    def parse_xq(self,response):
        name = response.xpath("//h1[@class='detailTitle']/text()").extract()[0]
        address = response.xpath('//div[@class="xiaoquDetailHeader"]//div[@class="detailHeader fl"]//div[@class="detailDesc"]/text()').extract()[0]
        price = response.xpath("//span[@class='xiaoquUnitPrice']/text()").extract()[0]
        l_content = response.xpath("//div[@class='xiaoquOverview']//div[@class='xiaoquInfo']/div/span[@class='xiaoquInfoContent']/text()").extract()
        print('name\taddress\tprices\tcreateYear\twuyeprice\twycompany\tkaifa\tdongshu\thushu')
        print(name,'\t',address,'\t',price,'\t',l_content[0],'\t',l_content[1],'\t',l_content[2],'\t',l_content[3],'\t',l_content[4],'\t',l_content[5])
