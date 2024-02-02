# -*- coding: utf-8 -*-
"""
Created on 2023-12-12 17:41:12
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from pprint import pprint
import re


class MyTestAirspider1(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            # "Referer":"https://en.wikipedia.org/wiki/Jaychou",
            # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        return request

    def start_requests(self):
        url = "https://en.wikipedia.org/wiki/Jay_Chou"
        yield feapder.Request(url=url)

    def parse(self, request, response):
        th_list = response.xpath('//th[contains(@scope,"row") and contains(@class,"infobox-label")]')
        item = dict()
        # 歌手名
        artist_name_l = response.xpath('//th[contains(@class,"infobox-above")]/div//text()').extract()
        print(artist_name_l)
        if len(artist_name_l)>1:
            artist_name_l = [k for k in artist_name_l if k not in ['\n','/',""]]
            item["crawl_result_artist_name"] = ' '.join(artist_name_l)
        else:
            item["crawl_result_artist_name"] = artist_name_l[0].strip()
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
        # 歌手图片
        # item["artist_image"] = response.xpath('//td[@class="infobox-image"]/span/a/@href').extract_first()
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
                
        item['artist_info'] = json_dict
        pprint(item)

if __name__ == "__main__":
    MyTestAirspider1().start()