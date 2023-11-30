# -*- coding: utf-8 -*-
"""
Created on 2023-04-04 16:37:17
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
import json
import re


class Myspider(feapder.AirSpider):

    def start_requests(self):
        yield feapder.Request("https://www.boomplay.com/artists/11876062")

    def parse(self, request, response):
        # 一、歌手信息表相关字段信息
        artist_info = dict()
        # 3-crawl_artist_name
        crawl_artist_name = response.xpath('.//article[@class="pop_descriptionReadMore"]/header/h2/text()').extract_first()
        artist_info["crawl_artist_name"] = crawl_artist_name.replace("&amp;","&").replace("&#039;","'")
        # 1-gmg_artist_id
        # artist_info["gmg_artist_id"] = request.task_gmg_artist_id
        # 2-gmg_artist_name
        # artist_info["gmg_artist_name"] = request.task_gmg_artist_name
        # 匹配页面script标签里的json_data数据
        script_json_data = response.re(r'type="application/ld\+json">(.*?)</script>')[0].replace('\t','').replace('\n','').strip()
        json_data = json.loads(script_json_data)
        # 4-boomplay_artist_id
        artist_info["boomplay_artist_id"] = json_data["@id"].split("/")[-1]
        # 5-boomplay_artist_name
        artist_info["boomplay_artist_name"] = json_data["name"].replace("&amp;","&").replace("&#039;","'")
        # 6-boomplay_artist_certification
        artist_info["boomplay_artist_certification"] = 1 if response.xpath(
        './/cite[contains(@class,"default_authentic_icon") and contains(@class,"icon_personal")]') else 0
        # # 7-batch
        # artist_info["batch"] = self.batch_date
        # 8-boomplay_artist_image
        artist_info["boomplay_artist_image"] = json_data["image"]
        # 9-boomplay_artist_info
        artist_info["boomplay_artist_info"] = ''.join(
        response.xpath('.//span[@class="description_content"]/text()').extract()).strip()
        # 10-artist_favorite_count
        artist_info["artist_favorite_count"] = response.xpath(
        './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]/@data-count').extract_first()
        # 11-artist_share_count
        artist_info["artist_share_count"] = response.xpath(
        './/button[contains(@class,"btn_share") and contains(@class,"share_event")]/@data-count').extract_first()
        # 12-artist_comment_count
        artist_info["artist_comment_count"] = response.xpath(
        './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]/@data-count').extract_first()
        # 13-ranking_current
        ranking_current = response.xpath('.//div[@class="rankingCurrent"]/text()').extract_first().split("#")[
        1].strip().replace(',','')
        if '+' not in ranking_current:
            artist_info["ranking_current"] = int(float(ranking_current.replace('k',''))*1000) if 'k' in ranking_current else int((float(ranking_current.replace('m',''))*1000000) if 'm' in ranking_current else ranking_current)
        else:
            artist_info["ranking_current"] = ranking_current
        # 14-ranking_alltime
        ranking_alltime = response.xpath('.//div[@class="rankingAllTime"]/text()').extract_first().split("#")[
        1].strip().replace(',','')
        if '+' not in ranking_alltime:
            artist_info["ranking_alltime"] = int(float(ranking_alltime.replace('k',''))*1000) if 'k' in ranking_alltime else int((float(ranking_alltime.replace('m',''))*1000000) if 'm' in ranking_alltime else ranking_alltime)
        else:
            artist_info["ranking_alltime"] = ranking_alltime
        # 15-country_region
        artist_info["country_region"] = response.xpath('.//cite[@class="boomIdDisplay"]/text()').extract_first().split(':')[1].strip()
        print(artist_info)

if __name__ == "__main__":
    Myspider().start()