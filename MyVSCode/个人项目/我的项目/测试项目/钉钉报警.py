import requests
import json
import pymysql
import pandas


def send_warning(info):
    url = "https://oapi.dingtalk.com/robot/send?access_token=703c62930dcd94c6b1541956ba8a547b3b8cd4eadfc1b446d779e8fff8b16821"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype":"text",
        "text":{"content":"-----------往生堂第77代堂主胡桃-----------\n\n"+info},
        "at": {
        "atMobiles":[
            "13037639858"
        ],
        "atUserIds":[
            "cxzyq1211"
        ],
        "isAtAll": false
    },
    }
    res = requests.post(url=url,headers=headers,data=json.dumps(data)) # 发送post请求
    print(res.text)

def get_sql_data():
    conn_beijing = pymysql.Connect(host='122.115.36.92',user="reader",password="reader.mysql",port=3306,db="GMG_DATA_ASSETS")
    beijing_count = pandas.read_sql_query("SELECT COUNT(*) FROM gmg_artist_aka WHERE site='spotify'", con=conn_beijing).values[0][0]
    print(beijing_count)
    conn_xianggang = pymysql.Connect(host='47.242.9.112',user="crawler",password="crawler.mysql",port=3306,db="GMG_DATA_ASSETS")
    xianggang_count = pandas.read_sql_query("SELECT COUNT(*) FROM gmg_artist_aka WHERE site='spotify'", con=conn_xianggang).values[0][0]
    print(xianggang_count)

    if beijing_count == xianggang_count:
        info = "北京和香港服务器，数据一致，无需操作"
        send_warning(info)
    else:
        info = "北京和香港服务器，数据库数据未同步，请及时确认"
        send_warning(info)

if __name__ == '__main__':
    get_sql_data()