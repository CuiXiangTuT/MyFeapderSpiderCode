import feapder
# from feapder import ArgumentParser
import time
from feapder.utils.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pprint import pprint
from copy import deepcopy
from datetime import datetime, timedelta
import re


class MyTestAirspider4(feapder.AirSpider):
    def start_requests(self):
        data = {
            "videoId": "_XC6PKxt7YM",
            "context": {
                "client": {
                    "hl": "en",
                    "gl": "US",
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20210101.00.00"
                }
            }
        }
        url = "https://music.youtube.com/youtubei/v1/player?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        yield feapder.Request(url=url, method="POST", json=data)

    def parse(self, request, response):
        print(response.json["responseContext"]["visitorData"])


if __name__ == "__main__":
    MyTestAirspider4().start()
