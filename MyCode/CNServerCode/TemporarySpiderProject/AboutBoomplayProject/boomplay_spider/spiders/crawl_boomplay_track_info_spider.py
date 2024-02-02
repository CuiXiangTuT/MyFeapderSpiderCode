# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 10:56:27
---------
@summary:
---------
@author: QiuQiuRen
@description：
    旨在获取歌曲页面下的信息：
        歌曲页面存在两种情况：
        1.正常打开，并且存在歌曲信息。样例：https://www.boomplay.com/songs/124784147
        2.无法正常打开，丢失版权。样例：https://www.boomplay.com/songs/1921625777

        添加任务：
            1.添加capture_artist_id至歌手任务表
            2.添加歌曲名至歌曲名清理表boomplay_track_name_cleaned_data
"""

import feapder
from feapder import ArgumentParser
import json
from items.boomplay_info_item import *


class CrawlBoomplayTrackInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def my_init_task(self):
        sql = "update {task_table} set {state} = 0".format(
            task_table=self._task_table,
            state=self._task_state,
        )
        return self._mysqldb.update(sql)

    def download_midware(self, request):
        request.headers = {
            'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_track_id = task.track_id
        url = 'https://www.boomplay.com/songs/{task_track_id}'.format(task_track_id=task_track_id)
        yield feapder.Request(url=url,
                              task_id=task_id,
                              task_track_id=task_track_id)

    def parse(self, request, response):
        """
        :param request:
        :param response:
        :return:
        """
        # 判断歌曲页面是否正常打开显示
        is_exists_banner = response.xpath(
            '//article[contains(@class,"summaryWrap") and contains(@class,"summary_album")]')
        if is_exists_banner:
            script_json_data = response.re(
                r'type="application/ld\+json">(.*?)</script>')[0].replace(
                '\t', '').replace('\n', '').strip()
            json_data = json.loads(script_json_data, strict=False)
            # ========================================================================
            # 一、歌曲信息相关字段
            boomplay_track_info_batch_data_item = BoomplayTrackInfoBatchDataItem()
            # 1-歌曲id
            boomplay_track_info_batch_data_item['crawl_condition_track_id'] = request.task_track_id
            boomplay_track_info_batch_data_item['crawl_result_track_id'] = json_data["@id"].split("/")[-1]
            boomplay_track_info_batch_data_item["track_id"] = boomplay_track_info_batch_data_item['crawl_result_track_id']
            # 2-歌曲名
            boomplay_track_info_batch_data_item["track_name"] = json_data[
                "name"].replace("&amp;", "&").replace("&#039;",
                                                      "'").lower().strip()
            # 3-歌曲类型
            boomplay_track_info_batch_data_item["track_type"] = str(
                json_data["@type"]).lower()
            # 4-歌曲封面
            boomplay_track_info_batch_data_item["track_image"] = json_data["image"]
            # 5-专辑id
            is_exists_album_id= json_data["inAlbum"]["@id"].split("/")[-1]
            if is_exists_album_id:
                boomplay_track_info_batch_data_item["album_id"] = is_exists_album_id
            else:
                boomplay_track_info_batch_data_item["album_id"] = None
            # 6-歌曲时长
            duration = json_data["duration"].replace('PT', '').replace(
                'M', ':').replace("S", '')
            h, m, s = ("00:" + duration).strip().split(":") if len(
                duration.split(":")) == 2 else duration.strip().split(":")
            boomplay_track_info_batch_data_item[
                "duration"] = int(h) * 3600 + int(m) * 60 + int(s)
            # 7-歌手id
            boomplay_track_info_batch_data_item["capture_artist_id"] = response.xpath(
                './/div[@class="ownerWrapOutForSong"]/a/@href').extract_first(
            ).split("/")[-1]
            # 8-歌手名capture_artist_name
            artist_name_get = ''.join(
                response.xpath('.//a[@class="ownerWrap"]/strong/text()').
                    extract()).strip().lower()
            if "artist" in artist_name_get:
                capture_artist_name = str(artist_name_get.split(":", 1)[1])
                if capture_artist_name.strip():
                    boomplay_track_info_batch_data_item["capture_artist_name"] = capture_artist_name.strip().replace("&amp;", "&").replace("&#039;", "'").lower()
                else:
                    boomplay_track_info_batch_data_item["capture_artist_name"] = capture_artist_name
            else:
                boomplay_track_info_batch_data_item["capture_artist_name"]  = artist_name_get
            # 9-歌手封面
            boomplay_track_info_batch_data_item["capture_artist_image"] = response.xpath(
                './/div[contains(@class,"default") and contains(@class,"default_artist ")]/div/@style'
            ).extract_first().split("url")[1][2:-2]
            # 10-专辑封面
            try:
                boomplay_track_info_batch_data_item[
                    "capture_album_image"] = response.xpath(
                    './/div[contains(@class,"default") and contains(@class,"default_album")]/div/@style'
                ).extract_first().split('(')[1][1:-2]
            except:
                boomplay_track_info_batch_data_item["capture_album_image"] = ""
            # 11-专辑名
            try:

                album_name_get = ''.join(
                    response.xpath(
                        './/a[contains(@class,"ownerWrap_album") and contains(@class,"ownerWrap")]/strong/text()'
                    ).extract()).strip().lower()
                boomplay_track_info_batch_data_item[
                    "capture_album_name"] = album_name_get.split(
                    ":", 1)[1].replace("&amp;", "&").replace(
                    "&#039;", "'"
                ) if "album" in album_name_get else album_name_get
            except:
                boomplay_track_info_batch_data_item["capture_album_name"] = ""
            # 12-专辑id
            try:
                capture_album_id = response.xpath(
                    './/a[contains(@class,"ownerWrap_album") and contains(@class,"ownerWrap")]/@href'
                ).extract_first().split("/")[-1]
                if capture_album_id:
                    boomplay_track_info_batch_data_item["capture_album_id"] = capture_album_id
                else:
                    boomplay_track_info_batch_data_item["capture_album_id"] = None
            except:
                boomplay_track_info_batch_data_item["capture_album_id"] = None

            # 13-喜欢数
            is_exists_like_banner = response.xpath(
                './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]')
            if is_exists_like_banner:
                boomplay_track_info_batch_data_item["track_favorite_count"] = response.xpath(
                    './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]/@data-count'
                ).extract_first()
            else:
                boomplay_track_info_batch_data_item["track_favorite_count"] = None
            # 14-分享数
            is_exists_share_banner = response.xpath(
                './/button[contains(@class,"btn_share") and contains(@class,"share_event")]')
            if is_exists_share_banner:
                boomplay_track_info_batch_data_item["track_share_count"] = response.xpath(
                    './/button[contains(@class,"btn_share") and contains(@class,"share_event")]/@data-count'
                ).extract_first()
            else:
                boomplay_track_info_batch_data_item["track_share_count"] = None

            # 15-评论数
            is_exists_comment_banner = response.xpath(
                './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]')
            if is_exists_comment_banner:
                boomplay_track_info_batch_data_item["track_comment_count"] = response.xpath(
                    './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]/@data-count'
                ).extract_first()
            else:
                boomplay_track_info_batch_data_item["track_comment_count"] = None
            # 16-曲风
            try:
                boomplay_track_info_batch_data_item["genre"] = response.xpath(
                    './/section[@class="songDetailInfo"]/ul/li[1]/span/text()'
                ).extract_first().lower()
            except:
                boomplay_track_info_batch_data_item["genre"] = ""
            # 17-发行年份
            try:
                boomplay_track_info_batch_data_item["publish_date"] = response.xpath(
                    './/section[@class="songDetailInfo"]/ul/li[2]/span/text()'
                ).extract_first().strip()
            except:
                boomplay_track_info_batch_data_item["publish_date"] = ''
            # 18-发行年份-修正
            if boomplay_track_info_batch_data_item["publish_date"]== "":
                boomplay_track_info_batch_data_item['fix_publish_date'] = None
            elif len(boomplay_track_info_batch_data_item["publish_date"])==4:
                boomplay_track_info_batch_data_item['fix_publish_date'] = boomplay_track_info_batch_data_item["publish_date"] + "-01-01"
            elif len(boomplay_track_info_batch_data_item["publish_date"])>4 and len(boomplay_track_info_batch_data_item["publish_date"])<10:
                boomplay_track_info_batch_data_item['fix_publish_date'] = None
            elif len(boomplay_track_info_batch_data_item["publish_date"]) < 4 and len(boomplay_track_info_batch_data_item["publish_date"]) > 1:
                boomplay_track_info_batch_data_item['fix_publish_date'] = None
            else:
                boomplay_track_info_batch_data_item['fix_publish_date'] = boomplay_track_info_batch_data_item["publish_date"]
            # 19-歌词链接
            try:
                # 获取歌曲歌词
                boomplay_track_info_batch_data_item["lyrics_url"] = response.xpath(
                    './/div[@class="lyrics"]/a/@href').extract_first()
                track_info_data_url = boomplay_track_info_batch_data_item["lyrics_url"]
                yield feapder.Request(
                    url=track_info_data_url,
                    callback=self.parse_lyrics_info,
                    boomplay_track_info_batch_data_item=boomplay_track_info_batch_data_item,
                    task_note=request.task_note)
            except:
                boomplay_track_info_batch_data_item["lyrics_url"] = ""
                boomplay_track_info_batch_data_item["batch"] = self.batch_date
                boomplay_track_info_batch_data_item["lyrics"] = ""
                yield boomplay_track_info_batch_data_item

            # ========================================================================
            # 二、歌曲名清理表相关字段
            boomplay_track_name_cleaned_data_item = BoomplayTrackNameCleanedDataItem()
            boomplay_track_name_cleaned_data_item['track_id'] = boomplay_track_info_batch_data_item['track_id']
            boomplay_track_name_cleaned_data_item['track_name'] = boomplay_track_info_batch_data_item['track_name']
            yield boomplay_track_name_cleaned_data_item



            # 三、歌曲采集情况相关字段
            boomplay_track_info_crawl_situation_record_batch_data_item = BoomplayTrackInfoCrawlSituationRecordBatchDataItem()
            boomplay_track_info_crawl_situation_record_batch_data_item['track_id'] = request.task_track_id
            boomplay_track_info_crawl_situation_record_batch_data_item['track_infomation_remarks'] = "EI"
            boomplay_track_info_crawl_situation_record_batch_data_item['track_exception_info'] = ""
            boomplay_track_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
            yield boomplay_track_info_crawl_situation_record_batch_data_item
            yield self.update_task_batch(request.task_id, 1)
        else:
            """
            歌曲页面无法正常打开
            """
            boomplay_track_info_crawl_situation_record_batch_data_item = BoomplayTrackInfoCrawlSituationRecordBatchDataItem()
            boomplay_track_info_crawl_situation_record_batch_data_item['track_id'] = request.task_track_id
            boomplay_track_info_crawl_situation_record_batch_data_item['track_infomation_remarks'] = "NI"
            boomplay_track_info_crawl_situation_record_batch_data_item['track_exception_info'] = response.xpath(
                '//div[@class="noData"]/div[@class="text"]/text()').extract_first().strip()
            boomplay_track_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
            yield boomplay_track_info_crawl_situation_record_batch_data_item
            yield self.update_task_batch(request.task_id, 1)


    def parse_lyrics_info(self, request, response):
        boomplay_track_info_batch_data_item = request.boomplay_track_info_batch_data_item
        boomplay_track_info_batch_data_item["lyrics"] = ','.join(
            response.xpath('.//div[@class="lyrics"]/p/text()').extract())
        boomplay_track_info_batch_data_item["batch"] = self.batch_date
        yield boomplay_track_info_batch_data_item


if __name__ == "__main__":
    spider = CrawlBoomplayTrackInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlBoomplayTrackInfoSpider爬虫")

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
    # python crawl_boomplay_track_info_spider.py --start_master  # 添加任务
    # python crawl_boomplay_track_info_spider.py --start_worker  # 启动爬虫
