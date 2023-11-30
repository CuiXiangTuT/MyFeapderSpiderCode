# -*- coding: utf-8 -*-
"""
Created on 2023-05-09 15:51:00
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *
import re
import json
import copy


class BoomplayArtistInfoSpider(feapder.BatchSpider):
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

    # def add_task(self):
    #     """
    #     从gmg_artist_aka中取出site="boomplay"的歌手
    #     1.更新booomplay_artist_info_batch_task中，boomplay_id在gmg_artist_aka中存在的，将gmg_artist_id和gmg_artist_name进行更新，
    #     并将booomplay_artist_info_batch_task中的boomplay_artist_name更新为与gmg_artist_name一致
    #     2.将gmg_artist_aka中其余与boomplay_artist_info_batch_task中不一致的进行添加
    #     """
    #     update_sql = """
    #     UPDATE `boomplay_artist_info_batch_task` b
    #     INNER JOIN `GMG_DATA_ASSETS`.`gmg_artist_aka` g
    #     ON b.boomplay_artist_id = g.id AND g.site='boomplay'
    #     SET b.gmg_artist_id=g.gmg_artist_id,b.gmg_artist_name=g.gmg_artist_name,b.boomplay_artist_name=g.gmg_artist_name,b.usable=1
    #     """
    #     self._mysqldb.update(update_sql)

    #     insert_sql = """
    #     INSERT IGNORE INTO `boomplay_artist_info_batch_task`
    #     (gmg_artist_id,gmg_artist_name,boomplay_artist_id,boomplay_artist_name,usable) 
    #     SELECT `gmg_artist_id`,`gmg_artist_name`,`id`,`gmg_artist_name`,1
    #     FROM `gmg_data_assets`.`gmg_artist_aka`
    #     WHERE site='boomplay' AND `id` NOT IN (
    #         SELECT boomplay_artist_id FROM `boomplay_artist_info_batch_task`
    #     )
    #     """
    #     self._mysqldb.add(insert_sql)

    #     update_state_sql = "UPDATE boomplay_artist_info_batch_task SET {} = 0 WHERE {} = -1".format(self._task_state,self._task_state)
    #     self._mysqldb.update(update_state_sql)
    

    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        # "gmg_artist_name", "boomplay_artist_id","boomplay_artist_name"
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_gmg_artist_name = task.gmg_artist_name
        task_boomplay_artist_id = task.boomplay_artist_id
        task_boomplay_artist_name = task.boomplay_artist_name
        yield feapder.Request(url='https://www.boomplay.com/artists/' + task_boomplay_artist_id,
                              task_boomplay_artist_name=task_boomplay_artist_name,task_id=task_id,task_gmg_artist_id=task_gmg_artist_id,
                              task_gmg_artist_name=task_gmg_artist_name,task_boomplay_artist_id=task_boomplay_artist_id)

    def parse(self, request, response):
        if str(request.task_boomplay_artist_id) == "43630":
            yield self.update_task_batch(request.task_id, -1)
        else:
            page = response.xpath('.//div[@id="page404"]')
            if len(page):
                yield self.update_task_batch(request.task_id, -1)
            else:
                try:
                    # 一、歌手信息表相关字段信息
                    artist_info = BoomplayArtistInfoBatchDataItem()
                    # 3-crawl_artist_name
                    artist_info["crawl_artist_name"] = str(request.task_gmg_artist_name).lower() if request.task_gmg_artist_name else ''
                    # 1-gmg_artist_id
                    artist_info["gmg_artist_id"] = request.task_gmg_artist_id
                    # 2-gmg_artist_name
                    artist_info["gmg_artist_name"] = str(request.task_gmg_artist_name).lower() if request.task_gmg_artist_name else ''
                    # 匹配页面script标签里的json_data数据
                    script_json_data = response.re(r'type="application/ld\+json">(.*?)</script>')[0].replace('\t','').replace('\n','').strip()
                    json_data = json.loads(script_json_data)
                    artist_info['crawl_boomplay_artist_id'] = request.task_boomplay_artist_id
                    # 4-boomplay_artist_id
                    artist_info["boomplay_artist_id"] = json_data["@id"].split("/")[-1]
                    # 5-boomplay_artist_name
                    artist_info["boomplay_artist_name"] = json_data["name"].replace("&amp;","&").replace("&#039;","'").replace("&#034;",'"').lower()
                    # 6-boomplay_artist_certification
                    artist_info["boomplay_artist_certification"] = 1 if response.xpath(
                        './/cite[contains(@class,"default_authentic_icon") and contains(@class,"icon_personal")]') else 0
                    # 7-batch
                    artist_info["batch"] = self.batch_date
                    # 8-boomplay_artist_image
                    artist_info["boomplay_artist_image"] = json_data["image"]
                    # 9-boomplay_artist_info
                    artist_info["boomplay_artist_info"] = ''.join(
                        response.xpath('.//span[@class="description_content"]/text()').extract()).strip().lower()
                    # 10-artist_favorite_count
                    artist_info["artist_favorite_count"] = response.xpath(
                        './/button[contains(@class,"btn_favorite") and contains(@class,"favorite_event")]/@data-count').extract_first()
                    # 11-artist_share_count
                    artist_info["artist_share_count"] = response.xpath(
                        './/button[contains(@class,"btn_share") and contains(@class,"share_event")]/@data-count').extract_first()
                    # 12-artist_comment_count
                    artist_info["artist_comment_count"] = response.xpath(
                        './/button[contains(@class,"btn_comment") and contains(@class,"comment_event")]/@data-count').extract_first()
                    # 13-ranking_current
                    ranking_current = response.xpath('.//div[@class="rankingCurrent"]/text()').extract_first().split("#")[
                    1].strip().replace(',','')
                    if '+' not in ranking_current:
                        artist_info["ranking_current"] = int(float(ranking_current.replace('k',''))*1000) if 'k' in ranking_current else int((float(ranking_current.replace('m',''))*1000000) if 'm' in ranking_current else ranking_current)
                    else:
                        artist_info["ranking_current"] = ranking_current
                    # 14-ranking_alltime
                    ranking_alltime = response.xpath('.//div[@class="rankingAllTime"]/text()').extract_first().split("#")[
                    1].strip().replace(',','')
                    if '+' not in ranking_alltime:
                        artist_info["ranking_alltime"] = int(float(ranking_alltime.replace('k',''))*1000) if 'k' in ranking_alltime else int((float(ranking_alltime.replace('m',''))*1000000) if 'm' in ranking_alltime else ranking_alltime)
                    else:
                        artist_info["ranking_alltime"] = ranking_alltime
                    if len(response.xpath('.//cite[@class="boomIdDisplay"]/text()').extract_first().strip()):
                        artist_info['country_region'] = response.xpath('.//cite[@class="boomIdDisplay"]/text()').extract_first().strip().split(':')[1].lower()
                    else:
                        artist_info['country_region'] = ''
                    yield artist_info
                    yield self.update_task_batch(request.task_id, 1)
                except:
                    yield self.update_task_batch(request.task_id, -1)
    
    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response,e):
        yield request
        yield self.update_task_state(request.task_id, -1)



if __name__ == "__main__":
    spider = BoomplayArtistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BoomplayArtistInfoSpider爬虫")

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
    # python boomplay_artist_info_spider.py --start_master  # 添加任务
    # python boomplay_artist_info_spider.py --start_worker  # 启动爬虫
