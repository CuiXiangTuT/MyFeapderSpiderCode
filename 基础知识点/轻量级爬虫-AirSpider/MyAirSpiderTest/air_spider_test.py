# -*- coding: utf-8 -*-
"""
Created on 2023-01-17 15:22:15
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
import datetime
from my_airspider_test_item import MyAirspiderTestItem


class AirSpiderTest(feapder.AirSpider): # feapder.AirSpider轻量级爬虫基类
    # 下载中间件
    def download_midware(self, request):
        """
        下载中间件用于在请求之前，对请求做一些处理，如添加cookie、header等
        """
        request.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        print("------自定义下载中间件，这里配置了headers参数------")
        return request
    
    # 自定义下载中间件 
    def my_download_midware(self,request):
        """
        与自定义解析函数类似，下载中间件也可以支持自定义，只需要在feapder.Request参数里指定download_midware回调即可
        """
        print("------这里是自定义下载中间件------")
        pass


    def start_requests(self): # 初始下发任务入口
        head_title = "Hello World"
        yield feapder.Request("https://top.baidu.com/board?tab=realtime")
        # 携带参数
        yield feapder.Request("https://www.baidu.com",top_title=head_title,callback=self.parse1,download_midware=self.my_download_midware) # 下发新任务
        # 浏览器渲染下载
        yield feapder.Request("https://www.youtube.com/",render=True)
    
    # 校验
    def validate(self, request, response):
        """
        @summary: 校验函数, 可用于校验response是否正确
        若函数内抛出异常，则重试请求
        若返回True 或 None，则进入解析函数
        若返回False，则抛弃当前请求
        可通过request.callback_name 区分不同的回调函数，编写不同的校验逻辑
        ---------
        @param request:
        @param response:
        ---------
        @result: True / None / False
        """
        if response.status_code != 200:
            raise Exception("Response code not 200") # 重试
        
        if "哈哈" not in response.text:
            return False # 抛弃当前请求

    def parse(self, request, response):
        # # 提取网站title
        # print(response.xpath("//title/text()").extract_first())
        # # 提取网站描述
        # print(response.xpath("//meta[@name='description']/@content").extract_first())
        # print("网站地址: ", response.url)
        div_list = response.xpath('..//div[contains(@class,"category-wrap_iQLoo") and contains(@class,"horizontal_1eKyQ")]')
        for per_div in div_list:
            item = MyAirspiderTestItem()
            # 标题
            item["title"] = per_div.xpath('.//div[@class="c-single-text-ellipsis"]/text()').extract_first().strip()
            # 热度值
            item["hot_search_index"] = per_div.xpath('.//div[@class="hot-index_1Bl1a"]/text()').extract_first().strip()
            # 插入时间
            item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # yield item
            print(item)
    
    def parse1(self,request,response):
        top_title = request.top_title
        print("传递过来的参数为："+top_title)

        # 失败重试
        if response.status_code != 200:
            raise Exception("非法页面") # 重试次数默认最大为100，可在配置文件中进行修改



if __name__ == "__main__":
    AirSpiderTest().start()