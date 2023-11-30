
import requests as ss

url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList'
print('-------------------------')
data = {
    "current": 1,  
    "rowCount": "10",
    "infoTypeCode": "1002",
    "privateOrCity": "1",
}
res = ss.post(url=url,data=data)
print('-------------------------')
print(res.text)
print('-------------------------')