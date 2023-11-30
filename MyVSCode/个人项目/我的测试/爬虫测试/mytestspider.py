# -*- coding: utf-8 -*-
"""
Created on 2023-03-14 18:52:59
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from pprint import pprint
import copy
import json
from feapder.utils.log import log
import requests

class Mytestspider(feapder.AirSpider):


    def download_midware(self, request):
        # request.headers = {
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        # }
        request.headers = {
        "Content-Type": "application/json"
        }
        return request

    def start_requests(self):
        DINGDING_WARNING_URL = "https://oapi.dingtalk.com/robot/send?access_token=703c62930dcd94c6b1541956ba8a547b3b8cd4eadfc1b446d779e8fff8b16821"  # 钉钉机器人api
        info = "这里是测试"
        data = {
            "msgtype":"text",
            "text":{"content":"-----------往生堂第77代堂主胡桃-----------\n\n"+info}
        }
        yield feapder.Request(url=DINGDING_WARNING_URL,data=json.dumps(data))
        # task_country = "US"
        # artist_name_list = ["Jay Melody","Jay Melody","Jay Melody","Jay"]
        # for artist_name in artist_name_list:
        #     yield feapder.Request("https://www.boomplay.com/search/default/{}".format(artist_name),artist_name = artist_name)

    def parse(self, request, response):
        print(response.text) 


    # def parse(self, request, response):
    #     if response.xpath('.//div[@class="noData"]'):
    #         print("查不到数据")
    #     else:
    #         artist_name = request.artist_name
    #         artist_name_list = response.xpath('..//article[contains(@class,"column") and contains(@class,"column_slide") and contains(@class,"artists_column")]/div[@class="column_content"]/ul/li')
    #         is_flag = False
    #         for artist_name_li in artist_name_list:
    #             try:
    #                 boomplay_artist_name = artist_name_li.xpath('.//strong/text()').extract_first().replace("&amp;","&").replace("&#039;","'")
    #                 if boomplay_artist_name.lower().strip() == artist_name.lower().strip():
    #                     log.info("boomplay_artist_name: {}".format(boomplay_artist_name))
    #                     log.info("artist_name: {}".format(artist_name.strip().lower()))
    #                     log.info("artist_name: {}".format(boomplay_artist_name.strip().lower()))
    #                     log.info("-----------------------------------")
    #                     break
    #                 else:
    #                     pass
    #             except:
    #                 boomplay_artist_name = artist_name_li.xpath('.//strong//text()').extract_first()
    #                 log.info("Boomplay上该歌手：{} 与目标歌手:{} 不一致！".format(boomplay_artist_name,artist_name))
                


if __name__ == "__main__":
    Mytestspider().start()