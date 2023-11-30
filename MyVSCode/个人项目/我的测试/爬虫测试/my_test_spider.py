# -*- coding: utf-8 -*-
"""
Created on 2023-04-11 16:16:47
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
import time
from feapder.utils.webdriver import WebDriver
import re
import time



class MyTestSpider(feapder.AirSpider):
    # def download_midware(self, request):
    #     request.headers = {
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    #     }
    #     return request

    # def init_task(self):
    #     pass

    # def add_task(self):
    #     update_state_sql = "UPDATE boomplay_track_info_batch_task SET {} = 0 WHERE {} = -1".format(self._task_state,self._task_state)
    #     self._mysqldb.update(update_state_sql)

    # def my_init_task(self):
    #     sql = "update {task_table} set {state} = 0 where {state} != -1".format(
    #         task_table=self._task_table,
    #         state=self._task_state,
    #     )
    #     return self._mysqldb.update(sql)

    def download_midware(self, request):
        request.headers = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
        # task_id = task.id
        task_track_id = '27289588'
        # if self._task_state:
        #     task_crawl_frequency = 'crawl_weekly'
        url = "https://www.boomplay.com/embed/{}/MUSIC?colType=5&colID=".format(
            task_track_id)
        yield feapder.Request(url=url,
                            #   task_id=task_id,
                            #   task_crawl_frequency=task_crawl_frequency,
                              task_track_id=task_track_id)

    def parse(self, request, response):
        track_views_batch_data_item = dict()
        # try:
        view = response.xpath(
            './/span[@class="listen"]/text()').extract_first().replace(
                ",", "")
        # 22-播放量
        if 'k' in view:
            track_views_batch_data_item["views"] = int(
                float(view[:-1]) * 1000)
        elif 'm' in view:
            track_views_batch_data_item["views"] = int(
                float(view[:-1]) * 1000000)
        else:
            track_views_batch_data_item["views"] = view
        track_views_batch_data_item['track_id'] = request.task_track_id
        track_views_batch_data_item['batch'] = self.batch_date
        track_views_batch_data_item[
            'crawl_frequency'] = request.task_crawl_frequency
        print(track_views_batch_data_item)
            # yield track_views_batch_data_item
            # yield self.update_task_batch(request.task_id, 1)
        # except:
            # yield self.update_task_batch(request.task_id, -1)
            # failed_info = response.xpath('//div[@class="noData"]/div[@class="text"]/text()').extract_first()
            # boomplay_track_status_failed_batch_data_item = dict()
            # boomplay_track_status_failed_batch_data_item['track_id'] = request.task_track_id
            # boomplay_track_status_failed_batch_data_item['failed_info'] = failed_info
            # # yield boomplay_track_status_failed_batch_data_item
            # print(boomplay_track_status_failed_batch_data_item)
            # print("失败")

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        failed_info = response.xpath('//div[@class="noData"]/div[@class="text"]/text()').extract_first()
        boomplay_track_status_failed_batch_data_item = dict()
        boomplay_track_status_failed_batch_data_item['track_id'] = request.task_track_id
        boomplay_track_status_failed_batch_data_item['failed_info'] = failed_info
        # yield boomplay_track_status_failed_batch_data_item
        print(boomplay_track_status_failed_batch_data_item)
        # yield request
        # yield self.update_task_state(request.task_id, -1)

if __name__ == "__main__":
    MyTestSpider().start()


