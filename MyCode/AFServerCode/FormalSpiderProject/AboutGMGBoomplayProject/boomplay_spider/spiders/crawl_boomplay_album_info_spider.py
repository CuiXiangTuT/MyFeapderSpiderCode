# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 10:55:58
---------
@summary:
---------
@author: QiuQiuRen
@description:
    旨在获取专辑页面下的信息
    存在3种情况：
        1.专辑页面正常显示，存在专辑信息、歌曲信息，样例：https://www.boomplay.com/albums/66073915
        2.专辑页面正常显示，存在专辑信息，不存在歌曲信息，样例：https://www.boomplay.com/albums/11504072
        3.专辑页面无法正常显示，样例：https://www.boomplay.com/albums/660739198

    相关表：专辑信息表、专辑-歌曲映射表、歌曲任务表
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *
import json


class CrawlBoomplayAlbumInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def my_init_task(self):
        sql = "update {task_table} set {task_state} = 0".format(
            task_table=self._task_table,
            task_state=self._task_state,
        )
        return self._mysqldb.update(sql)

    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_album_id = task.album_id
        url = "https://www.boomplay.com/albums/{task_album_id}".format(task_album_id=task_album_id)
        yield feapder.Request(url=url, task_id=task_id, task_album_id=task_album_id)

    def parse(self, request, response):
        # 对专辑页面进行解析
        # 判断页面是否存在专辑信息标签：<article class="summaryWrap summary_album">
        is_exists_banner = response.xpath(
            '//article[contains(@class,"summaryWrap") and contains(@class,"summary_album")]')
        if is_exists_banner:
            """
            专辑页面存在专辑信息
            存在两种情况：
                1.专辑页面正常显示，存在专辑信息、歌曲信息
                2.专辑页面正常显示，存在专辑信息，不存在歌曲信息
                3.专辑无法正常显示
            """
            # =========================================================================================
            # 专辑信息表
            boomplay_album_info_batch_data_item = GmgBoomplayAlbumInfoBatchDataItem()
            # 1-crawl_album_id
            boomplay_album_info_batch_data_item["crawl_condition_album_id"] = request.task_album_id

            script_json_data = response.re(r'type="application/ld\+json">(.*?)</script>')[0].replace('\t',
                                                                                                     '').replace(
                '\n', '').strip()
            json_data = json.loads(script_json_data, strict=False)
            # 2-album_id
            boomplay_album_info_batch_data_item['crawl_result_album_id'] = json_data["@id"].split("/")[-1]
            boomplay_album_info_batch_data_item["album_id"] = json_data["@id"].split("/")[-1]
            # 3-album_name
            boomplay_album_info_batch_data_item["album_name"] = json_data["name"].replace("&amp;", "&").replace(
                "&#039;",
                "'").strip().lower()
            # 4-专辑类型
            boomplay_album_info_batch_data_item["album_type"] = str(json_data["@type"]).lower().strip()
            # 5-专辑封面
            boomplay_album_info_batch_data_item["album_image"] = json_data["image"]
            # 6-album_info
            try:
                if len(response.xpath('.//span[@class="description_content"]/text()').extract_first().strip()):
                    boomplay_album_info_batch_data_item["album_info"] = str(response.xpath(
                        './/span[@class="description_content"]/text()').extract_first()).strip().lower()
            except:
                boomplay_album_info_batch_data_item["album_info"] = ""

            # 7-喜欢数
            is_exists_like_banner = response.xpath(
                './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]')
            if is_exists_like_banner:
                boomplay_album_info_batch_data_item["album_favorite_count"] = response.xpath(
                    './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]/@data-count').extract_first()
            else:
                boomplay_album_info_batch_data_item["album_favorite_count"] = 0
            # 8-分享数
            is_exists_share_banner = response.xpath(
                './/button[contains(@class,"btn_share") and contains(@class,"share_event")]')
            if is_exists_share_banner:
                boomplay_album_info_batch_data_item["album_share_count"] = response.xpath(
                    './/button[contains(@class,"btn_share") and contains(@class,"share_event")]/@data-count').extract_first()
            else:
                boomplay_album_info_batch_data_item["album_share_count"] = 0

            # 9-评论数
            is_exists_comment_banner = response.xpath(
                './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]')
            if is_exists_comment_banner:
                boomplay_album_info_batch_data_item["album_comment_count"] = response.xpath(
                    './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]/@data-count').extract_first()
            else:
                boomplay_album_info_batch_data_item["album_comment_count"] = 0

            # 是否存在歌曲
            is_exists_inner_banner = response.xpath(
                '//article[contains(@class,"songsMenu") and contains(@class,"clearfix") and contains(@class,"searchSongsMenuParent")]')
            if is_exists_inner_banner:
                """
                专辑下存在歌曲
                """
                # 7-专辑下的歌曲数量
                boomplay_album_info_batch_data_item["album_track_count"] = response.xpath(
                    './/h2[@class="searchSongsMenuWrap_h"]/cite/text()').extract_first()[1:-1]
                boomplay_album_info_batch_data_item['batch'] = self.batch_date
                yield boomplay_album_info_batch_data_item

                # =======================================================================================================

                # 歌曲信息
                track_ol_list = response.xpath(
                    './/ol[contains(@class,"noneSelect") and contains(@class,"morePart_musics")]/li')
                for per_track in track_ol_list:
                    # 歌曲任务表数据
                    boomplay_track_info_batch_task_item = GmgBoomplayTrackInfoBatchTaskItem()
                    # 12-歌曲id
                    boomplay_track_info_batch_task_item["track_id"] = \
                    per_track.xpath('.//a[@class="songName"]/@href').extract_first().split('/')[-1].split('?')[0]
                    # 专辑歌曲映射表数据
                    boomplay_album_track_batch_data_item = GmgBoomplayAlbumTrackBatchDataItem()
                    boomplay_album_track_batch_data_item['album_id'] = boomplay_album_info_batch_data_item["album_id"]
                    boomplay_album_track_batch_data_item["track_id"] = boomplay_track_info_batch_task_item["track_id"]
                    boomplay_album_track_batch_data_item['batch'] = self.batch_date
                    yield boomplay_track_info_batch_task_item
                    yield boomplay_album_track_batch_data_item

                boomplay_album_info_crawl_situation_record_batch_data_item = GmgBoomplayAlbumInfoCrawlSituationRecordBatchDataItem()
                boomplay_album_info_crawl_situation_record_batch_data_item['album_id'] = request.task_album_id
                boomplay_album_info_crawl_situation_record_batch_data_item['album_information_remarks'] = "ET"
                boomplay_album_info_crawl_situation_record_batch_data_item['album_exception_info'] = ""
                boomplay_album_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
                yield boomplay_album_info_crawl_situation_record_batch_data_item
                yield self.update_task_batch(request.task_id, 1)

            else:
                """
                专辑下不存在歌曲
                """
                # 7-专辑下的歌曲数量
                boomplay_album_info_batch_data_item["album_track_count"] = 0
                boomplay_album_info_batch_data_item['batch'] = self.batch_date
                boomplay_album_info_crawl_situation_record_batch_data_item = GmgBoomplayAlbumInfoCrawlSituationRecordBatchDataItem()
                boomplay_album_info_crawl_situation_record_batch_data_item['album_id'] = request.task_album_id
                boomplay_album_info_crawl_situation_record_batch_data_item['album_information_remarks'] = "NT"
                album_info = response.xpath(
                    '//div[@class="noData"]/div[@class="text"]/text()').extract_first()
                if album_info:
                    boomplay_album_info_crawl_situation_record_batch_data_item['album_exception_info'] = album_info.strip()
                else:
                    boomplay_album_info_crawl_situation_record_batch_data_item['album_exception_info'] = None
                album_info_1 = response.xpath(
                    '//div[@class="notAvailableText"]//p//text()'
                ).extract()
                if album_info_1:
                    boomplay_album_info_crawl_situation_record_batch_data_item['album_exception_info'] = ','.join(
                        album_info_1)
                else:
                    boomplay_album_info_crawl_situation_record_batch_data_item['album_exception_info'] = None

                boomplay_album_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
                yield boomplay_album_info_crawl_situation_record_batch_data_item
                yield boomplay_album_info_batch_data_item
                yield self.update_task_batch(request.task_id, 1)

        else:
            """
            专辑页面无法正常显示
            """
            boomplay_album_info_crawl_situation_record_batch_data_item = GmgBoomplayAlbumInfoCrawlSituationRecordBatchDataItem()
            boomplay_album_info_crawl_situation_record_batch_data_item['album_id'] = request.task_album_id
            boomplay_album_info_crawl_situation_record_batch_data_item['album_information_remarks'] = "NC"
            boomplay_album_info_crawl_situation_record_batch_data_item['album_exception_info'] = response.xpath(
                '//div[contains(@class,"scrollView_content") and contains(@class,"pageContent")]//div[@class="noData"]//div[@class="text"]/text()').extract_first().strip()
            boomplay_album_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
            yield boomplay_album_info_crawl_situation_record_batch_data_item
            yield self.update_task_batch(request.task_id, 1)


if __name__ == "__main__":
    spider = CrawlBoomplayAlbumInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlBoomplayAlbumInfoSpider爬虫")

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
    # python crawl_boomplay_album_info_spider.py --start_master  # 添加任务
    # python crawl_boomplay_album_info_spider.py --start_worker  # 启动爬虫
