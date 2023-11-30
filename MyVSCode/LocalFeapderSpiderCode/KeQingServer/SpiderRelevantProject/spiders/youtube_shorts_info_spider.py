# -*- coding: utf-8 -*-
"""
Created on 2023-08-21 15:49:36
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *
import re
from feapder.utils import tools
from feapder.utils.log import log


class YoutubeShortsInfoSpider(feapder.BatchSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    # __custom_setting__ = dict(
    #     REDISDB_IP_PORTS="localhost:6379",
    #     REDISDB_USER_PASS="",
    #     REDISDB_DB=0,
    #     MYSQL_IP="localhost",
    #     MYSQL_PORT=3306,
    #     MYSQL_DB="",
    #     MYSQL_USER_NAME="",
    #     MYSQL_USER_PASS="",
    # )
    def init_task(self):
        pass

    def add_task(self):
        # update_state_sql = "UPDATE youtube_shorts_video_views_batch_task SET {} = 0 WHERE {} = -1".format(self._task_state,self._task_state)
        update_state_sql = "UPDATE youtube_shorts_video_views_batch_task SET {} = 0".format(self._task_state)
        self._mysqldb.update(update_state_sql)


    def download_midware(self,request):
        request.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_youtube_artist_channel_id = task.youtube_artist_channel_id
        task_youtube_artist_name = task.youtube_artist_name
        task_youtube_artist_shorts_id = task.youtube_artist_shorts_id
        if task_youtube_artist_shorts_id == '-':
            yield self.update_task_state(task_id, -1)
        else:
            yield feapder.Request("https://www.youtube.com/{}/shorts".format(task_youtube_artist_shorts_id),
            task_youtube_artist_channel_id=task_youtube_artist_channel_id,
            task_id=task_id,
            task_youtube_artist_name=task_youtube_artist_name,
            task_youtube_artist_shorts_id=task_youtube_artist_shorts_id
            )

    def parse(self, request, response):
        # views_count_list = re.findall(r'"viewCountText":\{(.*?)\}',response.text)
        m_l = re.findall(r'\"videoId\":\"(.*?)\",',response.text)
        shorts_id_list = list()
        for i in m_l:
            if i in shorts_id_list:
                pass
            else:
                shorts_id_list.append(i)
        
        views_count_list = re.findall(r'"viewCountText":\{(.*?)\}',response.text)
        p = list(zip(views_count_list,shorts_id_list))

        for i in p:
            youtube_shorts_video_views_batch_data_item = YoutubeShortsVideoViewsBatchDataItem()
            s_views = i[0].split(":")[-1]
            print(s_views)
            if 'billion' in s_views:
                views = int(float(s_views.split('billion')[0][1:].strip()) * 1000000000)
            elif 'million' in s_views:
                views = int(float(s_views.split('million')[0][1:].strip()) * 1000000)
            elif 'K' in s_views:
                views = int(float(s_views.split('K')[0][1:].strip()) * 1000)
            else:
                views = s_views
            youtube_shorts_video_views_batch_data_item['youtube_shorts_video_views'] = views
            youtube_shorts_video_views_batch_data_item['youtube_artist_channel_id'] = request.task_youtube_artist_channel_id
            youtube_shorts_video_views_batch_data_item['youtube_artist_name'] = request.task_youtube_artist_name
            youtube_shorts_video_views_batch_data_item['youtube_shorts_video_id'] = request.task_youtube_artist_shorts_id
            youtube_shorts_video_views_batch_data_item['batch'] = self.batch_date
            youtube_shorts_video_views_batch_data_item['youtube_shorts_id'] = i[1]
            yield youtube_shorts_video_views_batch_data_item
        
        # shorts_id_list = list(set(re.findall(r'\"videoId\":\"(.*?)\",',response.text)))
        for i in p:
            youtube_shorts_video_likes_batch_task_item = YoutubeShortsVideoLikesBatchTaskItem()
            youtube_shorts_video_likes_batch_task_item['youtube_shorts_id'] = i[1]
            youtube_shorts_video_likes_batch_task_item['youtube_artist_channel_id']=request.task_youtube_artist_channel_id
            youtube_shorts_video_likes_batch_task_item['youtube_artist_name']=request.task_youtube_artist_name
            # yield self.add_new_task('youtube_shorts_video_likes_batch_task',youtube_shorts_video_likes_batch_task_item.to_dict)
            yield youtube_shorts_video_likes_batch_task_item
        yield self.update_task_state(request.task_id, 1)
    
    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)  
    
    
    # def add_new_task(self, table,data):
    #     sql = tools.make_insert_sql(
    #         table, data,insert_ignore=True
    #     )
    #     if self._mysqldb.update(sql):
    #         log.debug("添加任务成功: %s" % sql)
    #     else:
    #         log.error("添加任务失败")

            


if __name__ == "__main__":
    spider = YoutubeShortsInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="YoutubeShortsInfoSpider爬虫")

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
    # python youtube_shorts_info_spider.py --start_master  # 添加任务
    # python youtube_shorts_info_spider.py --start_worker  # 启动爬虫
