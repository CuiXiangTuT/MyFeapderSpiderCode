# import pandas as pd

# df = pd.read_excel("./File/临时文件.xlsx")
# df['artist_split'] = df['歌手清洗'].apply(lambda x:x.split(';'))
# df = df.explode("artist_split")
# df.to_excel("./File/修改.xlsx")
# import requests

# url = "http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start=20"
# headers = {
#     "Referer": "http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action",
#     "Host": "www.ccgp-gansu.gov.cn",
#     "Connection": "keep-alive",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
#     "Cookie": "4hP44ZykCTt5S=5hcMCp3CZSi_Jf8aPgLayoJQNiu1w2zdjBu0815oZYO.bpzoZpBvv5kPDkuCgDDNt8wVJsUsIwkvSm2.jaufVBq; JSESSIONID=1C4C212BEC527E2D475FA4C2480F0AF5.tomcat2; 4hP44ZykCTt5T=VWU0GKHAtyYix04_4nlvfiDNnWdZeVRG1Id7BYQrVxMkrtKvFgh48OEvcqimc_saSez.ZkICeX5aQpu2F6QlqYSDvH0zYv9b929PU7JJTPy0o2.jjnUsS3qjOM1so3xpJl_lT8F3MVfzix_p7.adgpH1C3D8SwmGVtaVToouSH9WJL6mbiY.v39WsFAW1AjYwfqjpSUC7qdiSuR5fzfMVbMBmM95Gsi4QQvOLvnnt9YRETxEre.QfHvd7btCken3FWASlvYz7iLNqGryCSK8CYwNpvyBx_VLfW9xMmQSSrpCkGX5Co03rIhYFz0b381iM.gquUJmvKNB0zrrF9Fg9itJtYwXU6C4XZnU2oyhChYYfW2Gc5jYOAA1diatbd_Ervz9lujPIiV8p3_QKdEA7q",
# }
# response = requests.get(url=url,headers=headers).text
# print(response)

import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer
from onedrivesdk.helpers.resource_discovery import ResourceDiscoveryRequest


redirect_uri = 'http://localhost/'
client_id = "e0e6ed75-c7e2-4a99-9590-1a3eca5b2194"
client_secret = "2~J8Q~vqjs1_bfR9UwQZaPTC76BpgfZpilHkRdsg"
api_base_url='https://api.onedrive.com/v1.0/'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

http_provider = onedrivesdk.HttpProvider()
auth_provider = onedrivesdk.AuthProvider(
    http_provider=http_provider,
    client_id=client_id,
    scopes=scopes)

client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
auth_url = client.auth_provider.get_auth_url(redirect_uri)
# Ask for the code
print('Paste this URL into your browser, approve the app\'s access.')
print('Copy everything in the address bar after "code=", and paste it below.')
print(auth_url)
# code = raw_input('Paste code here: ')
# Block thread until we have the code
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
print(code)
# Finally, authenticate!
# client.auth_provider.authenticate(code, redirect_uri, client_secret)


# # 添加文件夹
# f = onedrivesdk.Folder()
# i = onedrivesdk.Item()
# i.name = 'HuTaoFile'
# i.folder = f
# returned_item = client.item(drive='me', id='root').children.add(i)

# # 上传项目
# returned_item = client.item(drive='me', id='root').children['wanYe.txt'].upload('./wanye.txt')
# print(returned_item)
# print("上传成功！")

#  下载项目
# root_folder = client.item(drive='me', id='root:/HuTaoFile/HelloWorld.txt:/content').children.get()
# id_of_file = root_folder[0].id
# name = root_folder[0].name
# client.item(drive='me',id=id_of_file).download(name+'.txt')
# # # print(root_folder)
# print(id_of_file)
# # # print(root_folder[0].name)
# print("下载成功")


# item_id = "root"
# def navigate(client, item_id):
#     items = client.item(id=item_id).children.get()
#     return items
# items = navigate(client, item_id)
# print(items)
print("走到了这里")
# code = "M.R3_BAY.1aae8779-e82c-45a6-a6f8-8f50b5c9e03d"
# client.auth_provider.authenticate(code, redirect_uri, client_secret)

# returned_item = client.item(drive='me', id='root').children['newfile.txt'].upload('./path_to_file.txt')




# redirect_uri = 'http://localhost:8080'
# client_id = "e0e6ed75-c7e2-4a99-9590-1a3eca5b2194"
# client_secret = "2~J8Q~vqjs1_bfR9UwQZaPTC76BpgfZpilHkRdsg"
# discovery_uri = 'https://api.office.com/discovery/'
# auth_server_url='https://login.microsoftonline.com/common/oauth2/authorize'
# auth_token_url='https://login.microsoftonline.com/common/oauth2/token'

# http = onedrivesdk.HttpProvider()
# auth = onedrivesdk.AuthProvider(http,
#                                 client_id,
#                                 auth_server_url=auth_server_url,
#                                 auth_token_url=auth_token_url)
# auth_url = auth.get_auth_url(redirect_uri)
# code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
# auth.authenticate(code, redirect_uri, client_secret, resource=discovery_uri)
# # If you have access to more than one service, you'll need to decide
# # which ServiceInfo to use instead of just using the first one, as below.
# service_info = ResourceDiscoveryRequest().get_service_info(auth.access_token)[0]
# auth.redeem_refresh_token(service_info.service_resource_id)
# client = onedrivesdk.OneDriveClient(service_info.service_resource_id + '/_api/v2.0/', auth, http)
# print("成功")


# 上传文档
# returned_item = client.item(drive='me', id='root').children['newfile.txt'].upload('./path_to_file.txt')

# # 下载项目
# root_folder = client.item(drive='me', id='root').children.get()
# id_of_file = root_folder[0].id

# client.item(drive='me', id=id_of_file).download('./path_to_download_to.txt')



