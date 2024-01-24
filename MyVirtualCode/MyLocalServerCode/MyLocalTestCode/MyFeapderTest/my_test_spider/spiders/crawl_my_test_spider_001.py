# -*- coding: utf-8 -*-
"""
Created on 2023-10-11 11:07:46
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from params import *
from html import unescape
import re

"""
# all-time
更改前网站：https://bajao.pk/sectionPlaylist/100/All-Time-Hits/506
更改后网站：https://bajao.pk/sectionPlaylist/163/All-Time-Hits/506
状态：已采集
bajao_data_alltime = {'plId': '506', 'secId': '100', 'contentType': 'PLAYLIST'} # 13 已采集

更改前网站：https://bajao.pk/sectionPlaylist/100/Trending/541 
更改后网站：https://bajao.pk/sectionPlaylist/163/Trending/541    
状态：未采集
数据库存在数据：71
数据录入错误！
# trending
bajao_data_trending = {'plId': '541', 'secId': '100', 'contentType': 'PLAYLIST'} # 18 未采集
更改前网站：
更改后网站：
状态：采集
说明：未知来源，错误录入至https://bajao.pk/sectionPlaylist/100/Trending/541条件下
# pakistan
bajao_data_pakistan = {'page': 'FULLTRACK', 'sIndex': 0,'fIndex': 100} # 未知，71

Pakistani Hits 未采集
更改前网站：https://bajao.pk/playlist/156/Pakistani%20Hits?cid=7927577
更改后网站：https://bajao.pk/playlist/156/anything
状态：未采集


更改前网站：https://bajao.pk/sectionPlaylist/170/Punjabi-Hits/737
更改后网站：https://bajao.pk/sectionPlaylist/212/Punjabi-Hits/737
状态：已采集
# Punjabi-Hits
bajao_data_punjabi = {'plId': '737', 'secId': '212', 'contentType': 'PLAYLIST'} # 25 已采集


"""
"""
https://bajao.pk/sectionPlaylist/100/All-Time-Hits/506   改成    https://bajao.pk/sectionPlaylist/163/All-Time-Hits/506
https://bajao.pk/sectionPlaylist/100/Trending/541        改成    https://bajao.pk/sectionPlaylist/163/Trending/541    
https://bajao.pk/sectionPlaylist/170/Punjabi-Hits/737    改成    https://bajao.pk/sectionPlaylist/212/Punjabi-Hits/737
https://bajao.pk/playlist/156/Pakistani%20Hits?cid=7927577     https://bajao.pk/playlist/156/anything
"""

class CrawlMyTestSpider001(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = bajao_headers
        return request

    def start_requests(self):
        # url = 'https://bajao.pk/api/sections/playlist/v2/content?siteid='
        # # data = bajao_data_alltime
        # # data = bajao_data_trending
        # data = bajao_data_punjabi
        url = 'https://bajao.pk/api/home/sections/v2?siteid='
        data = bajao_data_pakistan
        yield feapder.Request(url,data=data)

    def parse(self, request, response):
        data_json = response.json
        chart_songs = data_json['respData'] or []
        if 'home' in request.url:
            for chart_ in chart_songs:
                if chart_["title"] == 'Pakistani Hits':
                    chart_songs = chart_['playLists'][0]['dataList']
                    chart_songs = [chart_song['data'] for chart_song in chart_songs]
                    break
        for idx in range(len(chart_songs)):
            item = dict()
            chart_song = chart_songs[idx]
            item['rank'] = idx + 1
            song_url = "{}/{}".format(chart_song['contentId'],
                                      self.handle_bajao_title_to_url(chart_song['contentTitle']))
            item['song_id'] = song_url
            item['song_name'] = unescape(chart_song['contentTitle'])
            item['chart_artist_id'] = chart_song['artistId']
            item['chart_artist_name'] = unescape(chart_song['artistTitle']).lower()  # .replace(',', ';')
            item['duration'] = chart_song['duration']
            item['views'] = chart_song['streamCount']
            print(item)

    @staticmethod
    def handle_bajao_title_to_url(title):
        if not title: return '-'
        title = re.sub(r'\s+', '-', title, re.S)
        title = re.sub(r'[\W\s]', '-', title, re.S)
        return title


if __name__ == "__main__":
    CrawlMyTestSpider001().start()