"""
@description：
    目的是将北京服务器上抓取到的状态为-1任务传输至香港（非洲）服务器，让香港（非洲）服务器做数据采集

    注意：本程序做长期部署
"""
from setting import *
import pandas
import pymysql

def transfer_task_data_bj_to_hk():
    """
    传输失败的任务从北京到香港
    """
    # 此处为测试，使用的为本地服务器
    bj_af_conn = pymysql.Connect(
        host=BJ_MYSQL_IP,
        port=BJ_MYSQL_PORT,
        database=BJ_MYSQL_DB,
        user=BJ_MYSQL_USER_NAME,
        password=BJ_MYSQL_USER_PASS
        )
    bj_af_cursor = bj_af_conn.cursor()

    # 1-歌手任务数据（将北京服务器歌手任务状态为-1的数据传输至香港（非洲）服务器）
    sql_boomplay_artist_info_task = """
    SELECT gmg_artist_id,gmg_artist_name,boomplay_artist_id,boomplay_artist_name FROM boomplay_artist_info_batch_task
    WHERE state=-1 OR artist_album_track_state=-1
    """
    bj_af_cursor.execute(sql_boomplay_artist_info_task)
    artist_info_task_data = bj_af_cursor.fetchall()
    df_artist_info_task_data = pandas.DataFrame(artist_info_task_data,columns=['gmg_artist_id','gmg_artist_name','boomplay_artist_id','boomplay_artist_name'])

    # 2-专辑任务数据（将北京服务器专辑任务状态为-1的数据传输至香港（非洲）服务器）
    sql_boomplay_album_info_task = """
    SELECT album_id FROM boomplay_album_info_batch_task WHERE state=-1
    """
    bj_af_cursor.execute(sql_boomplay_album_info_task)
    album_info_task_data = bj_af_cursor.fetchall()
    df_album_info_task_data = pandas.DataFrame(album_info_task_data,columns=['album_id'])

    # 3-歌曲任务数据（将北京服务器歌曲任务状态为-1的数据传输至香港（非洲）服务器）
    sql_boomplay_track_info_task = """
    SELECT track_id FROM boomplay_track_info_batch_task WHERE state=-1 OR views_state=-1
    """
    bj_af_cursor.execute(sql_boomplay_track_info_task)
    track_info_task_data = bj_af_cursor.fetchall()
    df_track_info_task_data = pandas.DataFrame(track_info_task_data,columns=['track_id'])
    bj_af_cursor.close()
    bj_af_conn.close()

    hk_conn = pymysql.Connect(
        host=HK_MYSQL_IP,
        port=HK_MYSQL_PORT,
        database=HK_MYSQL_DB,
        user=HK_MYSQL_USER_NAME,
        password=HK_MYSQL_USER_PASS
        )
    hk_cursor = hk_conn.cursor()
    # 1-1 将北京服务器歌手任务状态为-1的数据传输至香港（非洲）服务器
    for i in range(len(df_artist_info_task_data)):
        gmg_artist_id = df_artist_info_task_data.iloc[i]['gmg_artist_id']
        gmg_artist_name = df_artist_info_task_data.iloc[i]['gmg_artist_name']
        boomplay_artist_id = df_artist_info_task_data.iloc[i]['boomplay_artist_id']
        boomplay_artist_name = df_artist_info_task_data.iloc[i]['boomplay_artist_name']
        hk_boomplay_artist_info_task_sql = "INSERT IGNORE INTO boomplay_artist_info_batch_task(`gmg_artist_id`,`gmg_artist_name`,`boomplay_artist_id`,`boomplay_artist_name`) VALUES(%s,%s,%s,%s)"
        hk_cursor.execute(hk_boomplay_artist_info_task_sql,[gmg_artist_id,gmg_artist_name,boomplay_artist_id,boomplay_artist_name])
        hk_conn.commit()
    print("歌手任务数据传输完成！开始传输专辑任务数据")

    # 2-1 将北京服务器专辑任务状态为-1的数据传输至香港（非洲）服务器
    for i in range(len(df_album_info_task_data)):
        album_id = df_album_info_task_data.iloc[i]['album_id']
        hk_boomplay_album_info_task_sql = "INSERT IGNORE INTO boomplay_album_info_batch_task(`album_id`) VALUES(%s)"
        hk_cursor.execute(hk_boomplay_album_info_task_sql,[album_id])
        hk_conn.commit()
    print("专辑任务数据传输完成！开始传输歌曲任务数据")

    # 3-1 将北京服务器专辑任务状态为-1的数据传输至香港（非洲）服务器
    for i in range(len(df_track_info_task_data)):
        track_id = df_track_info_task_data.iloc[i]['track_id']
        hk_boomplay_track_info_task_sql = "INSERT IGNORE INTO boomplay_track_info_batch_task(`track_id`) VALUES(%s)"
        hk_cursor.execute(hk_boomplay_track_info_task_sql,[track_id])
        hk_conn.commit()
    print("歌曲任务传输完成！")
    hk_cursor.close()
    hk_conn.close()

if __name__ == '__main__':
    transfer_task_data_bj_to_hk()