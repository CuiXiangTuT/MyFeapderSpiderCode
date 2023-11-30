# -*- coding: utf-8 -*-
"""
Created on 2023-10-12 18:03:36
---------
@summary:
---------
@author: QiuQiuRen
@description：
    旨在获取歌手详情页下的歌曲、专辑、播放列表的数量映射
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *


class CrawlBoomplayArtistSongsAlbumsPlaylistsCountsSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_boomplay_artist_id = task.boomplay_artist_id
        url = 'https://www.boomplay.com/artists/{}'.format(task_boomplay_artist_id)
        yield feapder.Request(url, task_id=task_id, task_boomplay_artist_id=task_boomplay_artist_id)

    def parse(self, request, response):
        # 检测歌手存在Songs、Albums、Playlists标签
        boomplay_artist_songs_albums_playlists_counts_record_batch_data_item = BoomplayArtistSongsAlbumsPlaylistsCountsRecordBatchDataItem()
        is_exists_banner = response.xpath('//div[contains(@class,"tab_label") and contains(@class,"clearfix")]')
        if is_exists_banner:
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item[
                'boomplay_artist_id'] = request.task_boomplay_artist_id
            # 歌曲数量
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['songs_count'] = int(response.xpath(
                '//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[@class="current"]/h2/span/text()').extract_first()[
                                                                                                      1:-1])
            if boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['songs_count'] == 0:
                # 信息提示
                boomplay_artist_songs_albums_playlists_counts_record_batch_data_item[
                    'songs_count_none_info'] = 'No songs in artist. Go and find more music on Boomplay.'
            else:
                # 信息提示
                boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['songs_count_none_info'] = ''
            # 专辑数量
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['albums_count'] = int(response.xpath(
                '//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[2]/h2/span/text()').extract_first()[
                                                                                                       1:-1])
            if boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['albums_count'] == 0:
                # 信息提示
                boomplay_artist_songs_albums_playlists_counts_record_batch_data_item[
                    'albums_count_none_info'] = 'No Data. Go and find more music on Boomplay.'
            else:
                # 信息提示
                boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['albums_count_none_info'] = ''
            # 播放列表数量
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['playlists_count'] = int(
                response.xpath(
                    '//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[3]/h2/span/text()').extract_first()[
                1:-1])
            if boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['playlists_count'] == 0:
                # 信息提示
                boomplay_artist_songs_albums_playlists_counts_record_batch_data_item[
                    'playlists_count_none_info'] = 'No Data. Go and find more music on Boomplay.'
            else:
                # 信息提示
                boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['playlists_count_none_info'] = ''
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['batch'] = self.batch_date
            yield boomplay_artist_songs_albums_playlists_counts_record_batch_data_item
            yield self.update_task_batch(request.task_id, 1)

            if boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['songs_count'] == \
                    boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['albums_count'] == \
                    boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['playlists_count'] == 0:
                # 当【歌曲数量】、【专辑数量】、【播放列表】均为0时，将boomplay_artist_info_batch_task表中的-
                # -->bj_crawl_artist_album_track_state置为-1，在采集歌曲、专辑、播放列表信息时直接过滤，不作采集
                update_sql = "UPDATE {task_table} SET {task_state} = -3 WHERE boomplay_artist_id={task_artist_id}".format(
                    task_table=self._task_table,
                    task_state="bj_crawl_artist_album_track_playlist_task_state",
                    task_artist_id=request.task_boomplay_artist_id
                )
                return self._mysqldb.update(update_sql)

            if boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['songs_count'] != 0 or \
                    boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['albums_count'] != 0 or \
                    boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['playlists_count'] != 0:
                # 当【歌曲数量】和【专辑数量】有一个不为0时，将boomplay_artist_info_batch_task表中的-
                # -->bj_crawl_artist_album_track_state置为0，在采集歌曲、专辑任务信息时进行添加采集
                update_sql = "UPDATE {task_table} SET {task_state} = 0 WHERE boomplay_artist_id={task_artist_id}".format(
                    task_table=self._task_table,
                    task_state="bj_crawl_artist_album_track_playlist_task_state",
                    task_artist_id=request.task_boomplay_artist_id
                )
                return self._mysqldb.update(update_sql)
        else:
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item[
                'boomplay_artist_id'] = request.task_boomplay_artist_id
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['songs_count'] = 0
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item[
                'songs_count_none_info'] = 'No songs in artist. Go and find more music on Boomplay.'
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['albums_count'] = 0
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item[
                'albums_count_none_info'] = 'No Data. Go and find more music on Boomplay.'
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['playlists_count'] = 0
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item[
                'playlists_count_none_info'] = 'No Data. Go and find more music on Boomplay.'
            boomplay_artist_songs_albums_playlists_counts_record_batch_data_item['batch'] = self.batch_date
            yield boomplay_artist_songs_albums_playlists_counts_record_batch_data_item
            yield self.update_task_batch(request.task_id, 1)

            update_sql = """
            UPDATE {task_table} SET {task_state}=-3
            WHERE boomplay_artist_id =  {task_artist_id}
            """.format(task_table=self._task_table, task_state="bj_crawl_artist_album_track_playlist_task_state",
                       task_artist_id=request.task_boomplay_artist_id
                       )
            return self._mysqldb.update(update_sql)

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request


if __name__ == "__main__":
    spider = CrawlBoomplayArtistSongsAlbumsPlaylistsInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlBoomplayArtistSongsAlbumsPlaylistsInfoSpider爬虫")

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
    # python crawl_boomplay_artist_songs_albums_playlists_counts_spider.py --start_master  # 添加任务
    # python crawl_boomplay_artist_songs_albums_playlists_counts_spider.py --start_worker  # 启动爬虫
