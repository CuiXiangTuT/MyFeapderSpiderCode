import requests
from onedrivesdk.helpers import GetAuthCodeServer
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

client_id = "e0e6ed75-c7e2-4a99-9590-1a3eca5b2194"
scope = "files.readwrite offline_access"
redirect_uri = "http://localhost"
client_secret = "2~J8Q~vqjs1_bfR9UwQZaPTC76BpgfZpilHkRdsg"



def get_code():
    # 1.获取授权代码
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={}&scope={}&response_type=code&redirect_uri={}".format(client_id,scope,redirect_uri)
    # code = GetAuthCodeServer.get_auth_code(url, redirect_uri)
    print(url)


if __name__=="__main__":
    get_code()
