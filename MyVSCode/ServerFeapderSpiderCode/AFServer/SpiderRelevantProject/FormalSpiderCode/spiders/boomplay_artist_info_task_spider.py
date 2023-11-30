# -*- coding: utf-8 -*-
"""
Created on 2023-05-09 15:48:54
---------
@summary:
---------
@author: QiuQiuRen
@description: 
    此程序仅作用：采集歌手详情页数据，
    包括歌曲及专辑，存至【歌手-歌曲映射表】、【歌手-专辑映射表】、【歌曲任务表】、【专辑任务表】
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *
import re
import json
import copy
from feapder.utils import tools
from feapder.utils.log import log


class BoomplayArtistInfoTaskSpider(feapder.BatchSpider):
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
        update_state_sql = "UPDATE boomplay_artist_info_batch_task SET {} = 0 WHERE {} = -1".format(self._task_state,self._task_state)
        self._mysqldb.update(update_state_sql)

    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self,task):
        # "gmg_artist_name", "boomplay_artist_id","boomplay_artist_name"
        task_id = task.id
        task_boomplay_artist_id = task.boomplay_artist_id
        yield feapder.Request(url='https://www.boomplay.com/artists/' + task_boomplay_artist_id,
                              task_id=task_id,task_boomplay_artist_id=task_boomplay_artist_id)


    def parse(self, request, response):
        if str(request.task_boomplay_artist_id) == "43630":
            yield self.update_task_batch(request.task_id, -1)
        else:
            page = response.xpath('.//div[@id="page404"]')
            if len(page):
                yield self.update_task_batch(request.task_id, -1)
            else:
                """
                仅采集歌曲id、专辑id、歌手-歌曲映射、歌手-专辑映射
                """
                try:
                    # 一、歌曲信息任务表相关字段
                    # 获取歌曲数量
                    track_amount = int(response.xpath('.//li[@data-show="T"]/h2/span/text()').extract_first()[1:-1])
                    if track_amount == 0:
                        pass
                    else:
                        # 获取标签页的歌曲信息
                        li_list = response.xpath('.//ol[contains(@class,"noneSelect") and contains(@class,"morePart_musics")]/li')
                        for per_li in li_list:
                            # 【歌手歌曲映射表】
                            boomplay_artist_track_item = BoomplayArtistTrackBatchDataItem()
                            # 【歌曲任务表】
                            track_info_task_item = BoomplayTrackInfoBatchTaskItem()
                            # 获取歌曲id
                            track_info_task_item["track_id"] = per_li.xpath('.//div[@class="songNameWrap "]/a/@href').extract_first().split('/')[-1].split('?')[0]
                            boomplay_artist_track_item['boomplay_artist_id'] = request.task_boomplay_artist_id
                            boomplay_artist_track_item['track_id'] = track_info_task_item["track_id"]
                            yield track_info_task_item
                            yield self.add_new_task('boomplay_track_info_batch_task',track_info_task_item.to_dict)
                            yield boomplay_artist_track_item
                        
                        # 如果歌曲数量超过100，需要另做操作处理 
                        if track_amount>100:
                            page_num = track_amount // 100 + 2
                            for page_no in range(2,page_num):
                                url = "https://www.boomplay.com/artistsSongMore_part/{}?songTotal={}&page={}".format(request.boomplay_artist_id,track_amount,page_no)
                                headers={
                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
                                }
                                yield feapder.Request(url=url,headers=headers,callback=self.parse_track_page,boomplay_artist_id=request.boomplay_artist_id)
                except:
                    # 当前页面歌手没有歌曲相关数据，那么直接忽略
                    pass
                    
                try:
                    # 获取专辑数量
                    album_amount = int(response.xpath('.//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[2]/h2/span/text()').extract_first()[1:-1])
                    if album_amount > 0:
                        album_info_list = response.xpath('.//ul[@class="morePart_albums"]/li')
                        for per_album_info in album_info_list:
                            # 【专辑任务表】
                            album_info_task = BoomplayAlbumInfoBatchTaskItem()
                            # 【歌手专辑映射表】
                            artist_album_map = BoomplayArtistAlbumBatchDataItem()

                            album_info_task["album_id"] = per_album_info.xpath(".//a/@href").extract_first().split('/')[-1].split('?')[0]
                            artist_album_map['album_id'] = per_album_info.xpath(".//a/@href").extract_first().split('/')[-1].split('?')[0]
                            # 歌手专辑映射表：boomplay_artist_id
                            artist_album_map["boomplay_artist_id"] = request.task_boomplay_artist_id
                            yield album_info_task
                            yield self.add_new_task('boomplay_album_info_batch_task',album_info_task.to_dict)
                            yield artist_album_map

                    # 如果专辑数量超过100，需要另做操作处理 
                    if int(album_amount) > 100:
                        page_amount = int(album_amount) // 100 +2
                        for page_no in range(2,page_amount):
                            album_page_url = "https://www.boomplay.com/artists_part/albums/{}?page={}".format(request.boomplay_artist_id,page_no)
                            headers={
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
                            }
                            yield feapder.Request(url=album_page_url,headers=headers,callback=self.parse_album_page,boomplay_artist_id=request.boomplay_artist_id)
                except:
                    # 当前歌手页面没有专辑相关数据，那么直接忽略
                    pass
                yield self.update_task_batch(request.task_id, 1)

    def parse_track_page(self,request,response):
        """
        对歌曲数量超过100的页面进行相应的数据处理
        """
        li_list = response.xpath('.//ol[contains(@class,"noneSelect") and contains(@class,"morePart_musics")]/li')
        for per_li in li_list:
            # 【歌曲任务表】
            track_info_task_item = BoomplayTrackInfoBatchTaskItem()
            # 【歌手-歌曲映射表】
            boomplay_artist_track_item = BoomplayArtistTrackBatchDataItem()
            # 获取歌曲id
            track_info_task_item["track_id"] = per_li.xpath('.//div[@class="songNameWrap "]/a/@href').extract_first().split('/')[-1].split('?')[0]
            boomplay_artist_track_item['track_id'] = track_info_task_item["track_id"]
            boomplay_artist_track_item['boomplay_artist_id'] = request.boomplay_artist_id
            yield track_info_task_item
            yield self.add_new_task('boomplay_track_info_batch_task',track_info_task_item.to_dict)
            yield boomplay_artist_track_item

    def parse_album_page(self,request,response):
        """
        对专辑数量超过100的页面进行相应的数据处理
        """
        album_list = response.xpath('.//ul[@class="morePart_albums"]/li')
        boomplay_artist_id = request.boomplay_artist_id
        for per_li in album_list:
            # 【专辑任务表】
            album_info_task = BoomplayAlbumInfoBatchTaskItem()
            # 【歌手专辑映射表】
            artist_album_map = BoomplayArtistAlbumBatchDataItem()
            
            album_info_task["album_id"] = per_li.xpath(".//a/@href").extract_first().split('/')[-1].split('?')[0]
            artist_album_map['boomplay_artist_id'] = boomplay_artist_id
            artist_album_map["album_id"] = per_li.xpath(".//a/@href").extract_first().split('/')[-1].split('?')[0]
            yield album_info_task
            yield self.add_new_task('boomplay_album_info_batch_task',album_info_task.to_dict)
            yield artist_album_map
    

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
    spider = BoomplayArtistInfoTaskSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BoomplayArtistInfoTaskSpider爬虫")

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
    # python boomplay_artist_info_task_spider.py --start_master  # 添加任务
    # python boomplay_artist_info_task_spider.py --start_worker  # 启动爬虫
