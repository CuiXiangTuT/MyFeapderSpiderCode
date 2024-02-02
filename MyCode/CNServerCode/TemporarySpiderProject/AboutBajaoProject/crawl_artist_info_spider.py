# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 17:53:51
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
import pymysql


class CrawlArtistInfoSpider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
        url = "https://bajao.pk/api/artist/details?siteid="
        # artist_id = [108313,108320,108324,11156,11777,11869,11895,11918,11998,12151,12183,12184,12221,12451,12820,13027,132442,133,13451,13467,13754,13781,138,141,14412,14474,14611,14637,15307,1562,15923,16111,17227,173,17967,18386,18430,18490,193888,216344,2173,22401,24431,24459,2566,2567,2568,2573,2583,2592,2594,2610,2653,284524,30906,35652,36170,36513,3652,3873,4309,4322,441989,443025,443032,444117,448121,448198,45305,45417,46922,48735,498892,501370,507131,507243,508846,51,517929,517974,517975,517976,518265,518451,53544,55,5520,55805,5631,58809,59422,59441,59783,59784,59785,59786,60471,6406,6446,6451,6455,6485,6493,6503,6528,6529,6866,6890,6959,6984,7069,7089,7459,7476,7491,7505,78399,80895,8185,82090,83102,83103,83104,85,87731,96,98843]
        # for aid in artist_id:
        data = {
            'aId':15923,
            'sIndex':0,
            'fIndex':7
        }
        yield feapder.Request(url=url,data=data)

    def parse(self, request, response):
        data = response.json

        if data['msg']=='SUCCESS':
            title = data['respData']['title']
            print(title)
        else :
            print(data)

if __name__ == "__main__":
    # 北京：MySQL
    MYSQL_IP_BJ = "122.115.36.92"
    MYSQL_PORT = 3306
    MYSQL_DB = "GMG_DATA_ASSETS"
    MYSQL_USER_NAME = "crawler"
    MYSQL_USER_PASS = "crawler.mysql"
    # conn = pymysql.Connect(host=MYSQL_IP_BJ,port=MYSQL_PORT,user=MYSQL_USER_NAME,password=MYSQL_USER_PASS,db=MYSQL_DB)
    # cursor = conn.cursor()
    CrawlArtistInfoSpider().start()