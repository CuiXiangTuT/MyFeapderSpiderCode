# -*- coding: utf-8 -*-
"""
Created on 2023-10-12 15:39:10
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
import json
import re
import warnings
import httpx
from datetime import datetime
from pprint import pprint




class MyTestAirspider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            'Accept-Language': "en,zh-CN;q=0.9,zh;q=0.8",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):   
        url="https://music.youtube.com/browse/MPREb_U0IQlVX84p0"
        yield feapder.Request(url=url)

    def parse(self, request, response):
        print(response.url)
        

if __name__ == "__main__":
    MyTestAirspider().start()