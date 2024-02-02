import requests
import re
import json

url = "https://www.youtube.com/watch?v=ocDo3ySyHSI"
response = requests.get(url)

data = re.findall(r'var ytInitialPlayerResponse = (.*?)</script>.*<div id="player"',response.text,re.S)[0][:-1]
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
