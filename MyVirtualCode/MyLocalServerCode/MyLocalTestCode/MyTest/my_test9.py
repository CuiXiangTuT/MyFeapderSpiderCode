import feapder
from feapder import ArgumentParser
from feapder.db.redisdb import RedisDB
from queue import Queue
from feapder.utils.log import log
import os
import isodate
from pprint import pprint
from datetime import datetime, timedelta
from copy import deepcopy
import re
import copy


class MyTestAirspider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        request.proxies = {"https":"http://139.84.227.201:42000"}
        # proxyMeta = "http://7hyhrj:ju340pqy@%(host)s:%(port)s" % {
        #     "host": '139.84.227.201',
        #     "port": 42000,
        # }
        # request.proxies = {
        #     "http": proxyMeta,
        #     "https": proxyMeta
        # }
        return request

    def start_requests(self):
        task_id = 1
        task_region_en_abbreviation = ""
        task_chart_region = ""
        task_crawl_chart_country = ""
        task_chart_site = ""
        task_chart_type = ""
        task_update_frequency = ""
        task_chart_language = ""
        task_chart_segment = ""
        task_front_end_web = "https://www.boomplay.com/playlists/2491279?from=charts"
        yield feapder.Request(
            url=task_front_end_web,
            task_id=task_id,
            task_region_en_abbreviation=task_region_en_abbreviation,
            task_chart_region=task_chart_region,
            task_crawl_chart_country=task_crawl_chart_country,
            task_chart_site=task_chart_site,
            task_chart_type=task_chart_type,
            task_update_frequency=task_update_frequency,
            task_chart_language=task_chart_language,
            task_chart_segment=task_chart_segment)

    def parse(self, request, response):
        print(request.proxies)
        """
        榜单页数据需要入库4个：分别为 1.榜单数据表 2.歌手任务表 3.专辑任务表（忽略） 4.歌曲任务表
        1.榜单页数据：chart_data = chart_data_daily_boomplay_item.ChartDataDailyBoomplayItem()
        :param request:
        :param response:
        :return:
        """
        # 每日榜单数据item
        chart_data = dict()
        # 1.抓取平台
        chart_data['chart_site'] = request.task_chart_site
        # 2.榜单抓取日期
        # chart_data['chart_release_date'] = self.batch_date
        # 3.榜单歌曲表/榜单歌手表
        chart_data['chart_type'] = request.task_chart_type
        # 4.榜单名
        chart_data['chart_name'] = response.xpath(
            './/section[@class="text"]/h1/text()').extract_first()
        # 5.榜单部分
        chart_data['chart_segment'] = request.task_chart_segment
        # 6.国家地区
        chart_data['chart_region'] = request.task_region_en_abbreviation
        # 7.国家
        country = request.task_crawl_chart_country
        pattern = r'[a-zA-Z]+\’*[a-z]*'
        chart_data['crawl_chart_country'] = ""
        # 8.更新频次
        chart_data['update_frequency'] = request.task_update_frequency
        # 9.chart_language
        chart_data['chart_language'] = request.task_chart_language

        li_list = response.xpath(
            './/ol[contains(@class,"noneSelect") and contains(@class,"morePart_musics")]/li'
        )
        for per_track_info in li_list:
            chart_data_track_info = copy.deepcopy(chart_data)
            # 8.歌曲id
            chart_data_track_info['song_id'] = per_track_info.xpath(
                './/a[@class="songName"]/@href').extract_first().split(
                '/')[-1].split('?')[0]
            # 9.歌曲名
            chart_data_track_info['song_name'] = per_track_info.xpath(
                './/a[@class="songName"]/text()').extract_first().replace(
                "&amp;", "&").replace("&#039;", "'")
            # 10.歌手id
            chart_data_track_info['chart_artist_id'] = per_track_info.xpath(
                './/a[@class="artistName"]/@href').extract_first().split(
                '/')[-1].split('?')[0]
            # 11.歌手名
            name1 = per_track_info.xpath(
                './/a[@class="artistName"]/text()').extract_first()
            chart_data_track_info['chart_artist_name'] = name1.replace(
                "&amp;", "&").replace("&#039;", "'")
            # 12.专辑id
            chart_data_track_info["album_id"] = per_track_info.xpath(
                './/a[@class="albumName"]/@href').extract_first().split(
                '/')[-1].split('?')[0]
            # 13.专辑名
            chart_data_track_info["album_name"] = str(
                per_track_info.xpath('.//a[@class="albumName"]/text()').
                    extract_first()).replace("&amp;", "&").replace("&#039;",
                                                                   "'")
            # 14.歌曲时长
            duration = per_track_info.xpath('.//time/text()').extract_first()
            h, m, s = ("00:" + duration).strip().split(":") if len(
                duration.split(":")) == 2 else duration.strip().split(":")
            chart_data_track_info[
                'duration'] = int(h) * 3600 + int(m) * 60 + int(s)
            # 15.排名
            chart_data_track_info['rank'] = per_track_info.xpath(
                './/div[@class="serialNum"]/text()').extract_first()
            # 排名无变化
            ranking_state_no_change = per_track_info.xpath(
                './/div[@class="rankingState "]/text()').extract_first(
            ) if per_track_info.xpath(
                './/div[@class="rankingState "]') else ''
            # 排名上升
            ranking_state_ranking_up = per_track_info.xpath(
                './/div[contains(@class,"rankingState") and contains(@class,"ranking_up")]/text()'
            ).extract_first() if per_track_info.xpath(
                './/div[contains(@class,"rankingState") and contains(@class,"ranking_up")]'
            ) else ''
            # 排名下降
            ranking_state_ranking_down = per_track_info.xpath(
                './/div[contains(@class,"rankingState") and contains(@class,"ranking_down")]/text()'
            ).extract_first() if per_track_info.xpath(
                './/div[contains(@class,"rankingState") and contains(@class,"ranking_down")]'
            ) else ''
            chart_data_track_info[
                "ranking_state_change"] = ranking_state_no_change if ranking_state_no_change else (
                ranking_state_ranking_up if ranking_state_ranking_up else
                '-' + ranking_state_ranking_down)
            print(chart_data_track_info)



if __name__ == "__main__":
    MyTestAirspider().start()
