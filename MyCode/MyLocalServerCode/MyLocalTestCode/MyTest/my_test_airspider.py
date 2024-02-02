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
            'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):   
        # ["UClyA28-01x4z60eWQ2kiNbA","UChUJa1JyBc7Lc4orkiNKKQg","UCWu91J5KWEj1bQhCBuGeJxw"]
        url="https://music.youtube.com/channel/UCL2MDNdwEtV6aYUgNjFQGZA"
        # url="https://music.youtube.com/channel/UCL2MDNdwEtV6aYUgNjFQGZA"
        yield feapder.Request(url=url)

    def parse(self, request, response):
        pattern = r"initialData\.push\({([\s\S]*?)}\);"
        response.encoding = response.apparent_encoding
        matches = re.findall(pattern, response.text)
        if len(matches) >= 2:
            second_data = matches[1]
            match = re.search(r"data: '(.*)'", second_data)
            if match:
                data_value = match.group(1)
                data = bytes(data_value, 'UTF-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
                json_data = json.loads(data)
                with open('r7.txt','w',encoding="utf-8") as f:
                    f.write(data)
        #         item = dict()
        #         # 1-歌手名
        #         item["youtube_music_artist_name"] = json_data["header"]["musicImmersiveHeaderRenderer"]["title"]["runs"][0]["text"]
        #         # 2-歌手channelid
        #         item["youtube_music_artist_channel_id"] = json_data["header"]["musicImmersiveHeaderRenderer"]["subscriptionButton"]["subscribeButtonRenderer"]["channelId"]
        #         # 3-歌手订阅数
        #         item["youtube_music_artist_subscriber_count"] = json_data["header"]["musicImmersiveHeaderRenderer"]["subscriptionButton"]["subscribeButtonRenderer"]["subscriberCountWithSubscribeText"]["runs"][0]["text"]
        #         # 4-歌手简介
        #         item["youtube_music_artist_description"] = json_data["header"]["musicImmersiveHeaderRenderer"]["description"]["runs"][0]["text"] if "description" in json_data["header"]["musicImmersiveHeaderRenderer"] else None
        #         # 5-歌手主页背景图
        #         item["youtube_music_artist_background_image_url"] = json_data["header"]["musicImmersiveHeaderRenderer"]["thumbnail"]["musicThumbnailRenderer"]["thumbnail"]["thumbnails"][0]["url"]
        #         # 6-歌手被查看次数
        #         item["views"] = json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][-1]["musicDescriptionShelfRenderer"]["subheader"]["runs"][0]["text"] if "musicDescriptionShelfRenderer" in json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"] else 0
        #         # 7-歌手所有歌曲的URL
        #         item["youtube_music_all_songs_url"] = json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicShelfRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"] if "musicShelfRenderer" in json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0] else None
        #         # if item["youtube_music_all_songs_url"]:
        #         #     pass
        #         # else:
        #         #     # 需要对页面上的歌曲进行采集添加
        #         #     pass
                
        #         # 将musicCarouselShelfRenderer单独抽出添加至一个新的空列表进行存储
        #         json_result_data = json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
        #         musicCarouselShelfRenderer_data_list = [j for j in json_result_data if "musicCarouselShelfRenderer" in j]
        #         # 8-歌手【专辑、单曲】的URL
        #         for k in musicCarouselShelfRenderer_data_list:
        #             key_label = k["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["accessibilityData"]["accessibilityData"]["label"]
        #             if key_label=="专辑":
        #                 if "navigationEndpoint" in k["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]:
        #                     item["youtube_music_all_albums_singles_url"] = k["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
        #             elif key_label=="单曲":
        #                 if "navigationEndpoint" in k["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]:
        #                     item["youtube_music_all_albums_singles_url"] = k["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
        #                 # else:
        #                 #     pass
        #             elif key_label=="视频":
        #                 item["youtube_music_all_videos_url"] = k["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
        #             elif key_label=="精选":
        #                 # 需要做列表处理
        #                 featured_list = k["musicCarouselShelfRenderer"]["contents"]
        #                 for featured_per in featured_list:
        #                     # 精选集标题
        #                     featured_dict = dict()
        #                     featured_dict["featured_title"] = featured_per["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
        #                     featured_dict["featured_url"] = featured_per["musicTwoRowItemRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
        #                     print(featured_dict)
        #             elif key_label=="粉丝可能还会喜欢":
        #                 # 需要做列表处理
        #                 fans_also_like_list = k["musicCarouselShelfRenderer"]["contents"]
        #                 for fans_also_like_per in fans_also_like_list:
        #                     # 粉丝可能还会喜欢的艺人名
        #                     fasn_also_like_dict = dict()
        #                     fasn_also_like_dict["fans_also_like_artist_name"] = fans_also_like_per["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
        #                     fasn_also_like_dict["fans_also_like_artist_channel_id"] = fans_also_like_per["musicTwoRowItemRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
        #                     fasn_also_like_dict["fans_also_like_artist_subscriber_count"] = fans_also_like_per["musicTwoRowItemRenderer"]["subtitle"]["runs"][0]["text"]
        #                     print(fasn_also_like_dict)
        #         pprint(item)
        # else:
        #     print("无法找到第二个initialData.push的值")
        
        

if __name__ == "__main__":
    MyTestAirspider().start()