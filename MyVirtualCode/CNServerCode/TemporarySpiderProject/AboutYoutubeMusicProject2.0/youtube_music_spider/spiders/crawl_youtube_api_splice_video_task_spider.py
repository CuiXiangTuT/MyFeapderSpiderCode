# -*- coding: utf-8 -*-
"""
Created on 2024-01-03 15:00:15
---------
@summary:
---------
@author: QiuQiuRen
@description：
    用于将youtube_music_video_task产生的youtube_music_video_id按照每50个为一组进行拼接
"""
import pymysql
import hashlib

MYSQL_IP = "122.115.36.92"
MYSQL_PORT = 3306
MYSQL_DB = "temporary_youtube_music_data"
MYSQL_USER_NAME = "crawler"
MYSQL_USER_PASS = "MYSQL.crawler1"

# 连接到数据库
connection = pymysql.connect(host=MYSQL_IP, user=MYSQL_USER_NAME, password=MYSQL_USER_PASS, database=MYSQL_DB)
cursor = connection.cursor()

# 查询数据库表的数据
cursor.execute("SELECT youtube_video_id FROM api_youtube_playlist_info_data")
results = cursor.fetchall()

grouped_data = []
group = []

# 将每50个元素为一组进行组合
for index, row in enumerate(results, 1):
    group.append("&id="+row[0])

    if index % 50 == 0:
        grouped_data.append(group)
        group = []

# 处理最后一组不满五个元素的情况
if group:
    grouped_data.append(group)

# 打印每五个元素组合后的结果
for group in grouped_data:
    ids = "".join(group)
    md5_obj = hashlib.md5()
    md5_obj.update(ids.encode('utf-8'))
    encrypted_string = md5_obj.hexdigest()

    insert_sql = "INSERT INTO api_youtube_video_info_task(youtube_video_ids,youtube_video_ids_md5) VALUES(%s,%s)"
    cursor.execute(insert_sql,[ids,encrypted_string])
    connection.commit()

# 关闭数据库连接
cursor.close()
connection.close()