# -*- coding: utf-8 -*-
"""
Created on 2023-01-18 14:11:23
---------
@summary:
---------
@author: QiuQiuRen
"""

from feapder import Item


class MySpiderTaskBaiduNewsTestItem(Item):
    """
    This class was generated by feapder
    command: feapder create -i my_spider_task_baidu_news_test 1
    """

    __table_name__ = "my_spider_task_baidu_news_test"

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.title = kwargs.get('title')  # 标题
        self.hot_search_index = kwargs.get('hot_search_index')  # 热搜指数
        self.insert_time = kwargs.get('insert_time')  # 插入时间
