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

class MyTestAirspider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
        task_youtube_video_link = "https://www.boomplay.com/albums/64265601"
        task_id = 1
        yield feapder.Request(url=task_youtube_video_link,
                              task_youtube_video_link=task_youtube_video_link,
                              task_id=task_id
                              )

    def parse(self, request, response):
        album_info_1 = response.xpath(
            '//div[@class="notAvailableText"]//p//text()'
        ).extract()
        print(album_info_1)


if __name__ == "__main__":
    MyTestAirspider().start()