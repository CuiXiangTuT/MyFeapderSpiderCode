# -*- coding: utf-8 -*-
"""
Created on 2023-01-17 17:25:04
---------
@summary:
---------
@author: QiuQiuRen
"""

from feapder import Item


class MySpiderWangyiNewsTestItem(Item):
    """
    This class was generated by feapder
    command: feapder create -i my_spider_wangyi_news_test 1
    """

    __table_name__ = "my_spider_wangyi_news_test"

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.title = kwargs.get('title')  # 标题
        self.channel_name = kwargs.get('channel_name')  # 新闻频道类型
        self.comment_url = kwargs.get('comment_url')  # 评论链接
        self.doc_url = kwargs.get('doc_url')  # 文章链接
        self.img_url = kwargs.get('img_url')  # 图片链接
        self.keywords_akey_link = kwargs.get('keywords_akey_link')  # 关键词链接
        self.keywords_keyname = kwargs.get('keywords_keyname')  # 关键词
        self.label = kwargs.get('label')  # 标签
        self.news_type = kwargs.get('news_type')  # 新闻类型
        self.source = kwargs.get('source')  # 新闻来源
        self.tienum = kwargs.get('tienum')  # 跟帖数
        self.publish_time = kwargs.get('publish_time')  # 发表日期
        self.insert_time = kwargs.get('insert_time')  # 插入日期
