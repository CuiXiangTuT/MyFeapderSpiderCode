import requests
import json
import time

# 根据情况填写这一部分
auth_api="https://login.partner.microsoftonline.cn/common/oauth2/v2.0/token"
drive_api="https://microsoftgraph.chinacloudapi.cn/v1.0/me/drive"
refresh_token=""

refresh_time=0
token=""

def get_head():
    global refresh_time,token,refresh_token,auth_api
    if time.time()>refresh_time:
        data={
            'client_id':'',
            'client_secret':'',
            'redirect_uri':'http://localhost',
            'refresh_token':refresh_token,
            'grant_type':'refresh_token'
        }
        dic=requests.post(auth_api,data=data).json()
        refresh_time=time.time()+dic['expires_in']-11
        token='bearer '+dic['access_token']
    return {
    'Authorization':token
    }

def get_path(path,op):
    if path[0]=='/': path=path[1:]
    if path[-1]=='/': path=path[:-1]
    if op[0]=='/': op=op[1:]
    return drive_api+'/root:/{}:/{}'.format(path,op)


def upload_url(path,conflict="fail"):
    data = {
        "item": {
            "@microsoft.graph.conflictBehavior": conflict
        }
    }
    r=requests.post(get_path(
        path, 'createUploadSession'), headers=get_head(), json=data)
    if r.status_code==200:
        return r.json()['uploadUrl']
    else: return ""


# data是二进制
def upload_file(path, data):
    size = len(data)
    if size > 4000000:
        url = upload_url(path)
        chunk_size = 3276800
        for i in range(0, size, chunk_size):
            print(i/size,i,size)
            chunk_data = data[i:i+chunk_size]
            r = requests.put(url, headers={'Content-Length': str(len(chunk_data)),
                             'Content-Range': 'bytes {}-{}/{}'.format(i, i+len(chunk_data)-1, size)}, data=chunk_data)
            if r.status_code != 202:
                break
    else:
        r = requests.put(get_path(path, 'content'),
                         headers=get_head(), data=data)
    if r.status_code == 200 or r.status_code == 201:
        return True
    else:
        return False

def create_folder(path,name):
    data=json.dumps({
        "name":name,
        "folder":{},
    })
    r=requests.post(get_path(path,'children'),headers=get_head(),data=data)
    return r.status_code

upload_file("/test.txt","小苏!!~\(≧▽≦)/~".encode("utf-8"))