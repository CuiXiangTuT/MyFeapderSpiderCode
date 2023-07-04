# -*- coding: utf-8 -*-
"""
Created on 2023-05-09 15:13:05
---------
@summary:
---------
@author: QiuQiuRen
@description: 
    此程序用于抓取Boomplay榜单数据
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *
import re
import json
import copy


class BoomplayChartDataDailySpider(feapder.BatchSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        # REDISDB_IP_PORTS="localhost:6379",
        # REDISDB_USER_PASS="",
        # REDISDB_DB=0,
        MYSQL_IP = "122.115.36.92",
        MYSQL_PORT = 3306,
        MYSQL_DB = "music_data",
        MYSQL_USER_NAME = "crawler",
        MYSQL_USER_PASS = "crawler.mysql"
    )

    def download_midware(self, request):
        request.headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request
    
    def add_task(self):
        sql = """
        UPDATE `chart_boomplay_batch_task`
        SET state=0
        """
        self._mysqldb.update(sql)

    def start_requests(self, task):
        # "id", "region_en_abbreviation", "chart_region", "crawl_chart_country", "chart_site", "chart_type", "update_frequency", "chart_language", "chart_segment"
        task_id = task.id
        task_region_en_abbreviation = task.region_en_abbreviation
        task_chart_region= task.chart_region
        task_crawl_chart_country = task.crawl_chart_country
        task_chart_site = task.chart_site
        task_chart_type = task.chart_type
        task_update_frequency = task.update_frequency
        task_chart_language = task.chart_language
        task_chart_segment = task.chart_segment
        task_front_end_web = task.get("front-end web")
        yield feapder.Request(url=task_front_end_web, task_id=task_id, task_region_en_abbreviation=task_region_en_abbreviation, task_chart_region=task_chart_region,
            task_crawl_chart_country=task_crawl_chart_country, task_chart_site=task_chart_site, task_chart_type=task_chart_type, task_update_frequency=task_update_frequency,
            task_chart_language=task_chart_language, task_chart_segment=task_chart_segment
        )

    def parse(self, request, response):
        """
        榜单页数据需要入库4个：分别为 1.榜单数据表 2.歌手任务表 3.专辑任务表 4.歌曲任务表
        1.榜单页数据：chart_data = chart_data_daily_boomplay_item.ChartDataDailyBoomplayItem()
        :param request:
        :param response:
        :return:
        """
        # 每日榜单数据item
        chart_data = ChartDataDailyBoomplayItem()
        # 1.抓取平台
        chart_data['chart_site'] = request.task_chart_site
        # 2.榜单抓取日期
        chart_data['chart_release_date'] = self.batch_date
        # 3.榜单歌曲表/榜单歌手表
        chart_data['chart_type'] = request.task_chart_type
        # 4.榜单名
        chart_data['chart_name'] = response.xpath('.//section[@class="text"]/h1/text()').extract_first().lower()
        # 5.榜单部分
        chart_data['chart_segment'] = request.task_chart_segment
        # 6.国家地区
        chart_data['chart_region'] = request.task_region_en_abbreviation
        # 7.国家
        country = request.task_crawl_chart_country
        pattern = r'[a-zA-Z]+\’*[a-z]*'
        chart_data['crawl_chart_country'] = str(re.findall(pattern, country)[0]).lower()
        # 8.更新频次
        chart_data['update_frequency'] = request.task_update_frequency
        # 9.chart_language
        chart_data['chart_language'] = request.task_chart_language

        li_list = response.xpath('.//ol[contains(@class,"noneSelect") and contains(@class,"morePart_musics")]/li')
        for per_track_info in li_list:
            chart_data_track_info = copy.deepcopy(chart_data)
            # 8.歌曲id
            chart_data_track_info['song_id'] = per_track_info.xpath('.//a[@class="songName"]/@href').extract_first().split('/')[-1].split('?')[0]
            # 9.歌曲名
            chart_data_track_info['song_name'] = per_track_info.xpath('.//a[@class="songName"]/text()').extract_first().replace("&amp;","&").replace("&#039;","'").lower()
            # 10.歌手id
            chart_data_track_info['chart_artist_id'] = per_track_info.xpath('.//a[@class="artistName"]/@href').extract_first().split('/')[-1].split('?')[0]
            # 11.歌手名
            name1 = per_track_info.xpath('.//a[@class="artistName"]/text()').extract_first()
            chart_data_track_info['chart_artist_name'] = name1.replace("&amp;","&").replace("&#039;","'").lower()
            # 12.专辑id
            chart_data_track_info["album_id"] = per_track_info.xpath('.//a[@class="albumName"]/@href').extract_first().split('/')[-1].split('?')[0]
            # 13.专辑名
            chart_data_track_info["album_name"] = str(per_track_info.xpath('.//a[@class="albumName"]/text()').extract_first()).replace("&amp;","&").replace("&#039;","'").lower()
            # 14.歌曲时长
            duration = per_track_info.xpath('.//time/text()').extract_first()
            h, m, s = ("00:" + duration).strip().split(":") if len(duration.split(":")) == 2 else duration.strip().split(":")
            chart_data_track_info['duration'] = int(h) * 3600 + int(m) * 60 + int(s)
            # 15.排名
            chart_data_track_info['rank'] = per_track_info.xpath('.//div[@class="serialNum"]/text()').extract_first()
            # 排名无变化
            ranking_state_no_change = per_track_info.xpath('.//div[@class="rankingState "]/text()').extract_first() if per_track_info.xpath('.//div[@class="rankingState "]') else ''
            # 排名上升
            ranking_state_ranking_up = per_track_info.xpath('.//div[contains(@class,"rankingState") and contains(@class,"ranking_up")]/text()').extract_first() if per_track_info.xpath('.//div[contains(@class,"rankingState") and contains(@class,"ranking_up")]') else ''
            # 排名下降
            ranking_state_ranking_down = per_track_info.xpath('.//div[contains(@class,"rankingState") and contains(@class,"ranking_down")]/text()').extract_first() if per_track_info.xpath('.//div[contains(@class,"rankingState") and contains(@class,"ranking_down")]') else ''
            chart_data_track_info["ranking_state_change"] = ranking_state_no_change if ranking_state_no_change else (ranking_state_ranking_up if ranking_state_ranking_up else '-'+ranking_state_ranking_down)
            # 17.批次
            chart_data_track_info['batch'] = self.batch_date
            chart_data_track_info['note'] = ''

            """
            # 2.歌手任务表：boomplay_artist_info_batch_task_item
            # """
            artist_info_task_item = BoomplayArtistInfoBatchTaskItem()
            artist_info_task_item['boomplay_artist_id'] = chart_data_track_info['chart_artist_id']
            artist_info_task_item['boomplay_artist_name'] = chart_data_track_info['chart_artist_name']

            """
            3.专辑任务表：boomplay_album_info_batch_task_item
            """
            album_info_task_item = BoomplayAlbumInfoBatchTaskItem()
            album_info_task_item['album_id'] = per_track_info.xpath('.//a[@class="albumName"]/@href').extract_first().split('/')[-1].split('?')[0]

            """
            4.歌曲任务表：boomplay_track_info_batch_task_item
            """
            track_info_task_item = BoomplayTrackInfoBatchTaskItem()
            track_info_task_item["track_id"] = chart_data_track_info["song_id"]

            yield chart_data_track_info
            yield artist_info_task_item
            yield album_info_task_item
            yield track_info_task_item
        yield self.update_task_batch(request.task_id, 1) 

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response,e):
        yield request
        yield self.update_task_batch(request.task_id, -1)


if __name__ == "__main__":
    spider = BoomplayChartDataDailySpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BoomplayChartDataDailySpider爬虫")

    parser.add_argument(
        "--start_master",
        action="store_true",
        help="添加任务",
        function=spider.start_monitor_task,
    )
    parser.add_argument(
        "--start_worker", action="store_true", help="启动爬虫", function=spider.start
    )

    parser.start()

    # 直接启动
    # spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python boomplay_chart_data_daily_spider.py --start_master  # 添加任务
    # python boomplay_chart_data_daily_spider.py --start_worker  # 启动爬虫
