import feapder
from feapder import ArgumentParser
from feapder.db.redisdb import RedisDB
from queue import Queue
from feapder.utils.log import log
import os
import isodate
from pprint import pprint
from datetime import datetime, timedelta
from copy import deepcopy
import re


class MyTestAirspider(feapder.AirSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        # request.proxies = {"http": "http://139.84.227.201:42000"}

        proxyMeta = "http://7hyhrj:ju340pqy@%(host)s:%(port)s" % {
            "host": '139.84.227.201',
            "port": 42000,
        }
        request.proxies = {
            "http": proxyMeta,
            # "http": proxyMeta
        }
        return request

    def start_requests(self):
        url = "https://api64.ipify.org?format=json"
        yield feapder.Request(url=url,callback=self.parse)

    def parse(self, request, response):
        print(response.text)


if __name__ == "__main__":
    MyTestAirspider().start()
