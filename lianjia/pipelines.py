# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 项目管道文件，对传入的项目类中的数据进行一个清理和入库
import codecs

class ZuFangPipline(object):
    def __init__(self):
        self.file = codecs.open("sh_zufang.csv", "w", encoding="utf-8")

    # 爬虫从html分析得到数据，传入item，item被丢到管道文件中，
    def process_item(self, item, spider):
        iteminfo =self.printItem(item)
        self.file.write(iteminfo+"\n")
        # return iteminfo


    def printItem(self,item):
        return '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' \
               % \
               (item['name'],
                item['address'],
                item['price'],
                item['content'],
                item['createYear'],
                item['wuyeprice'],
                item['wycompany'],
                item['kaifa'],
                item['dongshu'],
                item['hushu'],
                item['position']
                )
