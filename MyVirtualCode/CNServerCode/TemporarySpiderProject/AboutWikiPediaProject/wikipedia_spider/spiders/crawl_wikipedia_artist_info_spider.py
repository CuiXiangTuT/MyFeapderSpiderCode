# -*- coding: utf-8 -*-
"""
Created on 2023-12-12 17:39:22
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.wikipedia_info_item import *
import re


class CrawlWikipediaArtistInfoSpider(feapder.BatchSpider):
    def download_midware(self, request):
        request.headers = {
            # "Referer":"https://en.wikipedia.org/wiki/Jaychou",
            # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        return request

    def start_requests(self, task):
        task_gmg_artist_id = task.gmg_artist_id
        task_gmg_artist_name = task.gmg_artist_name
        task_artist_id = task.artist_id
        task_artist_name = task.artist_name
        task_id = task.id
        if self._task_table=="wikipedia_artist_batch_task":
            if task_artist_name==None:
                wiki_situation_item = WikipediaArtistCrawlSituationRecordBatchDataItem()
                wiki_situation_item["gmg_artist_id"] = task_gmg_artist_id
                wiki_situation_item["gmg_artist_name"] = task_gmg_artist_name
                wiki_situation_item["artist_id"] = task_artist_id
                wiki_situation_item["artist_name"] = task_artist_name
                wiki_situation_item['artist_infomation_remarks'] = "NI"
                wiki_situation_item["batch"] = self.batch_date
                yield wiki_situation_item
                yield self.update_task_batch(task_id, 1)
            elif len(task_artist_name):
                url = "https://en.wikipedia.org/wiki/{}".format(task.artist_name.replace(" ","_").title())
            else:
                wiki_situation_item = WikipediaArtistCrawlSituationRecordBatchDataItem()
                wiki_situation_item["gmg_artist_id"] = task_gmg_artist_id
                wiki_situation_item["gmg_artist_name"] = task_gmg_artist_name
                wiki_situation_item["artist_id"] = task_artist_id
                wiki_situation_item["artist_name"] = task_artist_name
                wiki_situation_item['artist_infomation_remarks'] = "NI"
                wiki_situation_item["batch"] = self.batch_date
                yield wiki_situation_item
                yield self.update_task_batch(task_id, 1)
        if self._task_table=="wikipedia_spotify_artist_batch_task":
            url = task.spotify_wikipedia_url
        yield feapder.Request(url=url,task_id=task_id,task_gmg_artist_id=task_gmg_artist_id,
            task_gmg_artist_name=task_gmg_artist_name,task_artist_id=task_artist_id,
            task_artist_name=task_artist_name
        )

    def parse(self, request, response):
        is_exist_infobox = response.xpath('//th[contains(@scope,"row") and contains(@class,"infobox-label")]')
        if is_exist_infobox:
            th_list = response.xpath('//th[contains(@scope,"row") and contains(@class,"infobox-label")]')
            if self._task_table=="wikipedia_artist_batch_task":
                item = WikipediaArtistBatchDataItem()
            if self._task_table=="wikipedia_spotify_artist_batch_task":
                item = WikipediaSpotifyArtistBatchDataItem()
            # 歌手名
            artist_name_l = response.xpath('//th[contains(@class,"infobox-above")]/div//text()').extract()
            item["crawl_condition_artist_name"] = request.task_artist_name.replace(" ","_").title() if request.task_artist_name else None
            item["wikipedia_url"] = request.url
            if len(artist_name_l)>1:
                artist_name_l = [k for k in artist_name_l if k not in ['\n','/',""]]
                item["crawl_box_header_artist_name"] = ' '.join(artist_name_l)
            elif len(artist_name_l)==1:
                item["crawl_box_header_artist_name"] = artist_name_l[0].strip()
            else:
                item["crawl_box_header_artist_name"] = ""
            # 歌手二级名称
            is_exist_d = response.xpath('//table[contains(@class,"infobox") and contains(@class,"vcard")]//span[@class="nobold"]/text()')
            if is_exist_d:
                item["sub_artist_name"] = response.xpath('//table[contains(@class,"infobox") and contains(@class,"vcard")]//span[@class="nobold"]/text()').extract_first()
            else:
                is_exist_f = response.xpath('//table[contains(@class,"infobox") and contains(@class,"vcard")]//td[contains(@class,"infobox-subheader") and contains(@class,"nickname")]//text()')
                if is_exist_f:
                    sub_artist_name_l = response.xpath('//table[contains(@class,"infobox") and contains(@class,"vcard")]//td[contains(@class,"infobox-subheader") and contains(@class,"nickname")]//text()').extract()
                    if len(sub_artist_name_l)>1:
                        sub_artist_name_l = [k for k in sub_artist_name_l if k not in ['\n','/',""]]
                        item["sub_artist_name"] = ' '.join(sub_artist_name_l)
                    else:
                        item["sub_artist_name"] = sub_artist_name_l[0]
            try:
                # 歌手图片
                item["artist_image"] = response.xpath('//td[@class="infobox-image"]/span/a/@href').extract_first()
                
                is_exist_c = response.xpath('//div[@class="infobox-caption"]/div[@class="hlist"]/ul/li')
                if is_exist_c:
                    img_description = response.xpath('//div[@class="infobox-caption"]/div[@class="hlist"]/ul/li//text()').extract()
                    if len(img_description)>1:
                        item["artist_image_description"] = ''.join(img_description)
                    else:
                        item["artist_image_description"] = img_description[0]
                else:
                    # 图片说明
                    l = response.xpath('//div[@class="infobox-caption"]//text()').extract()
                    if len(l)>1:
                        item["artist_image_description"] = ''.join(l)
                    else:
                        item["artist_image_description"] = l[0]
            except:
                item["artist_image_description"] = None
            json_dict = dict()
            json_dict.clear()
            for i in range(len(th_list)):
                # 文字说明
                is_exist_span = th_list[i].xpath("./span")
                if is_exist_span:
                    key_word = th_list[i].xpath("./span/text()").extract_first()
                    if key_word:
                        move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
                        key_word = key_word.translate(move)
                else:
                    is_exist_a = th_list[i].xpath("./a")
                    if is_exist_a:
                        key_word = th_list[i].xpath("./a//text()").extract()
                        if len(key_word)>1:
                            move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
                            key_word = ' '.join(key_word)
                            key_word = key_word.translate(move)
                        else:
                            move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
                            key_word = key_word[0].translate(move)
                    else:
                        key_word = th_list[i].xpath("./text()").extract_first()
                        if key_word:
                            move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
                            key_word = key_word.translate(move)
                    


                is_exist = th_list[i].xpath('./following-sibling::td/div[@class="hlist"]')
                if is_exist:
                    l = th_list[i].xpath('./following-sibling::td/div[@class="hlist"]/ul//text()').extract()
                    l_list = [j.strip() for j in l if j not in ['\n','/',""]]
                    move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
                    l_output = [j.translate(move) for j in l_list if len(j.strip())]
                    if '.com' in l_output:
                        l_result = [re.sub(r'[^\w\s.-–]', '', j) for j in l_output if len(re.sub(r'[^\w\s.-–]', '', j))]
                        json_dict[str(key_word)] = "http://"+''.join(l_result).strip()
                    else:
                        l_result = [re.sub(r'[^\w\s.-–]', '', j) for j in l_output if len(re.sub(r'[^\w\s.-–]', '', j))]
                        if key_word in ["TraditionalChinese","Simplified Chinese"]:
                            json_dict[str(key_word)] = ''.join(l_result).strip()
                        else:
                            json_dict[str(key_word)] = ','.join(l_result).strip()
                else:
                    is_exist_1 = th_list[i].xpath('./following-sibling::td/div[@class="plainlist"]')
                    if is_exist_1:
                        # 文字信息
                        l = th_list[i].xpath('./following-sibling::td/div[@class="plainlist"]/ul//text()').extract()
                        l_list = [j.strip() for j in l if j not in ['\n','/','']]
                        move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
                        l_output = [j.translate(move) for j in l_list]
                        if '.com' in l_output:
                            l_result = [re.sub(r'[^\w\s.-–]', '', j) for j in l_output if len(re.sub(r'[^\w\s.-–]', '', j))]
                            json_dict[str(key_word)] = "http://"+''.join(l_result).strip()
                        else:
                            l_result = [re.sub(r'[^\w\s.-–]', '', j) for j in l_output if len(re.sub(r'[^\w\s.-–]', '', j))]
                            if key_word in ["TraditionalChinese","Simplified Chinese"]:
                                json_dict[str(key_word)] = ''.join(l_result).strip()
                            else:
                                json_dict[str(key_word)] = ','.join(l_result).strip()
                    else:
                        is_exist_b = th_list[i].xpath('./following-sibling::td/div[@class="marriage-display-ws"]')
                        if is_exist_b:
                            # 文字信息
                            l = th_list[i].xpath('./following-sibling::td/div[@class="marriage-display-ws"]//text()').extract()
                            l_list = [j.strip() for j in l if j not in ['\n','/','']]
                            move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
                            l_output = [j.translate(move) for j in l_list]
                            if '.com' in l_output:
                                l_result = [re.sub(r'[^\w\s.-–]', '', j) for j in l_output if len(re.sub(r'[^\w\s.-–]', '', j))]
                                json_dict[str(key_word)] = "http://"+''.join(l_result).strip()
                            else:
                                l_result = [re.sub(r'[^\w\s.-–]', '', j) for j in l_output if len(re.sub(r'[^\w\s.-–]', '', j))]
                                key_info = ','.join(l_result).strip()
                                json_dict[str(key_word)] = re.sub('\u200b', '', key_info)
                        else:
                            # 文字信息
                            l = th_list[i].xpath("./following-sibling::td//text()").extract()
                            l_list = [j.strip() for j in l if j not in ['\n','/','']]
                            move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
                            l_output = [j.translate(move) for j in l_list]
                            if '.com' in l_output:
                                l_result = [re.sub(r'[^\w\s.-–]', '', j) for j in l_output if len(re.sub(r'[^\w\s.-–]', '', j))]
                                json_dict[str(key_word)] = "http://"+''.join(l_result).strip()
                            else:
                                l_result = [re.sub(r'[^\w\s.-–]', '', j) for j in l_output if len(re.sub(r'[^\w\s.-–]', '', j))]
                                if key_word in ["TraditionalChinese","Simplified Chinese"]:
                                    json_dict[str(key_word)] = ''.join(l_result).strip()
                                else:
                                    json_dict[str(key_word)] = ','.join(l_result).strip()
            if len(json_dict)==0:
                item['artist_info'] = None
                item["born"] = None
                item["genres"] = None
                item["labels"] = None
                item["years_active"] = None
                item["website"] = None
                item["occupations"] = None
                item["birth_name"] = None 
                item["origin"] = None
            else:  
                item['artist_info'] = json_dict
                item["born"] = json_dict["Born"] if "Born" in json_dict else None
                item["genres"] = json_dict["Genres"] if "Genres" in json_dict else None
                item["labels"] = json_dict["Labels"] if "Labels" in json_dict else None
                item["years_active"] = json_dict["Years active"] if "Years active" in json_dict else None
                item["website"] = json_dict["Website"] if "Website" in json_dict else None
                item["occupations"] = json_dict["Occupation(s)"] if "Occupation(s)" in json_dict else None
                item["birth_name"] = json_dict["Birth name"] if "Birth name" in json_dict else None 
                item["origin"] = json_dict["Origin"] if "Origin" in json_dict else None
            item["artist_id"] = request.task_artist_id
            item["artist_name"] = request.task_artist_name
            item["gmg_artist_id"] = request.task_gmg_artist_id
            item["gmg_artist_name"] = request.task_gmg_artist_name
            item["batch"] = self.batch_date

            if self._task_table=="wikipedia_artist_batch_task":
                wiki_situation_item = WikipediaArtistCrawlSituationRecordBatchDataItem()
            if self._task_table=="wikipedia_spotify_artist_batch_task":
                wiki_situation_item = WikipediaSpotifyArtistCrawlSituationRecordBatchDataItem()
            wiki_situation_item["gmg_artist_id"] = request.task_gmg_artist_id
            wiki_situation_item["gmg_artist_name"] = request.task_gmg_artist_name
            wiki_situation_item["artist_id"] = request.task_artist_id
            wiki_situation_item["artist_name"] = request.task_artist_name
            wiki_situation_item['artist_infomation_remarks'] = "EI"
            wiki_situation_item["batch"] = self.batch_date
            yield item
            yield wiki_situation_item
            yield self.update_task_batch(request.task_id, 1)
            
        else:
            if self._task_table=="wikipedia_artist_batch_task":
                wiki_situation_item = WikipediaArtistCrawlSituationRecordBatchDataItem()
            if self._task_table=="wikipedia_spotify_artist_batch_task":
                wiki_situation_item = WikipediaSpotifyArtistCrawlSituationRecordBatchDataItem()
            wiki_situation_item["gmg_artist_id"] = request.task_gmg_artist_id
            wiki_situation_item["gmg_artist_name"] = request.task_gmg_artist_name
            wiki_situation_item["artist_id"] = request.task_artist_id
            wiki_situation_item["artist_name"] = request.task_artist_name
            wiki_situation_item['artist_infomation_remarks'] = "NI"
            wiki_situation_item["batch"] = self.batch_date
            yield wiki_situation_item
            yield self.update_task_batch(request.task_id, 1)



if __name__ == "__main__":
    spider = CrawlWikipediaArtistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlWikipediaArtistInfoSpider爬虫")

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
    # python crawl_wikipedia_artist_info_spider.py --start_master  # 添加任务
    # python crawl_wikipedia_artist_info_spider.py --start_worker  # 启动爬虫
