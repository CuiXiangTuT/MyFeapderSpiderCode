import pymysql
import pandas

MYSQL_IP = "122.115.36.92"
MYSQL_PORT = 3306
MYSQL_DB = "music_data"
MYSQL_USER_NAME = "crawler"
MYSQL_USER_PASS = "crawler.mysql"

conn = pymysql.connect(host=MYSQL_IP,port=MYSQL_PORT,user=MYSQL_USER_NAME,password=MYSQL_USER_PASS,db=MYSQL_DB)
cursor = conn.cursor()

data = pandas.read_excel('./af-ghana-artist_batch1.xlsx',sheet_name='af-ghana-artist_batch',usecols=[0,2,8,9])
for i in range(len(data)):
    gmg_artist_id = data.iloc[i]["gmg_artist_id"]
    gmg_artist_name = data.iloc[i]["gmg_artist_name"]
    boomplay_artist_id = data.iloc[i]["boomplay_artist_id"]
    boomplay_artist_name = data.iloc[i]["boomplay_artist_name"]
    sql = '''
    INSERT IGNORE INTO `boomplay_artist_info_batch_task`
    (gmg_artist_id,gmg_artist_name,boomplay_artist_id,boomplay_artist_name,usable) 
    VALUES("{}","{}","{}","{}","{}")
    '''.format(gmg_artist_id,gmg_artist_name,boomplay_artist_id,boomplay_artist_name,1)
    cursor.execute(sql)
    conn.commit()

    update_sql = """
    UPDATE `boomplay_artist_info_batch_task`
    SET gmg_artist_id="{}",gmg_artist_name="{}",boomplay_artist_name="{}"
    WHERE boomplay_artist_id="{}"
    """.format(gmg_artist_id,gmg_artist_name,boomplay_artist_name,boomplay_artist_id)
    cursor.execute(update_sql)
    conn.commit()
    print("更新 gmg_artist_id={} 数据完成".format(gmg_artist_id))
    