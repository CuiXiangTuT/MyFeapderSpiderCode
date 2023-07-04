#-*- coding: UTF-8-*-
"""
Created on 2023-05-22 16:49:23
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.search_youtube_info_data_item import SearchYoutubeInfoDataItem
import re
import json


class GetYoutubeInfoViews(feapder.BatchSpider):
    def add_task(self):
        update_state_sql = """
        UPDATE search_youtube_info_task
        SET state = 0
        WHERE state != 1
        """
        self._mysqldb.update(update_state_sql)

    def download_midware(self, request):
        request.headers = {
            'accept-language': 'zh-CN,zh;q=0.9',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_artist_id = task.artist_id
        task_artist_name = task.artist_name
        task_track_id = task.track_id
        task_track_name = task.track_name
        yield feapder.Request("https://www.youtube.com/results?search_query={}".format(task_track_name+""+task_artist_name),
            task_id = task_id,
            task_artist_id = task_artist_id,
            task_artist_name = task_artist_name,
            task_track_id = task_track_id,
            task_track_name = task_track_name
        )

    def parse(self, request, response):
        pattern = re.compile('var ytInitialData = (.*?);</script>',re.S)
        content = re.findall(pattern,response.text)[0]
        youtube_info = SearchYoutubeInfoDataItem()
        try:
            try:
                contents_data = json.loads(content)['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]
                youtube_info['artist_id'] = request.task_artist_id
                youtube_info['artist_name'] = request.task_artist_name
                youtube_info['track_id'] = request.task_track_id
                youtube_info['track_name'] = request.task_track_name
                youtube_info['youtube_video_id'] = contents_data['videoRenderer']['videoId']
                youtube_info['youtube_title'] = contents_data['videoRenderer']['title']['runs'][0]['text'].lower().strip()
                # try:
                youtube_info['views'] = contents_data['videoRenderer']['viewCountText']['simpleText'].replace('次观看','').replace(',','').strip()
                # except:
                #     youtube_info['views'] = contents_data['videoRenderer']['viewCountText']['simpleText'].encode('utf-8').decode('latin1').replace('views','').strip().replace(',','')
                youtube_info['youtube_link'] = 'https://www.youtube.com/watch?v='+youtube_info['youtube_video_id']
                youtube_info['youtube_channel'] = contents_data['videoRenderer']['longBylineText']['runs'][0]['text'].lower().strip()
                youtube_info['batch'] = self.batch_date
                yield youtube_info
                yield self.update_task_batch(request.task_id, 1) 
            except:
                contents_data = json.loads(content)['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][1]
                youtube_info['artist_id'] = request.task_artist_id
                youtube_info['artist_name'] = request.task_artist_name
                youtube_info['track_id'] = request.task_track_id
                youtube_info['track_name'] = request.task_track_name
                youtube_info['youtube_video_id'] = contents_data['videoRenderer']['videoId']
                youtube_info['youtube_title'] = contents_data['videoRenderer']['title']['runs'][0]['text'].lower().strip()
                # try:
                youtube_info['views'] = contents_data['videoRenderer']['viewCountText']['simpleText'].replace('次观看','').replace(',','').strip()
                # except:
                #     youtube_info['views'] = contents_data['videoRenderer']['viewCountText']['simpleText'].encode('utf-8').decode('latin1').replace('views','').strip().replace(',','')
                youtube_info['youtube_link'] = 'https://www.youtube.com/watch?v='+youtube_info['youtube_video_id']
                youtube_info['youtube_channel'] = contents_data['videoRenderer']['longBylineText']['runs'][0]['text'].lower().strip()
                youtube_info['batch'] = self.batch_date
                yield youtube_info
                yield self.update_task_batch(request.task_id, 1) 
        except:
            yield self.update_task_batch(request.task_id, -1) 
    
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1) 



if __name__ == "__main__":
    spider = GetYoutubeInfoViews(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="GetYoutubeInfoViews爬虫")

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
    # python get_youtube_info_views.py --start_master  # 添加任务
    # python get_youtube_info_views.py --start_worker  # 启动爬虫
