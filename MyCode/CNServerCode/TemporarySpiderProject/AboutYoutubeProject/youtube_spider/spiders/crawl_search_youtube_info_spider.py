# -*- coding: utf-8 -*-
"""
Created on 2023-12-01 14:49:35
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *
import json
import re
from datetime import datetime
import warnings
import httpx


class CrawlSearchYoutubeInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def start_requests(self, task):
        task_id = task.id
        task_artist_id = task.artist_id
        task_track_id = task.track_id
        task_artist_name = task.artist_name
        task_track_name = task.track_name
        query_words = task_artist_name+" "+task_track_name
        result = CrawlSearchYoutubeInfoSpider.search(query_words)
        yield feapder.Request(url=result["url"],videoId=result["id"],task_id=task_id,
            task_artist_id=task_artist_id,
            task_track_id=task_track_id,
            task_artist_name=task_artist_name,
            task_track_name=task_track_name
        )

    def parse(self, request, response):
        data = re.findall(r'var ytInitialPlayerResponse = (.*?)var meta = document.*</script>',response.text,re.S)[0][:-1]
        json_data = json.loads(data)['videoDetails']
        temporary_search_youtube_info_batch_data_item = TemporarySearchYoutubeInfoBatchDataItem()
        # task_artist_id
        temporary_search_youtube_info_batch_data_item['artist_id'] = request.task_artist_id
        # task_track_id
        temporary_search_youtube_info_batch_data_item['track_id'] = request.task_track_id
        # task_artist_name
        temporary_search_youtube_info_batch_data_item['artist_name'] = request.task_artist_name
        # task_track_name
        temporary_search_youtube_info_batch_data_item['track_name'] = request.task_track_name
        #  标题
        temporary_search_youtube_info_batch_data_item["youtube_title"] = json_data["title"]
        # video_id
        temporary_search_youtube_info_batch_data_item["youtube_video_id"] = json_data["videoId"]
        # url
        temporary_search_youtube_info_batch_data_item['youtube_link'] = "https://www.youtube.com/watch?v="+json_data["videoId"]
        # 时长？
        temporary_search_youtube_info_batch_data_item["duration"] = json_data["lengthSeconds"]
        # channelId
        temporary_search_youtube_info_batch_data_item["youtube_channel_id"] = json_data["channelId"]
        # 作者
        temporary_search_youtube_info_batch_data_item['youtube_channel_name'] = json_data['author']
        # 播放量
        temporary_search_youtube_info_batch_data_item["views"] = json_data['viewCount']
        # 发行日期
        publish_date = json.loads(data)["microformat"]["playerMicroformatRenderer"]["publishDate"]
        datetime_obj = datetime.fromisoformat(publish_date)
        temporary_search_youtube_info_batch_data_item["publish_date"] = datetime_obj.date().strftime('%Y-%m-%d')
        # 简述
        temporary_search_youtube_info_batch_data_item["description"] = json_data['shortDescription'].replace("\n"," ")
        temporary_search_youtube_info_batch_data_item['batch'] = self.batch_date
        yield temporary_search_youtube_info_batch_data_item
        yield self.update_task_state(request.task_id, 1)
    
    @staticmethod
    def search(query: str) -> dict[str | None]:
        headers: dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

        page: str = httpx.get(f"https://music.youtube.com/search?q={query}", headers=headers,
                            timeout=None).content.decode("unicode_escape")

        trackId: str | None = re.search('"videoId":"(.*?)"', page)

        if not trackId:
            return {}

        trackId: str = eval(f"{{{trackId.group()}}}")["videoId"]

        track_info: dict = httpx.get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={trackId}",
                                    headers=headers, timeout=None).json()

        return dict(
            title=track_info["title"],
            id=trackId,
            url=f"https://www.youtube.com/watch?v={trackId}",
            # artwork=f"https://img.youtube.com/vi/{trackId}/0.jpg",
            # author=dict(name=track_info["author_name"], url=track_info["author_url"])
        )


if __name__ == "__main__":
    spider = CrawlSearchYoutubeInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlSearchYoutubeInfoSpider爬虫")

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
    # python crawl_search_youtube_info_spider.py --start_master  # 添加任务
    # python crawl_search_youtube_info_spider.py --start_worker  # 启动爬虫
