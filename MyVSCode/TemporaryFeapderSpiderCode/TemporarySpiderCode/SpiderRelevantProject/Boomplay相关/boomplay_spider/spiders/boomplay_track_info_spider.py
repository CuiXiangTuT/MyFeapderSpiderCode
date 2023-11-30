# -*- coding: utf-8 -*-
"""
Created on 2023-02-20 01:56:21
---------
@summary:
---------
@author: AirWolf
"""

import feapder
from feapder import ArgumentParser
import json
from items.boomplay_info_item import *
import re
import copy
from feapder.utils import tools
from feapder.utils.log import log


class BoomplayTrackInfoSpider(feapder.BatchSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    # __custom_setting__ = dict(
    #     # REDISDB_IP_PORTS="localhost:6379",
    #     # REDISDB_USER_PASS="",
    #     # REDISDB_DB=0,
    #     MYSQL_IP = "122.115.36.92",
    #     MYSQL_PORT = 3306,
    #     MYSQL_DB = "music_data",
    #     MYSQL_USER_NAME = "crawler",
    #     MYSQL_USER_PASS = "crawler.mysql"
    # )

    def init_task(self):
        pass

    def my_init_task(self):
        sql = "update {task_table} set {state} = 0 where {state} != -1".format(
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
        # "id", "track_id"
        task_id = task.id
        task_track_id = task.track_id
        url = 'https://www.boomplay.com/songs/{}'.format(task_track_id)
        yield feapder.Request(url=url,
                              task_id=task_id,
                              task_track_id=task_track_id)

    def parse(self, request, response):
        """
        入库数据表：1.歌曲信息表 2.专辑任务表 3.歌手任务表 
        """
        # 歌曲信息表
        track_info_batch_data_item = BoomplayTrackInfoBatchDataItem()
        # 歌手任务表
        artist_info_batch_task_item = BoomplayArtistInfoBatchTaskItem()
        # 专辑任务表
        album_info_batch_task_item = BoomplayAlbumInfoBatchTaskItem()
        # 歌曲清洗表
        track_name_cleaned_data_item = BoomplayTrackNameCleanedDataItem()

        # 1-crawl_track_id
        track_info_batch_data_item["crawl_track_id"] = request.task_track_id

        if response.xpath('//div[@class="noData"]/div[@class="text"]'):
            """
            当前页面无歌曲相关数据
            """
            yield self.update_task_state(request.task_id, -1)
        else:
            """
            存在歌曲数据
            """
            script_json_data = response.re(
                r'type="application/ld\+json">(.*?)</script>')[0].replace(
                    '\t', '').replace('\n', '').strip()
            json_data = json.loads(script_json_data, strict=False)
            # 2-歌曲id
            track_info_batch_data_item["track_id"] = json_data["@id"].split(
                "/")[-1]
            # 3-歌曲名
            track_info_batch_data_item["track_name"] = json_data[
                "name"].replace("&amp;", "&").replace("&#039;",
                                                      "'").lower().strip()
            track_name_cleaned_data_item["track_id"] = json_data["@id"].split(
                "/")[-1]
            track_name_cleaned_data_item['track_name'] = json_data[
                "name"].replace("&amp;", "&").replace("&#039;",
                                                      "'").lower().strip()
            # 4-歌曲类型
            track_info_batch_data_item["track_type"] = str(
                json_data["@type"]).lower()
            # 5-歌曲封面
            track_info_batch_data_item["track_image"] = json_data["image"]
            # 6-专辑id
            track_info_batch_data_item["album_id"] = json_data["inAlbum"][
                "@id"].split("/")[-1]
            # 7-歌曲时长
            duration = json_data["duration"].replace('PT', '').replace(
                'M', ':').replace("S", '')
            h, m, s = ("00:" + duration).strip().split(":") if len(
                duration.split(":")) == 2 else duration.strip().split(":")
            track_info_batch_data_item[
                "duration"] = int(h) * 3600 + int(m) * 60 + int(s)
            # 8-歌手id
            track_info_batch_data_item["boomplay_artist_id"] = json_data[
                "byArtist"][0]["@id"].split('/')[-1]
            # 9-歌手名boomplay_artist_id
            track_info_batch_data_item["boomplay_artist_name"] = str(
                json_data["byArtist"][0]["name"]).replace(
                    "&amp;", "&").replace("&#039;", "'").lower()
            # 10-歌手名capture_artist_name
            artist_name_get = ''.join(
                response.xpath('.//a[@class="ownerWrap"]/strong/text()').
                extract()).strip().lower()
            track_info_batch_data_item["capture_artist_name"] = str(
                artist_name_get.split(":", 1)[1]).strip(
                ).replace("&amp;", "&").replace("&#039;", "'").lower(
                ) if "artist" in artist_name_get else artist_name_get.lower()
            # 11-歌手id
            track_info_batch_data_item["capture_artist_id"] = response.xpath(
                './/div[@class="ownerWrapOutForSong"]/a/@href').extract_first(
                ).split("/")[-1]
            # 12-歌手封面
            track_info_batch_data_item["capture_artist_image"] = response.xpath(
                './/div[contains(@class,"default") and contains(@class,"default_artist ")]/div/@style'
            ).extract_first().split("url")[1][2:-2]
            try:
                # 13-专辑封面
                track_info_batch_data_item[
                    "capture_album_image"] = response.xpath(
                        './/div[contains(@class,"default") and contains(@class,"default_album")]/div/@style'
                    ).extract_first().split('(')[1][1:-2]
            except:
                track_info_batch_data_item["capture_album_image"] = ""
            try:
                # 14-专辑名
                album_name_get = ''.join(
                    response.xpath(
                        './/a[contains(@class,"ownerWrap_album") and contains(@class,"ownerWrap")]/strong/text()'
                    ).extract()).strip().lower()
                track_info_batch_data_item[
                    "capture_album_name"] = album_name_get.split(
                        ":", 1)[1].replace("&amp;", "&").replace(
                            "&#039;", "'"
                        ) if "album" in album_name_get else album_name_get
            except:
                track_info_batch_data_item["capture_album_name"] = ""
            try:
                # 15-专辑id
                track_info_batch_data_item["capture_album_id"] = response.xpath(
                    './/a[contains(@class,"ownerWrap_album") and contains(@class,"ownerWrap")]/@href'
                ).extract_first().split("/")[-1]
            except:
                track_info_batch_data_item["capture_album_id"] = ""
            # 16-喜欢数
            track_info_batch_data_item["track_favorite_count"] = response.xpath(
                './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]/@data-count'
            ).extract_first()
            # 17-分享数
            track_info_batch_data_item["track_share_count"] = response.xpath(
                './/button[contains(@class,"btn_share") and contains(@class,"share_event")]/@data-count'
            ).extract_first()
            # 18-评论数
            track_info_batch_data_item["track_comment_count"] = response.xpath(
                './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]/@data-count'
            ).extract_first()
            try:
                # 19-曲风
                track_info_batch_data_item["genre"] = response.xpath(
                    './/section[@class="songDetailInfo"]/ul/li[1]/span/text()'
                ).extract_first()
            except:
                track_info_batch_data_item["genre"] = ""
            try:
                # 20-发行年份
                track_info_batch_data_item["publish_date"] = response.xpath(
                    './/section[@class="songDetailInfo"]/ul/li[2]/span/text()'
                ).extract_first()
            except:
                track_info_batch_data_item["publish_date"] = ''
            try:
                # 21-歌词链接
                # 获取歌曲歌词
                track_info_batch_data_item["lyrics_url"] = response.xpath(
                    './/div[@class="lyrics"]/a/@href').extract_first()
                track_info_data_url = track_info_batch_data_item["lyrics_url"]
                yield feapder.Request(
                    url=track_info_data_url,
                    callback=self.parse_lyrics_info,
                    track_info_batch_data_item=track_info_batch_data_item,
                    task_note=request.task_note)
            except:
                track_info_batch_data_item["lyrics_url"] = ""
                track_info_batch_data_item["batch"] = self.batch_date
                track_info_batch_data_item["lyrics"] = ""
                yield track_info_batch_data_item

            # 添加歌手id至歌手任务表中
            try:
                if track_info_batch_data_item["capture_artist_id"] != '':
                    artist_info_batch_task_item[
                        'boomplay_artist_id'] = track_info_batch_data_item[
                            "capture_artist_id"]
                    artist_info_batch_task_item[
                        'boomplay_artist_name'] = track_info_batch_data_item[
                            "capture_artist_name"]
                    yield artist_info_batch_task_item
                else:
                    pass
            except:
                pass

            # 添加专辑id至专辑任务表中
            try:
                if track_info_batch_data_item["capture_album_id"] != '':
                    album_info_batch_task_item['album_id'] = track_info_batch_data_item["capture_album_id"]
                    yield album_info_batch_task_item
                else:
                    pass
            except:
                pass
            
            yield track_name_cleaned_data_item
            yield self.update_task_batch(request.task_id, 1)

            


    def parse_lyrics_info(self, request, response):
        track_info_batch_data_item = request.track_info_batch_data_item
        track_info_batch_data_item["lyrics"] = ','.join(
            response.xpath('.//div[@class="lyrics"]/p/text()').extract())
        track_info_batch_data_item["batch"] = self.batch_date
        yield track_info_batch_data_item

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_state(request.task_id, -1)
    

    def add_new_task(self, table,data):
        sql = tools.make_insert_sql(
            table, data,insert_ignore=True
        )
        if self._mysqldb.update(sql):
            log.debug("添加任务成功: %s" % sql)
        else:
            log.error("添加任务失败")
    

if __name__ == "__main__":
    spider = BoomplayTrackInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BoomplayTrackInfoSpider爬虫")

    parser.add_argument(
        "--start_master",
        action="store_true",
        help="添加任务",
        function=spider.start_monitor_task,
    )
    parser.add_argument("--start_worker",
                        action="store_true",
                        help="启动爬虫",
                        function=spider.start)

    parser.start()

    # 直接启动
    # spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python boomplay_track_info_spider.py --start_master  # 添加任务
    # python boomplay_track_info_spider.py --start_worker  # 启动爬虫
