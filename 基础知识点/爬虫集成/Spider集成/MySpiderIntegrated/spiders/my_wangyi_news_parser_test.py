# -*- coding: utf-8 -*-
"""
Created on 2023-01-19 11:28:28
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
import datetime
from items.my_spider_integrated_wangyi_news_test_item import MySpiderIntegratedWangyiNewsTestItem
import re
import time
from feapder.dedup import Dedup


class MyWangyiNewsParserTest(feapder.BaseParser):
    def __init__(self,*args,**kwargs):
        # filter_type：去重类型，支持BloomFilter、MemoryFilter、ExpireFilter三种
        self.dedup = Dedup() # 默认是永久去重
    """
    注意 这里继承的是BaseParser，而不是Spider
    """
    # # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    # __custom_setting__ = dict(
    #     REDISDB_IP_PORTS="localhost:6379", REDISDB_USER_PASS="", REDISDB_DB=0
    # )

    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
        for i in range(2):
            if i==0:
                yield feapder.Request("https://news.163.com/special/cm_guoji/?callback=data_callback")
            else:
                yield feapder.Request("https://news.163.com/special/cm_guoji_02/?callback=data_callback")

    def parse(self, request, response):
        pattern = re.compile(r'data_callback\((.*?)\)',re.S)
        result = re.findall(pattern=pattern, string=response.text)[0]
        for per_dict in eval(result):
            # keywords处理
            if len(per_dict["keywords"]) == 0:
                item = MySpiderIntegratedWangyiNewsTestItem()
                item["title"] = per_dict["title"]
                item["channel_name"] = per_dict["channelname"]
                item["comment_url"] = per_dict["commenturl"]
                item["doc_url"] = per_dict["docurl"]
                item["img_url"] = per_dict["imgurl"]
                item["label"] = per_dict["label"]
                item["news_type"] = per_dict["newstype"]
                item["source"] = per_dict["source"]
                item["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(per_dict["time"], "%m/%d/%Y %H:%M:%S"))
                item["tienum"] = per_dict["tienum"]
                item["keywords_akey_link"] = ""
                item["keywords_keyname"] = ""
                if self.dedup.add(item):
                    item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    yield item
            else:
                for per_keywords_dict in per_dict["keywords"]:
                    item = MySpiderIntegratedWangyiNewsTestItem()
                    item["title"] = per_dict["title"]
                    item["channel_name"] = per_dict["channelname"]
                    item["comment_url"] = per_dict["commenturl"]
                    item["doc_url"] = per_dict["docurl"]
                    item["img_url"] = per_dict["imgurl"]
                    item["label"] = per_dict["label"]
                    item["news_type"] = per_dict["newstype"]
                    item["source"] = per_dict["source"]
                    item["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(per_dict["time"], "%m/%d/%Y %H:%M:%S"))
                    item["tienum"] = per_dict["tienum"]
                    item["keywords_akey_link"] = per_keywords_dict["akey_link"]
                    item["keywords_keyname"] = per_keywords_dict["keyname"]
                    if self.dedup.add(item):
                        item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        yield item


if __name__ == "__main__":
    MyWangyiNewsParserTest(redis_key="xxx:xxx").start()
