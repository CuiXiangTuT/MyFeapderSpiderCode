# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class BaidunewsPipeline:
    def __init__(self):
        self.conn = pymysql.Connect(host="192.168.10.133",user="root",password="123456",db="my_test_data",port=3306)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = '''
            INSERT INTO baidu_hot_news (title)
            VALUES (%s)
            '''
        self.cursor.execute(sql, (item['title']))
        return item

    def close_spider(self,spider):
        self.conn.commit()
        self.conn.close()