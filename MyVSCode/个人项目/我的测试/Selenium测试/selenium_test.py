from selenium import webdriver
from selenium.webdriver.common.by import By

chrome = webdriver.Chrome()
chrome.get('https://bulletin.cebpubservice.com/resource/ceb/js/pdfjs-dist/web/viewer.html?file=https://bulletin.cebpubservice.com/details/bulletin/getBulletin/8a94947586c9310b0189309cbdf908d0')
# chrome.switch_to_frame("iframe")
# name = chrome.find_element(By.XPATH,'//h2[@data-e2e="user-title"]').text
# print(name)
# chrome.close()
# print(chrome.page_source)
# trs = chrome.find_element_by_tag_name("left: 83.2957px; top: 241.021px; font-size: 18.3235px; font-family: sans-serif; transform: scaleX(1.00019);")
# print(trs)
# import random 
# import time
# # var ids=(random.random()*10000000).toString(16).substr(0,4)+'-'+(new Date()).getTime()+'-'+Math.random().toString().substr(2,5);
# print(random.random())
# ids = str(random.random()*10000000)[:4]+"-"+str(int(round(time.time() * 1000)))+'-'+str(random.random()*10000000)[2:7]
with open('District_Advisory_patna_17.pdf', 'wb') as f:
    f.write(chrome.page_source)
    print("保存陈宫")
# print(ids)