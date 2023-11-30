import requests
import re,json


url = "https://www.youtube.com/watch?v=SJKoWAd5ySo"
print(url)
headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
response = requests.get(url,headers)
if response.status_code==200:
    print("进来了")
    # data = re.findall(r'.*var ytInitialPlayerResponse = (.*?)</script>.*<div id="player".*',response.text,re.S)[0][:-1]
    data = re.findall(r'var ytInitialPlayerResponse = (.*?)</script>.*<div id="player"',response.text,re.S)[0][:-1]
    print(data)
    json_data = json.loads(data)['videoDetails']
    print(json_data)
    item = dict()
    #  标题
    item["title"] = json_data["title"]
    # video_id
    item["video_id"] = json_data["videoId"]
    # 时长？
    item["duration"] = json_data["lengthSeconds"]
    # channelId
    item["channel_id"] = json_data["channelId"]
    # 播放量
    item["views"] = json_data['viewCount']
    # 作者
    item['channel_name'] = json_data['author']
    # 简述
    item["description"] = json_data['shortDescription'].replace("\n"," ")
    print(item)