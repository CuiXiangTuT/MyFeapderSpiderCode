# -*- coding: utf-8 -*-
"""
Created on 2023-01-17 17:15:36
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from items.my_spider_wangyi_news_test_item import MySpiderWangyiNewsTestItem
import datetime
import time
import re
import copy


class MyWangyiNewsTest(feapder.Spider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
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
                print("第一次抓取")
                yield feapder.Request("https://news.163.com/special/cm_guoji/?callback=data_callback")
            else:
                print("第二次抓取")
                yield feapder.Request("https://news.163.com/special/cm_guoji_02/?callback=data_callback")
        


    def parse(self, request, response):
        # # 提取网站title
        # print(response.xpath("//title/text()").extract_first())
        # # 提取网站描述
        # print(response.xpath("//meta[@name='description']/@content").extract_first())
        # print("网站地址: ", response.url)
        
        pattern = re.compile(r'data_callback\((.*?)\)',re.S)
        result = re.findall(pattern=pattern, string=response.text)[0]
        for per_dict in eval(result):
            # keywords处理
            if len(per_dict["keywords"]) == 0:
                item = MySpiderWangyiNewsTestItem()
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
                item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item
            else:
                for per_keywords_dict in per_dict["keywords"]:
                    item = MySpiderWangyiNewsTestItem()
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
                    item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    yield item


if __name__ == "__main__":
    # WangyiNews(redis_key="xxx:xxx").start()
    spider = MyWangyiNewsTest.to_DebugSpider(
        redis_key="feapder:my_spider_wangyi_news_test",request=feapder.Request("https://news.163.com/special/cm_guoji/?callback=data_callback")
    )
    spider.start()

    print("第一次调试完毕，等待第二次调试")
    
    time.sleep(5)
    
    # spider1 = MyWangyiNewsTest.to_DebugSpider(
    #     redis_key="feapder:my_spider_wangyi_news_test",request=feapder.Request("https://news.163.com/special/cm_guoji_02/?callback=data_callback")
    # )
    # spider1.start()
    
    # print("第二次调试结束，程序终止")