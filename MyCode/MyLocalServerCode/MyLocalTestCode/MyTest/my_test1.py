import requests 
import re
from pprint import pprint


url = "https://music.youtube.com/channel/UCL2MDNdwEtV6aYUgNjFQGZA"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

response = requests.get(url,headers=headers).text

pattern = r"initialData\.push\({([\s\S]*?)}\);"
matches = re.findall(pattern, response)
if len(matches) >= 2:
    second_data = matches[1]
    print(second_data)
else:
    print("无法找到第二个initialData.push的值")