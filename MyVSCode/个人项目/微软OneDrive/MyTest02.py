import requests
from onedrivesdk.helpers import GetAuthCodeServer
import time

client_id = "e0e6ed75-c7e2-4a99-9590-1a3eca5b2194"
scope = "files.readwrite offline_access"
redirect_uri = "http://localhost"
client_secret = "2~J8Q~vqjs1_bfR9UwQZaPTC76BpgfZpilHkRdsg"



def get_code():
    # 1.获取授权代码
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={}&scope={}&response_type=code&redirect_uri={}".format(client_id,scope,redirect_uri)
    code = GetAuthCodeServer.get_auth_code(url, redirect_uri)
    return code



def get_mid_token(code):
    # 2.兑换代码以获取访问令牌
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id":client_id,
        "redirect_uri":redirect_uri,
        "client_secret":client_secret,
        "code":code,
        "grant_type":"authorization_code"
    }
    response = requests.post(url=url,headers=headers,data=data).json()
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]
    return access_token,refresh_token


def get_token(access_token,refresh_token):
    # 3.获取新的访问令牌或刷新令牌
    access_token  = "EwBgA8l6BAAUkj1NuJYtTVha+Mogk+HEiPbQo04AAbiKq2YuPKbO79X8Bc97qBasspUVBP5vHxQvaSOCsU+DcV7G70loazUUxuGqiqqZ5ZNjWoZLinMlkFE+XYeH/9Gz7qCrtStiI2+zBtzw+Fv70+b4yJdMNUef2va4YhEt30Tx0S+gYQSkaSJpPrmoXtkaDFf85cp9mZmAgADOcR8obD5HUblMNKrrL7bK/sADNl+5Rc1VH0WGxp/IEKgOALsMy3kINrW2fzJflUO/HfuOgjqMsJjPpLlEeYsotYMV6hio1oQb8CEyJcW7O6E4zrcZr+pjQETtt1NAiaT+1R2Dfn7ajZtpiWXieTEsFMof7SL4sLjsq8nXD/CIsvNauZQDZgAACJBhZteGlYGKMAIMpieRumb9gWUghfXQrteowzurWdEB0P8OmpiOMsfRL5EIJVXUR3UNmfRVxF07k8fBscBj58cwNx1DPn+18lZBa8DnFPsdBYyqHwEa5XAYClXIW8K/kID/9PHr1Yx4jAgVWcuDjTj3NJYUyhFTgExSvhiNlvnMlZ2tPtMAoEJBdVDJw9CeKc7hUxvuUC4jYMYH1hPIq9JEvfljL5m2dKr9c9CndGkGHD8WUMgbaPrtRW0XLi6r7lxJvvpw0xAVvdC/JIBdiHFGdPZqf+COmUdHzWO6z9a05fBDS9d4xOKAPXkpXI0OqEFDllY/T2N3dgXrV6pv1UbAeJvKhYxdFPY/Jj46j3wP+K1YLTNn28ftrr5p9xjHVAB3M5f06/nmlgg2hv1kMNiQXtFHkHu0tU0uoRxntZxizO9cRmPLfmd2AZiBuRM+7XDhi7MFMlSK4q/FNyT6E8cIYGAY8+HC0U7zfDNyjI77CDUJqESaS+jH6M8nXjMUGZXPkVhemDPgPq5X1XHyb/Q5tlnxPWz8a0uMYAxMxwd+QxTgdZc8+9mqXN5P467L+a4dOePSVpYxT2+2IuYwB2IdS42TZjr88Ei0wLbSS9aQQSWz+GSJwNQSTPh5cp9gnqjrrzuZ6wNIJAy1nagT1pkF/1r6LttU3A4x0Ar4WaySaM/Mx0bxJFCwxIA/99/vARP+1MZsYnjm0ZU2cEp6KCo91znV3LhtuXfyQld69a2fNxg+qpb/dtAgjWgC"
    refresh_token = "M.R3_BAY.-CbyfbPN38stnEQxiK0TlfA4ga4DiLT!F8*HdD5TsFM3k8rFx14pJZ2DycqLT*OSpbmfaW39yC*9ZUZHVx0rZz4OgirgRMVM6fu4tBlja6b5GKcn76m!nRfni0!6D418S5MkwOFbiCeA7uSWGOmoXP8sO13!xGgbOcQdjC2rW1f*oA!D6GHSgZ1yj0mA*Nv7!HsdTxPQ0q9ZapVyfBH3!981BGNivyvU5w8ZOlUWYIyZb9FRCTAb2iq!dHchIv6LnzRkTB8By5J6nz4PNZEyPijfrUtIsBifslDDg5u!7tvWFmaCGvmtAQUy5wljaBgAtL3F7L8YvJ4rKl3o8o6hkMHs$"
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id":client_id,
        "redirect_uri":redirect_uri,
        "client_secret":client_secret,
        "refresh_token":refresh_token,
        "grant_type":"refresh_token"
    }
    response = requests.post(url=url,headers=headers,data=data).json()
    token = response["token_type"]+ " " + response["access_token"]
    return token
