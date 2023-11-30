# -*- coding: utf-8 -*-
"""
Created on 2023-02-20 01:56:07
---------
@summary:
---------
@author: AirWolf
"""
import copy

import feapder
from feapder import ArgumentParser
import json
from items.boomplay_info_item import *
from feapder.utils import tools
from feapder.utils.log import log

class BoomplayAlbumInfoSpider(feapder.BatchSpider):
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
    
    def add_task(self):
        update_state_sql = "UPDATE boomplay_album_info_batch_task SET {} = 0 WHERE {} = -1".format(self._task_state,self._task_state)
        self._mysqldb.update(update_state_sql)
        
    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }

    def start_requests(self, task):
        # "id", "album_id"
        task_id = task.id
        task_album_id = task.album_id
        url = "https://www.boomplay.com/albums/{}".format(task_album_id)
        yield feapder.Request(url=url, task_id=task_id, task_album_id=task_album_id)

    def parse(self, request, response):
        try:
            # 专辑信息表
            album_info_item = BoomplayAlbumInfoBatchDataItem()
            # 1-crawl_album_id 
            album_info_item["crawl_album_id"] = request.task_album_id
            script_json_data = response.re(r'type="application/ld\+json">(.*?)</script>')[0].replace('\t','').replace('\n','').strip()
            json_data = json.loads(script_json_data,strict=False)
            # 2-album_id
            album_info_item["album_id"] = json_data["@id"].split("/")[-1]
            # 3-album_name
            album_info_item["album_name"] = json_data["name"].replace("&amp;","&").replace("&#039;","'").strip().lower()
            # 4-专辑类型
            album_info_item["album_type"] = str(json_data["@type"]).lower().strip()
            # 5-专辑封面
            album_info_item["album_image"] = json_data["image"]
            # 6-album_info
            if len(response.xpath('.//span[@class="description_content"]/text()').extract_first().strip()):
                album_info_item["album_info"] = str(response.xpath('.//span[@class="description_content"]/text()').extract_first()).strip().lower()
            else:
                album_info_item["album_info"] = ""
            try:
                # 7-专辑下的歌曲数量
                album_info_item["album_track_count"] = response.xpath(
                    './/h2[@class="searchSongsMenuWrap_h"]/cite/text()').extract_first()[1:-1]
                # 8-歌手id
                album_info_item["boomplay_artist_id"] = json_data["byArtist"][0]["@id"].split("/")[-1]

                # 9-喜欢数
                album_info_item["album_favorite_count"] = response.xpath(
                    './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]/@data-count').extract_first()
                # 10-分享数
                album_info_item["album_share_count"] = response.xpath(
                    './/button[contains(@class,"btn_share") and contains(@class,"share_event")]/@data-count').extract_first()
                # 11-评论数
                album_info_item["album_comment_count"] = response.xpath(
                    './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]/@data-count').extract_first()
                album_info_item['batch'] = self.batch_date
                yield album_info_item
                
                # 歌曲信息
                if int(album_info_item["album_track_count"])>0:
                    track_ol_list = response.xpath('.//ol[contains(@class,"noneSelect") and contains(@class,"morePart_musics")]/li')
                    for per_track in track_ol_list:
                        # 歌曲任务表数据
                        track_info_task = BoomplayTrackInfoBatchTaskItem()
                        # 12-歌曲id
                        track_info_task["track_id"] = per_track.xpath('.//a[@class="songName"]/@href').extract_first().split('/')[-1].split('?')[0]
                        # 专辑歌曲映射表数据
                        album_track_map = BoomplayAlbumTrackBatchDataItem()
                        album_track_map['album_id'] = album_info_item["album_id"]
                        album_track_map["track_id"] = track_info_task["track_id"]
                        boomplay_artist_track_item = BoomplayArtistTrackBatchDataItem()
                        boomplay_artist_track_item['boomplay_artist_id'] = album_info_item["boomplay_artist_id"]
                        boomplay_artist_track_item['track_id'] = track_info_task["track_id"]
                        yield boomplay_artist_track_item
                        yield track_info_task
                        yield self.add_new_task('boomplay_track_info_batch_task',track_info_task.to_dict)
                        yield album_track_map
                    
                else:
                    # 7-专辑下的歌曲数量
                    album_info_item["album_track_count"] = 0
                    # 8-歌手id
                    album_info_item["boomplay_artist_id"] = json_data["byArtist"][0]["@id"].split("/")[-1]
                    # 9-喜欢数
                    album_info_item["album_favorite_count"] = 0
                    # 10-分享数
                    album_info_item["album_share_count"] = 0
                    # 11-评论数
                    album_info_item["album_comment_count"] = 0
                    album_info_item['batch'] = self.batch_date
                    yield album_info_item
                yield self.update_task_batch(request.task_id,1)
            except:
                yield self.update_task_batch(request.task_id,1)
        except:
            yield self.update_task_state(request.task_id, -1)
    

    def add_new_task(self, table,data):
        sql = tools.make_insert_sql(
            table, data,insert_ignore=True
        )
        if self._mysqldb.update(sql):
            log.debug("添加任务成功: %s" % sql)
        else:
            log.error("添加任务失败")
    

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response,e):
        yield request
        yield self.update_task_state(request.task_id, -1)


if __name__ == "__main__":
    spider = BoomplayAlbumInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BoomplayAlbumInfoSpider爬虫")

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
    # python boomplay_album_info_spider.py --start_master  # 添加任务
    # python boomplay_album_info_spider.py --start_worker  # 启动爬虫
