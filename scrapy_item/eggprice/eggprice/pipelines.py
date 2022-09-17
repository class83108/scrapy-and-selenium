# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from .settings import *
import pymysql

class EggpricePipeline:
    def process_item(self, item, spider):
        print(item)
        return item
class CsvPipeline(object):
    def __init__(self):
        self.file = open('data_meat_egg_price.csv', 'wb')
        #預設utf8，想用excel開啟需要big5
        self.exporter = CsvItemExporter(self.file, encoding = 'big5')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

class MysqlPipeline(object):
    def open_spider(self, spider):
        """爬蟲程序開始時，只執行一次，資料庫連接"""
        self.db = pymysql.connect(host = MYSQL_HOST, user = MYSQL_USER, password=MYSQL_PWD, db = MYSQL_DB, charset=CHARSET)
        self.cur = self.db.cursor()
        print('open_spider is running')
    def process_item(self, item, spider):
        ins = 'insert into egg_meat_price values(%s, %s, %s, %s, %s, %s)'
        list =[
            item['id'],
        item['date'],
        item['meat_ab2'],
        item['meat_l2'],
        item['meat_south'],
        item['egg']
        ]
        self.cur.execute(ins, list)
        self.db.commit()
        return item
    def close_spider(self, spider):
        self.cur.close()
        self.db.close()
        print('close_spider is running')