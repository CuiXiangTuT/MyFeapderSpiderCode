# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 10:55:26
---------
@summary:
---------
@author: QiuQiuRen
@description：
    旨在采集歌手歌曲、专辑信息，主要涉及歌曲id、专辑id、播放列表id
    1.添加歌曲id至歌曲任务表：boomplay_track_info_batch_task
    2.添加专辑id至专辑任务表：boomplay_album_info_batch_task
    3.添加歌手歌曲映射至歌手歌曲映射表：boomplay_artist_track_batch_data
    4.添加歌手专辑映射至歌手专辑映射表：boomplay_artist_album_batch_data
    5.添加播放列表id至播放列表任务表：boomplay_playlists_info_batch_task
    6.添加歌手播放列表映射至歌手播放列表映射表：boomplay_artist_playlist_batch_data
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *


class CrawlBoomplayArtistAlbumTrackInfoTaskSpider(feapder.BatchSpider):
    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self,task):
        task_id = task.id
        task_boomplay_artist_id = task.boomplay_artist_id
        yield feapder.Request(url='https://www.boomplay.com/artists/{task_artist_id}'.format(task_artist_id=task_boomplay_artist_id),
                               task_boomplay_artist_id=task_boomplay_artist_id,task_id=task_id)

    def parse(self, request, response):
        # 歌曲数量
        songs_count = int(response.xpath(
            '//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[@class="current"]/h2/span/text()').extract_first()[
                          1:-1])
        # 专辑数量
        albums_count = int(response.xpath(
            '//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[2]/h2/span/text()').extract_first()[
                           1:-1])
        # 播放列表数量
        playlists_count = int(response.xpath(
            '//div[contains(@class,"tab_label") and contains(@class,"clearfix")]/ul/li[3]/h2/span/text()').extract_first()[
                              1:-1])

        # 存在歌曲
        if songs_count:
            # 获取标签页的歌曲信息
            li_list = response.xpath('.//ol[contains(@class,"noneSelect") and contains(@class,"morePart_musics")]/li')
            for per_li in li_list:
                # 【歌曲任务表】
                boomplay_track_info_batch_task_item = BoomplayTrackInfoBatchTaskItem()
                # 获取歌曲id
                boomplay_track_info_batch_task_item["track_id"] = \
                per_li.xpath('.//div[@class="songNameWrap "]/a/@href').extract_first().split('/')[-1].split('?')[0]

                # 【歌手-歌曲映射】
                boomplay_artist_track_batch_data_item = BoomplayArtistTrackBatchDataItem()
                boomplay_artist_track_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
                boomplay_artist_track_batch_data_item['track_id'] = boomplay_track_info_batch_task_item["track_id"]
                boomplay_artist_track_batch_data_item['batch'] = self.batch_date
                yield boomplay_track_info_batch_task_item
                yield boomplay_artist_track_batch_data_item

            # 如果歌曲数量超过100，需要另做操作处理
            if songs_count > 100:
                page_num = songs_count // 100 + 2
                for page_no in range(2, page_num):
                    url = "https://www.boomplay.com/artistsSongMore_part/{}?songTotal={}&page={}".format(
                        request.task_boomplay_artist_id, songs_count, page_no)
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
                    }
                    yield feapder.Request(url=url, headers=headers, callback=self.parse_track_page,
                                          task_boomplay_artist_id = request.task_boomplay_artist_id
                                          )

        # 存在专辑
        if albums_count:
            album_info_list = response.xpath('.//ul[@class="morePart_albums"]/li')
            for per_album_info in album_info_list:
                # 【专辑任务表】
                boomplay_album_info_batch_task_item = BoomplayAlbumInfoBatchTaskItem()
                boomplay_album_info_batch_task_item["album_id"] = \
                per_album_info.xpath(".//a/@href").extract_first().split('/')[-1].split('?')[0]

                # 【歌手 专辑映射】
                boomplay_artist_album_batch_data_item = BoomplayArtistAlbumBatchDataItem()
                boomplay_artist_album_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
                boomplay_artist_album_batch_data_item['album_id'] = boomplay_album_info_batch_task_item["album_id"]
                boomplay_artist_album_batch_data_item['batch'] = self.batch_date
                yield boomplay_album_info_batch_task_item
                yield boomplay_artist_album_batch_data_item

            # 如果专辑数量超过100，需要另做操作处理
            if int(albums_count) > 100:
                page_amount = int(albums_count) // 100 + 2
                for page_no in range(2, page_amount):
                    album_page_url = "https://www.boomplay.com/artists_part/albums/{}?page={}".format(
                        request.task_boomplay_artist_id, page_no)
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
                    }
                    yield feapder.Request(url=album_page_url, headers=headers, callback=self.parse_album_page,
                                          task_boomplay_artist_id = request.task_boomplay_artist_id
                                          )

        # 存在播放列表
        if playlists_count:
            playlists_info_list = response.xpath('//ul[@class="morePart_playlists"]/li')
            for per_li in playlists_info_list:
                # 【播放列表任务表】
                boomplay_playlist_info_batch_task_item = BoomplayPlaylistInfoBatchTaskItem()
                boomplay_playlist_info_batch_task_item['boomplay_playlist_id'] = per_li.xpath(".//a/@href").extract_first().split('/')[-1].split('?')[0]
                # 【歌手 播放列表 映射】
                boomplay_artist_playlist_batch_data_item = BoomplayArtistPlaylistBatchDataItem()
                boomplay_artist_playlist_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
                boomplay_artist_playlist_batch_data_item['boomplay_playlist_id'] = boomplay_playlist_info_batch_task_item['boomplay_playlist_id']
                boomplay_artist_playlist_batch_data_item['batch'] = self.batch_date
                yield boomplay_playlist_info_batch_task_item
                yield boomplay_artist_playlist_batch_data_item

            if playlists_count>100:
                page_amount = int(playlists_count) // 100 + 2
                for page_no in range(2,page_amount):
                    playlist_url = "https://www.boomplay.com/artists_part/playlists/{task_artist_id}?page={page_no}".format(
                        task_artist_id=request.task_boomplay_artist_id,
                        page_no=page_no
                    )
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
                    }
                    yield feapder.Request(url=playlist_url,headers=headers,
                                          task_boomplay_artist_id =  request.task_boomplay_artist_id,
                                          callback=self.parse_playlist_page)

        yield self.update_task_state(request.task_id, 1)

    # 对歌曲数量超过100的页面进行相应的数据处理
    def parse_track_page(self, request, response):
        """
        对歌曲数量超过100的页面进行相应的数据处理
        """
        li_list = response.xpath('.//ol[contains(@class,"noneSelect") and contains(@class,"morePart_musics")]/li')
        for per_li in li_list:
            # 【歌手-歌曲映射】
            boomplay_artist_track_batch_data_item = BoomplayArtistTrackBatchDataItem()
            # 【歌曲任务表】
            boomplay_track_info_batch_task_item = BoomplayTrackInfoBatchTaskItem()

            # 获取歌曲id
            boomplay_track_info_batch_task_item["track_id"] = \
            per_li.xpath('.//div[@class="songNameWrap "]/a/@href').extract_first().split('/')[-1].split('?')[0]
            boomplay_artist_track_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
            boomplay_artist_track_batch_data_item['track_id'] = boomplay_track_info_batch_task_item["track_id"]
            boomplay_artist_track_batch_data_item['batch'] = self.batch_date
            yield boomplay_track_info_batch_task_item
            yield boomplay_artist_track_batch_data_item


    # 对专辑数量超过100的页面进行相应的数据处理
    def parse_album_page(self, request, response):
        """
        对专辑数量超过100的页面进行相应的数据处理
        """
        album_list = response.xpath('.//ul[@class="morePart_albums"]/li')
        for per_li in album_list:
            # 【专辑任务表】
            boomplay_album_info_batch_task_item = BoomplayAlbumInfoBatchTaskItem()
            # 【歌手 专辑映射】
            boomplay_artist_album_batch_data_item = BoomplayArtistAlbumBatchDataItem()
            boomplay_album_info_batch_task_item["album_id"] = per_li.xpath(".//a/@href").extract_first().split('/')[-1].split('?')[0]

            boomplay_artist_album_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
            boomplay_artist_album_batch_data_item['album_id'] = boomplay_album_info_batch_task_item["album_id"]
            boomplay_artist_album_batch_data_item["batch"] = self.batch_date
            yield boomplay_album_info_batch_task_item
            yield boomplay_artist_album_batch_data_item


    # 对播放列表超过100的页面进行数据处理
    def parse_playlist_page(self,request,response):
        """
        对播放列表超过100的页面进行数据处理
        :param request:
        :param response:
        :return:
        """
        playlist_list = response.xpath('//ul[@class="morePart_playlists"]//li')
        for per_li in playlist_list:
            # 【播放列表任务表】
            boomplay_playlist_info_batch_task_item = BoomplayPlaylistInfoBatchTaskItem()
            # 【歌手 播放列表 映射】
            boomplay_artist_playlist_batch_data_item = BoomplayArtistPlaylistBatchDataItem()
            boomplay_playlist_info_batch_task_item['boomplay_playlist_id'] = per_li.xpath('.//a/@href').extract_first().split('/')[-1].split('?')[0]
            boomplay_artist_playlist_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
            boomplay_artist_playlist_batch_data_item['boomplay_playlist_id'] = boomplay_playlist_info_batch_task_item['boomplay_playlist_id']
            boomplay_artist_playlist_batch_data_item['batch'] = self.batch_date
            yield boomplay_playlist_info_batch_task_item
            yield boomplay_artist_playlist_batch_data_item



if __name__ == "__main__":
    spider = CrawlBoomplayArtistAlbumTrackInfoTaskSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlBoomplayArtistAlbumTrackInfoTaskSpider爬虫")

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
    # python crawl_boomplay_artist_songs_albums_playlists_task_spider.py --start_master  # 添加任务
    # python crawl_boomplay_artist_songs_albums_playlists_task_spider.py --start_worker  # 启动爬虫