"""
{'token_type': 'Bearer', 
'scope': 'Files.ReadWrite',
'expires_in': 3600, 
'ext_expires_in': 3600, 
'access_token': 'EwBgA8l6BAAUkj1NuJYtTVha+Mogk+HEiPbQo04AAepzTXETwjb59nLrEggLqU8POULRccHh5Zt+s+03Altnl8QicvhqG56I+p3YY4bl6W8+rVfHgTZcKzhbp/1SWxzFjcLMJ4rY9WkXI43JhT/Bof/61Lfr+Vt0D4aMDIra+flRnzA6E2UKSwv8X3BKiX14pHTnNKyhWYfHSgZtwJivCshQr1IOrOASmvC4nHz0InovA1zDVbKV1zK4ZxrSUW9ckbZfqF+/rmbqLVr4t+REpjjUmyUDWq7DTIji5Dy2MGrT9EiAHCiB+BR1SUl2gh9995wOnM0YDbTa6eucR6KrAB1yWdFYNE6L9jYUVbyOv5STpddx/oMFNtJAOnxDJhcDZgAACHKuZPmXfvMxMAJSZRwgXO5q6zDLPw1ccNEfPTkfFJApZAEqwChTb1nBG2P6RD7XGLp1UQgm0pUbu2I7sSwFUuVoemoogMyNVcefiRX1/kpfm5dZir04lEWyJ4O2Rysb7hJpOUjFh3MLjINGxizVmQR12Q8vD3jGZ4chllRxtuuJrdiaXWLqZ9qqZI+hy77QfmbqL9gwtB0zGbXLVSkM435vHqd+E8571VkREEbrgtvxI6ThEOC1QMMOPksDGdThbrJ0BuyzeM+yM80B9MktKpZM863jWJ3VOo0/jT+sW453LImOfDvPPTosfGczarlP2EozqhHnMGAamBkr+KFbIXFgmsVgteuLJS4t/JbxOnABgb8gsrDlFHyowLahrJrpdqtIOfGFo9S5MrUhthJTAGRie3teJPbUq7l1u/6uFpI6hv3ll4Tq3Rr9Cyqd5mgT6Hdgywg/GjKJU15ll3CLTKWzm0J23d7WWi+iikiNqGOcoaEqhZ6t6rbVBKl9Iwy4d/SaCZC+JN00B2ErCCqJKTpwHOPH/SQP9Qx0bYTUzTMFt7cCrwgPMynAugZlCB09hMlG60vF9QwXAMxefoftcw+3zdx3GY9sawsCGZPo4qDmHk2n0r9P9j2wNXGocJ9AmaiQSlg5RNbIplWezZtc5Re66kAAez84fpq8Tt/qwR8SC/WRC2DZKyYHlDhPecKEghOUiJR31tJ/MEMzNBWwapF8Q/xZsabiM5KpPFTPnMBTieUmfM/4bjkdfmgC'
}
"""

if __name__=="__main__":
    code = get_code()
    time.sleep(3)
    access_token,refresh_token = get_mid_token(code=code)
    token = get_token(access_token=access_token, refresh_token=refresh_token)
    print(token)
    