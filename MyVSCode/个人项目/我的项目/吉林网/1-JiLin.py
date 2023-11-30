import requests
import execjs


def get_ss():
    url = "http://www.ccgp-jilin.gov.cn/ext/search/keyPair.action"
    headers = {
        "Host": "www.ccgp-jilin.gov.cn",
        "Cookie": "_gscu_1208125908=632990502ozp4i17; _gscbrs_1208125908=1; _gscs_1208125908=t63922518d8ip3v14|pv:3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42"
    }
    response = requests.post(url=url, headers=headers).json()

    exponent = response["map"]["exponent"]
    modulus = response["map"]["modulus"]
    keyId = response["keyId"]

    ctx = execjs.compile(open("../MyJS/JiLin.js").read())
    rsa_text = ctx.call('dd', exponent, modulus, keyId)
    return rsa_text

url = "http://www.ccgp-jilin.gov.cn/ext/search/morePolicyGonggaoAjax.action"
headers = {
    "Cookie": "_gscu_1208125908=632990502ozp4i17; _gscbrs_1208125908=1; _gscs_1208125908=t63924523l5iri014|pv:1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42"
}

data = {
    "categoryId": "124",
    "num": 10,
    "id": "9,10",
    "orderby": "createTime",
    "ss":get_ss()
}
response = requests.post(url=url,headers=headers,data=data).json()
print(response)
