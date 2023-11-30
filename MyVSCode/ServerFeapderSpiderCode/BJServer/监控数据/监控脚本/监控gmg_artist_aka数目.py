import pymysql
import requests
import json
import datetime

def get_bj_mysql_count():
    MYSQL_IP = "122.115.36.92"
    MYSQL_PORT = 3306
    MYSQL_DB = "GMG_DATA_ASSETS"
    MYSQL_USER_NAME = "reader"
    MYSQL_USER_PASS = "reader.mysql"
    conn = pymysql.Connect(host=MYSQL_IP,user=MYSQL_USER_NAME,password=MYSQL_USER_PASS,port=MYSQL_PORT,db=MYSQL_DB)
    cursor = conn.cursor()
    sql = """
    SELECT COUNT(id) FROM `gmg_artist_aka`
    WHERE site = 'spotify' AND id != '-' AND id IS NOT NULL
    """
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result

def get_hk_mysql_count():
    MYSQL_IP = "8.218.99.123"
    MYSQL_PORT = 3306
    MYSQL_DB = "GMG_DATA_ASSETS"
    MYSQL_USER_NAME = "crawler"
    MYSQL_USER_PASS = "crawler.mysql"
    conn = pymysql.Connect(host=MYSQL_IP,user=MYSQL_USER_NAME,password=MYSQL_USER_PASS,port=MYSQL_PORT,db=MYSQL_DB)
    cursor = conn.cursor()
    sql = """
    SELECT COUNT(id) FROM `gmg_artist_aka`
    WHERE site = 'spotify' AND id != '-' AND id IS NOT NULL
    """
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result

def send_dingding_warning(info):
    url = "https://oapi.dingtalk.com/robot/send?access_token=703c62930dcd94c6b1541956ba8a547b3b8cd4eadfc1b446d779e8fff8b16821"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype":"text",
        "text":{"content":"-----------热榜数据采集任务监控-----------\n\n"+info},
        "at": {
            "atMobiles":[
                "13037639858"
            ],
            "atUserIds":[
                "cxzyq1211"
            ],
            "isAtAll": False
        }
    }
    res = requests.post(url=url,headers=headers,data=json.dumps(data)) # 发送post请求
    print(res.text)


def compare_result():
    bj = get_bj_mysql_count()
    hk = get_hk_mysql_count()
    isEqual = True if bj==hk else False
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if isEqual:
        info = "日期：{}\n数据一致，无需操作\n北京数据条目数：{}\n香港数据条目数：{}\n".format(current_date,bj,hk)
        send_dingding_warning(info)
    else:
        info = "日期：{}\n数据有差异，请及时查询数据库表情况，给予反馈\n北京数据条目数：{}\n香港数据条目数：{}\n".format(current_date,bj,hk)
        send_dingding_warning(info)


if __name__ == '__main__':
    compare_result()