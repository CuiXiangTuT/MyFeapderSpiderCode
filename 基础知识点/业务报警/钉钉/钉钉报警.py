# https://oapi.dingtalk.com/robot/send?access_token=942adf7fff6f0685127f8b6b09541c81045f8dc50f6269c964bea0316150757d
import requests
import json

url = "https://oapi.dingtalk.com/robot/send?access_token=703c62930dcd94c6b1541956ba8a547b3b8cd4eadfc1b446d779e8fff8b16821"
headers = {
    "Content-Type": "application/json"
}
data = {
    "msgtype":"text",
    "text":{"content":"-----------往生堂第77代堂主胡桃-----------\n秋秋大魔王来咯~"}
}
res = requests.post(url=url,headers=headers,data=json.dumps(data)) # 发送post请求
print(res.text)
