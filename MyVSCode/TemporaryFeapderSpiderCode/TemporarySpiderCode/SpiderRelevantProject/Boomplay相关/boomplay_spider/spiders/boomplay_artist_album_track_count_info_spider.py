# -*- coding: utf-8 -*-
"""
Created on 2023-09-19 15:13:18
---------
@summary:
---------
@author: QiuQiuRen
@description：
    用来收集歌手下的歌曲及专辑数目（仅页面展示为准）
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import BoomplayArtistAlbumTrackCountInfoDataItem


class BoomplayArtistAlbumTrackCountInfoSpider(feapder.BatchSpider):

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

    def start_requests(self, task):
        task_id = task.id
        task_boomplay_artist_id = task.boomplay_artist_id
        yield feapder.Request(url='https://www.boomplay.com/artists/'+task_boomplay_artist_id,
            task_id=task_id,
            task_boomplay_artist_id=task_boomplay_artist_id
        )

    def parse(self, request, response):
        # # 提取网站title
        # print(response.xpath("//title/text()").extract_first())
        # # 提取网站描述
        # print(response.xpath("//meta[@name='description']/@content").extract_first())
        # print("网站地址: ", response.url)
        if str(request.task_boomplay_artist_id) == "43630":
            yield self.update_task_batch(request.task_id, -1)
        else:
            boomplay_artist_album_track_count_info_data_item = BoomplayArtistAlbumTrackCountInfoDataItem()
            boomplay_artist_album_track_count_info_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
            boomplay_artist_album_track_count_info_data_item['track_counts'] = response.xpath('//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[1]/h2/span/text()').extract_first()[1:-1]
            boomplay_artist_album_track_count_info_data_item['album_counts'] = response.xpath('//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[2]/h2/span/text()').extract_first()[1:-1]
            boomplay_artist_album_track_count_info_data_item['source'] = '非洲以外地区采集'
            boomplay_artist_album_track_count_info_data_item['batch'] = self.batch_date
            yield boomplay_artist_album_track_count_info_data_item
            yield self.update_task_batch(request.task_id, 1) 
    
    
    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response,e):
        yield request
        yield self.update_task_state(request.task_id, -1)


if __name__ == "__main__":
    spider = BoomplayArtistAlbumTrackCountInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BoomplayArtistAlbumTrackCountInfoSpider爬虫")

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
    # python boomplay_artist_album_track_count_info_spider.py --start_master  # 添加任务
    # python boomplay_artist_album_track_count_info_spider.py --start_worker  # 启动爬虫
