import json
import pymysql 


MYSQL_IP = "122.115.36.92"
MYSQL_PORT = 3306
MYSQL_DB = "temporary_youtube_data"
MYSQL_USER_NAME = "crawler"
MYSQL_USER_PASS = "MYSQL.crawler1"


conn = pymysql.Connect(host=MYSQL_IP,db=MYSQL_DB,port=MYSQL_PORT,user=MYSQL_USER_NAME,password=MYSQL_USER_PASS)
cursor = conn.cursor()

with open("../MyYoutubeJsonFile/14.json","r",encoding='utf-8-sig') as f:
    json_data = json.load(f)


data_list = json_data["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"]
# print(data_list)
for i in data_list[:-1]:
    video_id = i["richItemRenderer"]["content"]["videoRenderer"]["videoId"]
    title = i["richItemRenderer"]["content"]["videoRenderer"]["title"]['runs'][0]['text']
    sql = "INSERT INTO tmp_cx_001(video_id,title) VALUES(%s,%s)"
    cursor.execute(sql,[video_id,title])
    conn.commit()
    print("提交 {} 完成".format(video_id))
    print("========================================================")