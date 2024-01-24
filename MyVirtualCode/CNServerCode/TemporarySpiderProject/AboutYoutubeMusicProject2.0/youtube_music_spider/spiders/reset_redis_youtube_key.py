# -*- coding: utf-8 -*-
"""
Created on 2024-01-03 15:29:32
---------
@summary:
---------
@author: QiuQiuRen
@description：
    用来重置每日youtube的配额
"""
import redis


class ResetRedisYoutubeKeyValue:
    def __init__(self):
        self.redis_host = "127.0.0.1"
        self.redis_password = ""
        self.redis_db = 0
        self.redis_conn = redis.Redis(host=self.redis_host, password=self.redis_password, db=self.redis_db)

    def reset_key_value(self):
        l = [
            {"AIzaSyAh55pBcbDVv0tUngbat3J1IhoVekXyIrY": 0},
        ]
        for i in l:
            self.redis_conn.zadd("youtube_quota", i)

if __name__ == '__main__':
    ResetRedisYoutubeKeyValue().reset_key_value()

