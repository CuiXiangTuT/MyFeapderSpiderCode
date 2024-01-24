# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 10:54:49
---------
@summary:
---------
@author: QiuQiuRen
@description:
    旨在获取歌手页面数据，仅包含个人信息相关，不包含专辑、歌曲方面
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *


class CrawlBoomplayArtistInfoSpider(feapder.BatchSpider):

    def init_task(self):
        pass

    def my_init_task(self):
        sql = "update {task_table} set {task_state} = 0,{task_state1}=-2,{task_state2}=-2".format(
            task_table=self._task_table,
            task_state=self._task_state,
            task_state1="bj_crawl_artist_album_track_playlist_task_state",
            task_state2="bj_crawl_songs_albums_playlists_count_state"
        )
        return self._mysqldb.update(sql)

    def add_task(self):
        """
        1.将GMG_DATA_ASSETS.gmg_artist_aka中，条件为chart_site='boomplay'，
        且id与boomplay_artist_info_batch_task表中boomplay_artist_id一致的，
        进行关联，更新boomplay_artist_info_batch_task中gmg_artist_id、gmg_artist_name、
        boomplay_artist_name等信息
        """
        update_sql = """
        UPDATE `gmg_boomplay_artist_info_batch_task` b
        INNER JOIN `GMG_DATA_ASSETS`.`gmg_artist_aka` g
        ON b.boomplay_artist_id = g.id AND g.site='boomplay'
        SET b.gmg_artist_id=g.gmg_artist_id,b.gmg_artist_name=g.gmg_artist_name,b.boomplay_artist_name=g.gmg_artist_name,b.usable=1
        """
        self._mysqldb.update(update_sql)

        """
        2.将GMG_DATA_ASSETS.gmg_artist_aka中，条件为chart_site='boomplay'，
        且id不在boomplay_artist_info_batch_task中的信息，放入至boomplay_artist_info_batch_task
        表中，进行采集
        """
        insert_sql = """
        INSERT IGNORE INTO `gmg_boomplay_artist_info_batch_task`
        (gmg_artist_id,gmg_artist_name,boomplay_artist_id,boomplay_artist_name,usable)
        SELECT `gmg_artist_id`,`gmg_artist_name`,`id`,`gmg_artist_name`,1
        FROM `GMG_DATA_ASSETS`.`gmg_artist_aka`
        WHERE site='boomplay' AND `id` NOT IN (
            SELECT boomplay_artist_id FROM `gmg_boomplay_artist_info_batch_task`
        )
        """
        self._mysqldb.add(insert_sql)



    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_gmg_artist_name = task.gmg_artist_name
        task_boomplay_artist_id = task.boomplay_artist_id
        task_boomplay_artist_name = task.boomplay_artist_name
        yield feapder.Request(url='https://www.boomplay.com/artists/{}'.format(task_boomplay_artist_id),
                              task_boomplay_artist_name=task_boomplay_artist_name, task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
                              task_gmg_artist_name=task_gmg_artist_name,
                              task_boomplay_artist_id=task_boomplay_artist_id)

    def parse(self, request, response):
        # boomplay_artist_id为43460的暂时不做采集
        if str(request.task_boomplay_artist_id) == "43630":
            boompplay_artist_info_crawl_situation_record_batch_data_item = BoomplayArtistInfoCrawlSituationRecordBatchDataItem()
            boompplay_artist_info_crawl_situation_record_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
            boompplay_artist_info_crawl_situation_record_batch_data_item[
                'boomplay_artist_id'] = request.task_boomplay_artist_id
            boompplay_artist_info_crawl_situation_record_batch_data_item['boomplay_artist_infomation_remarks'] = "NI"
            boompplay_artist_info_crawl_situation_record_batch_data_item[
                'boomplay_artist_exception_info'] = "43630暂不予采集"
            boompplay_artist_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
            yield boompplay_artist_info_crawl_situation_record_batch_data_item
            yield self.update_task_state(request.task_id, 1)
        else:
            # 查验当前歌手页面存在信息与否
            is_exist_info = response.xpath(
                '//div[contains(@class,"scrollView_content") and contains(@class,"pageContent")]/@id').extract_first()
            if is_exist_info == 'artistsDetails':
                # ========================================================================
                # 一、歌手信息相关字段
                boomplay_artist_info_batch_data_item = BoomplayArtistInfoBatchDataItem()
                # 1.gmg_artist_id
                boomplay_artist_info_batch_data_item['gmg_artist_id'] = request.task_gmg_artist_id
                # 2.gmg_artist_name
                boomplay_artist_info_batch_data_item['gmg_artist_name'] = request.task_gmg_artist_name
                # 3.crawl_condition_boomplay_artist_id
                boomplay_artist_info_batch_data_item['crawl_condition_boomplay_artist_id'] = request.task_boomplay_artist_id
                # 4.crawl_result_boomplay_artist_id
                boomplay_artist_info_batch_data_item['crawl_result_boomplay_artist_id'] = response.xpath('//link[@rel="canonical"]/@href').extract_first().split('/')[-1]
                # 5.boomplay_artist_id
                boomplay_artist_info_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
                # 6.crawl_condition_boomplay_artist_name
                boomplay_artist_info_batch_data_item['crawl_condition_boomplay_artist_name'] = request.task_gmg_artist_name
                # 7.crawl_result_boomplay_artist_name
                is_exists_vip_banner = response.xpath(
                    '//h1[contains(@class,"icon_vip") and contains(@class,"isVip")]')
                if is_exists_vip_banner:
                    crawl_result_boomplay_artist_name = response.xpath(
                        '//h1[contains(@class,"icon_vip") and contains(@class,"isVip")]/text()').extract_first()
                    if crawl_result_boomplay_artist_name:
                        boomplay_artist_info_batch_data_item['crawl_result_boomplay_artist_name'] = crawl_result_boomplay_artist_name.strip().lower()
                    else:
                        boomplay_artist_info_batch_data_item['crawl_result_boomplay_artist_name'] = crawl_result_boomplay_artist_name
                else:
                    crawl_result_boomplay_artist_name = response.xpath(
                        '//h1[contains(@class,"icon_vip ")]/text()').extract_first()
                    if crawl_result_boomplay_artist_name:
                        boomplay_artist_info_batch_data_item[
                            'crawl_result_boomplay_artist_name'] = crawl_result_boomplay_artist_name.strip().lower()
                    else:
                        boomplay_artist_info_batch_data_item[
                            'crawl_result_boomplay_artist_name'] = crawl_result_boomplay_artist_name

                # 8.boomplay_artist_name
                boomplay_artist_info_batch_data_item['boomplay_artist_name'] = boomplay_artist_info_batch_data_item['crawl_condition_boomplay_artist_name']
                # 9.boomplay_artist_certification
                vip_icon = response.xpath(
                    '//article[@class="summaryWrap"]/div[contains(@class,"summary") and contains(@class,"clearfix")]/section/div/cite/@class').extract_first().strip()
                boomplay_artist_info_batch_data_item['boomplay_artist_certification'] = 1 if vip_icon == "default_authentic_icon icon_personal" else 0
                # 10.boomplay_artist_image
                boomplay_artist_info_batch_data_item['boomplay_artist_image'] = response.xpath(
                    '//section[contains(@class,"default") and contains(@class,"default_artist")]/div[@class="img"]/img/@src').extract_first()
                # 11.boomplay_artist_info
                boomplay_artist_info_batch_data_item['boomplay_artist_info'] = ','.join(
                    [p.strip().lower() for p in response.xpath('//span[@class="description_content"]/text()').extract()])
                # 12.country_region
                boomplay_artist_info_batch_data_item['country_region'] = \
                response.xpath('//cite[@class="boomIdDisplay"]/text()').extract_first().strip().split(':')[
                    1].lower().strip()


                # 13.artist_favorite_count
                is_exists_favorite_banner = response.xpath(
                    './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]')
                if is_exists_favorite_banner:
                    boomplay_artist_info_batch_data_item["artist_favorite_count"] = response.xpath(
                        './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]/@data-count').extract_first()
                else:
                    boomplay_artist_info_batch_data_item["artist_favorite_count"] = ''
                # 14.artist_share_count
                is_exists_share_banner = response.xpath(
                    './/button[contains(@class,"btn_share") and contains(@class,"share_event")]')
                if is_exists_share_banner:
                    boomplay_artist_info_batch_data_item["artist_share_count"] = response.xpath(
                        './/button[contains(@class,"btn_share") and contains(@class,"share_event")]/@data-count').extract_first()
                else:
                    boomplay_artist_info_batch_data_item["artist_share_count"] = ''

                # 15.artist_comment_count
                is_exists_comment_banner = response.xpath(
                    './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]')
                if is_exists_comment_banner:
                    boomplay_artist_info_batch_data_item["artist_comment_count"] = response.xpath(
                        './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]/@data-count').extract_first()
                else:
                    boomplay_artist_info_batch_data_item["artist_comment_count"] = ''

                # 16.ranking_current
                is_exists_current_banner = response.xpath('.//div[@class="rankingCurrent"]')
                if is_exists_current_banner:
                    ranking_current = response.xpath('.//div[@class="rankingCurrent"]/text()').extract_first().split("#")[
                        1].strip().replace(',', '')
                    if '+' not in ranking_current:
                        boomplay_artist_info_batch_data_item["ranking_current"] = int(
                            float(ranking_current.replace('k', '')) * 1000) if 'k' in ranking_current else int((float(
                            ranking_current.replace('m', '')) * 1000000) if 'm' in ranking_current else ranking_current)
                    else:
                        boomplay_artist_info_batch_data_item["ranking_current"] = ranking_current
                else:
                    boomplay_artist_info_batch_data_item['ranking_current'] = ''

                # 17.ranking_alltime
                is_exists_alltime_banner = response.xpath('.//div[@class="rankingAllTime"]')
                if is_exists_alltime_banner:
                    ranking_alltime = response.xpath('.//div[@class="rankingAllTime"]/text()').extract_first().split("#")[
                        1].strip().replace(',', '')
                    if '+' not in ranking_alltime:
                        boomplay_artist_info_batch_data_item["ranking_alltime"] = int(
                            float(ranking_alltime.replace('k', '')) * 1000) if 'k' in ranking_alltime else int((float(
                            ranking_alltime.replace('m', '')) * 1000000) if 'm' in ranking_alltime else ranking_alltime)
                    else:
                        boomplay_artist_info_batch_data_item["ranking_alltime"] = ranking_alltime
                else:
                    boomplay_artist_info_batch_data_item["ranking_alltime"] = ''

                # 18.batch
                boomplay_artist_info_batch_data_item['batch'] = self.batch_date
                # ========================================================================
                # 二、歌手信息采集情况表
                boompplay_artist_info_crawl_situation_record_batch_data_item = BoomplayArtistInfoCrawlSituationRecordBatchDataItem()
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    "gmg_artist_id"] = request.task_gmg_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item['boomplay_artist_infomation_remarks'] = "EI"
                boompplay_artist_info_crawl_situation_record_batch_data_item['boomplay_artist_exception_info'] = ''
                boompplay_artist_info_crawl_situation_record_batch_data_item['boomplay_artist_exception_info'] = response.xpath('//div[contains(@class,"scrollView_content") and contains(@class,"pageContent")]/div[@class="noData"]/div[@class="text"]/text()').extract_first()
                boompplay_artist_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
                yield boomplay_artist_info_batch_data_item
                yield boompplay_artist_info_crawl_situation_record_batch_data_item
                yield self.update_task_state(request.task_id, 1)

                # 本次采集到相关信息，需要将对应采集歌曲、专辑、播放列表的相关任务字段重置，避免其值为-1，不参与采集而丢失数据
                update_sql1 = """
                UPDATE {task_table} SET {task_state}=-2,{task_state1}=0
                WHERE boomplay_artist_id = {task_artist_id}
                """.format(
                    task_table="gmg_boomplay_artist_info_batch_task",
                    task_state="bj_crawl_artist_album_track_playlist_task_state",
                    task_state1="bj_crawl_songs_albums_playlists_count_state",
                    task_artist_id=request.task_boomplay_artist_id
                )
                return self._mysqldb.update(update_sql1)


            elif is_exist_info=='page404':
                # 二、歌手信息采集情况表
                boompplay_artist_info_crawl_situation_record_batch_data_item = BoomplayArtistInfoCrawlSituationRecordBatchDataItem()
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    "gmg_artist_id"] = request.task_gmg_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item['boomplay_artist_id'] = request.task_boomplay_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item['boomplay_artist_infomation_remarks'] = "NI"
                boompplay_artist_info_crawl_situation_record_batch_data_item['boomplay_artist_exception_info'] = "page404: " +response.xpath('//div[contains(@class,"scrollView_content") and contains(@class,"pageContent")]/div[@class="noData"]/div[@class="text"]/text()').extract_first()
                boompplay_artist_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
                yield boompplay_artist_info_crawl_situation_record_batch_data_item
                yield self.update_task_state(request.task_id, 1)

                # 无法正常采集歌手信息，其对应的歌曲、专辑及其相关映射，任务也不再参与执行
                update_sql1 = """
                UPDATE {task_table} SET {task_state}=-3,{task_state1}=-3 WHERE boomplay_artist_id={task_artist_id}
                """.format(task_table=self._task_table,task_state="bj_crawl_songs_albums_playlists_count_state",
                           task_state1="bj_crawl_artist_album_track_playlist_task_state",task_artist_id=request.task_boomplay_artist_id
                           )
                return self._mysqldb.update(update_sql1)

            elif is_exist_info=="songsDetails":
                boompplay_artist_info_crawl_situation_record_batch_data_item = BoomplayArtistInfoCrawlSituationRecordBatchDataItem()
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    "gmg_artist_id"] = request.task_gmg_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_id'] = request.task_boomplay_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_infomation_remarks'] = "NI"
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_exception_info'] = "This is songs id"
                boompplay_artist_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
                yield boompplay_artist_info_crawl_situation_record_batch_data_item
                yield self.update_task_state(request.task_id, 1)

                # 无法正常采集歌手信息，其对应的歌曲、专辑及其相关映射，任务也不再参与执行
                update_sql1 = """
                                UPDATE {task_table} SET {task_state}=-3,{task_state1}=-3 WHERE boomplay_artist_id={task_artist_id}
                                """.format(task_table=self._task_table,
                                           task_state="bj_crawl_songs_albums_playlists_count_state",
                                           task_state1="bj_crawl_artist_album_track_playlist_task_state",
                                           task_artist_id=request.task_boomplay_artist_id
                                           )
                return self._mysqldb.update(update_sql1)

            elif is_exist_info=="playlistsDetails":
                boompplay_artist_info_crawl_situation_record_batch_data_item = BoomplayArtistInfoCrawlSituationRecordBatchDataItem()
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    "gmg_artist_id"] = request.task_gmg_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_id'] = request.task_boomplay_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_infomation_remarks'] = "NI"
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_exception_info'] = "This is playlists id"
                boompplay_artist_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
                yield boompplay_artist_info_crawl_situation_record_batch_data_item
                yield self.update_task_state(request.task_id, 1)

                # 无法正常采集歌手信息，其对应的歌曲、专辑及其相关映射，任务也不再参与执行
                update_sql1 = """
                                UPDATE {task_table} SET {task_state}=-3,{task_state1}=-3 WHERE boomplay_artist_id={task_artist_id}
                                """.format(task_table=self._task_table,
                                           task_state="bj_crawl_songs_albums_playlists_count_state",
                                           task_state1="bj_crawl_artist_album_track_playlist_task_state",
                                           task_artist_id=request.task_boomplay_artist_id
                                           )
                return self._mysqldb.update(update_sql1)

            elif is_exist_info=="albumsDetails":
                boompplay_artist_info_crawl_situation_record_batch_data_item = BoomplayArtistInfoCrawlSituationRecordBatchDataItem()
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    "gmg_artist_id"] = request.task_gmg_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_id'] = request.task_boomplay_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_infomation_remarks'] = "NI"
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_exception_info'] = "This is albums id"
                boompplay_artist_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
                yield boompplay_artist_info_crawl_situation_record_batch_data_item
                yield self.update_task_state(request.task_id, 1)

                # 无法正常采集歌手信息，其对应的歌曲、专辑及其相关映射，任务也不再参与执行
                update_sql1 = """
                                UPDATE {task_table} SET {task_state}=-3,{task_state1}=-3 WHERE boomplay_artist_id={task_artist_id}
                                """.format(task_table=self._task_table,
                                           task_state="bj_crawl_songs_albums_playlists_count_state",
                                           task_state1="bj_crawl_artist_album_track_playlist_task_state",
                                           task_artist_id=request.task_boomplay_artist_id
                                           )
                return self._mysqldb.update(update_sql1)

            elif is_exist_info=="JsonPage":
                boompplay_artist_info_crawl_situation_record_batch_data_item = BoomplayArtistInfoCrawlSituationRecordBatchDataItem()
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    "gmg_artist_id"] = request.task_gmg_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_id'] = request.task_boomplay_artist_id
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_infomation_remarks'] = "NI"
                boompplay_artist_info_crawl_situation_record_batch_data_item[
                    'boomplay_artist_exception_info'] = "JsonPage: " + response.xpath(
                    '//div[contains(@class,"scrollView_content") and contains(@class,"pageContent")]/div[@class="noData"]/div[@class="text"]/text()').extract_first()
                boompplay_artist_info_crawl_situation_record_batch_data_item['batch'] = self.batch_date
                yield boompplay_artist_info_crawl_situation_record_batch_data_item
                yield self.update_task_state(request.task_id, 1)

                # 无法正常采集歌手信息，其对应的歌曲、专辑及其相关映射，任务也不再参与执行
                update_sql1 = """
                                UPDATE {task_table} SET {task_state}=-3,{task_state1}=-3 WHERE boomplay_artist_id={task_artist_id}
                                """.format(task_table=self._task_table,
                                           task_state="bj_crawl_songs_albums_playlists_count_state",
                                           task_state1="bj_crawl_artist_album_track_playlist_task_state",
                                           task_artist_id=request.task_boomplay_artist_id
                                           )
                return self._mysqldb.update(update_sql1)


    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_state(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawlBoomplayArtistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlBoomplayArtistInfoSpider爬虫")

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
    # python crawl_boomplay_artist_info_spider.py --start_master  # 添加任务
    # python crawl_boomplay_artist_info_spider.py --start_worker  # 启动爬虫
