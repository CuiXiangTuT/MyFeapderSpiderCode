# -*- coding: utf-8 -*-
import time
# import yccc.yasuo_tool as s
import json
from lxml import etree
import re
import datetime
import requests as ss
import ddddocr
from w3lib.html import remove_tags

def yzm():
    print(111111111111111111111111111111111111)
    yzm_time = int(time.time())
    yzm_url = 'https://cg.95306.cn/proxy/portal/enterprise/base/loadComplexValidCodeImg?validCodeKey=%s&timestamp=%s' % (str(yzm_time), str(yzm_time))
    ocr = ddddocr.DdddOcr()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    yzm_res = ss.get(yzm_url, headers=headers)
    with open('gtcg.png', 'wb') as f:
        f.write(yzm_res.content)
    with open('gtcg.png', 'rb') as f:
        img_bytes = f.read()
    yam_code = ocr.classification(img_bytes)
    # print(yam_code)
    post_yzm = 'https://cg.95306.cn/proxy/portal/elasticSearch/checkRequestNumValidateCode'
    post_data = {
        "picValidCodeKey": str(yzm_time),
        "picValidCode": yam_code,
    }
    yzm_res = ss.post(post_yzm, data=post_data,headers=headers)
    data_yzm =  json.loads(yzm_res.text)
    print(data_yzm['msg'])
    if data_yzm['msg'] =='图形验证码填写错误，请重新填写':
        time.sleep(2)
        yzm()

def data_item(response,item,title):
    print(response.text)
    html = json.loads(response.text)
    content = etree.HTML(html['data']['noticeContent']['notCont'])
    # result = remove_tags(data).replace('&nbsp;', '').split('\n')
    # print(html['data']['noticeContent']['notCont'])
    # try:
    #     data_content = content.xpath('//div[@align="center"]/descendant::text()')
    # except:
    data_content = content.xpath('//descendant::text()')
    content_list = []
    for content_one in data_content:
        if content_one.split():
            content_list.append(content_one.split()[0])
    content_one = ''
    # print(content_list)
    for data_content_list in content_list[:]:
        content_data = ''
        for data_content_one in data_content_list.split():
            content_data += data_content_one
        content_one += content_data
    if '详见附件' in content_one:
        print(11111)
        return 1
    try:
        content_one = re.findall('公示如下(.*)', content_one)[0]
    except:
        content_one = content_one.replace(r'%s' % title, '')
    print(content_one)

    try:
        item['win_supply_name'] = re.findall('成交人(.*?)成交总价', content_one)[0].replace('：', '').replace('-', '')
    except:
        try:
            item['win_supply_name'] = re.findall('候选人为(.*?)，', content_one)[0].replace('：', '').replace('-', '')
        except:
            try:
                item['win_supply_name'] = re.findall('成交候选人(.*?)公示期', content_one)[0].replace('：', '').replace('-', '')
            except:
                try:
                    item['win_supply_name'] = re.findall('成交候选人(.*?)公示时间', content_one)[0].replace('-', '').replace('：', '')
                except:
                    try:
                        item['win_supply_name'] = re.findall('第1名(.*?)第2名：', content_one)[0].replace('-', '').replace('：', '')
                    except:
                        try:
                            item['win_supply_name'] = re.findall('第一名(.*?)第二名', content_one)[0].replace('-', '').replace('：', '')
                        except:
                            try:
                                item['win_supply_name'] = re.findall('第一名(.*?)公示期', content_one)[0].replace('-', '').replace('：', '')
                            except:
                                try:
                                    item['win_supply_name'] = re.findall('拟成交人(.*?)公示时间：', content_one)[0].replace('-', '').replace('：', '')
                                except:
                                    try:
                                        item['win_supply_name'] = re.findall('中商候选人(.*?)公司', content_one)[0].replace('：', '') + '公司'
                                    except:
                                        try:
                                            item['win_supply_name'] = re.findall('中商单位(.*?)公司', content_one)[0].replace('：', '') + '公司'
                                        except:
                                            print(content_one)
    try:
        if '成交人' in item['win_supply_name']:
            item['win_supply_name'] = re.findall('成交人(.*)', item['win_supply_name'])[0]
        if '供应商' in item['win_supply_name']:
            item['win_supply_name'] = re.findall('供应商(.*)', item['win_supply_name'])[0]
        if '成交候选人' in item['win_supply_name']:
            item['win_supply_name'] = re.findall('成交候选人(.*)', item['win_supply_name'])[0]
        if '候选人' in item['win_supply_name']:
            item['win_supply_name'] = re.findall('候选人(.*)', item['win_supply_name'])[0]
        if '包' in item['win_supply_name']:
            item['win_supply_name'] = re.findall('包(.*)', item['win_supply_name'])[0]
        if '1.' in item['win_supply_name']:
            item['win_supply_name'] = re.findall('1.(.*)', item['win_supply_name'])[0]
        if '公司' in item['win_supply_name']:
            item['win_supply_name'] = re.findall('(.*?)公司', item['win_supply_name'])[0].replace(':', '') + '公司'
    except:
        pass

    print("---------------------->",item)

def haha():
    url = 'https://cg.95306.cn/proxy/portal/elasticSearch/queryProcurementResultsList'
    for i in range(3,4):
        # i = 1
        data = {
            "projBidType": "01",
            "bidType": "",
            "noticeType": "07",
            "title": "",
            "inforCode": "",
            "startDate": "",#"2023-08-03",
            "endDate":"",#"2023-08-09",
            "pageNum": str(i),
            "projType": "",
            "professionalCode": "",
            "createPeopUnit": "",
        }
        query = list(map(lambda item: item[0] + '=' + item[1], data.items()))
        query_str = '&'.join(query)
        spider_init_url = url + '?' + query_str
        res = ss.get(url=spider_init_url)
        # print(res.text)


        data_list = json.loads(res.text)
        for data in data_list['data']['resultData']['result']:
            notice_link = 'https://cg.95306.cn/baseinfor/notice/informationShow?id='+ data['id']
            url_data = 'https://cg.95306.cn/proxy/portal/elasticSearch/indexView?noticeId='+ data['id']
            title = data['notTitle']
            bidpubdate = data['checkTime']
            type = data['projTypeName']
            zclx = data['bidTypeName']
            print(notice_link)
            # print('标题:',title)
            # print(bidpubdate)
            # print(type)
            # print(zclx)
            item = {
                # 'notice_link':notice_lin`k,
                # 'title':title,
                # 'bidpubdate':bidpubdate,
                # 'type':type,
                # 'zclx':zclx,`
            }
            # time.sleep(10)
            yzm()
            response = ss.get(url=url_data)
            if '流标' in response.text or '废标' in response.text or '作废' in response.text :
                continue
            data_item(response,item,title)
            # break
# yzm()
haha()
