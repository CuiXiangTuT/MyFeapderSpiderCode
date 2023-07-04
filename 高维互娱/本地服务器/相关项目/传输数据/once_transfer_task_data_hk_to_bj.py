"""
@description：
    目的是实现将香港服务器（非洲）上boomplay的task任务数据，传输到北京服务器上，作任务添加,
    以及将歌手-专辑映射、歌手-歌曲映射、专辑-歌曲映射进行传输

    注意：本程序仅做一次运行，第一次做全量传输，运行时间较长

    控制传输的频率：每月1号、16号传一次
"""
from setting import *
import pymysql
import pandas

def transfer_task_data_hk_to_bj():
    """
    传输任务数据从香港到北京
    """
    hk_conn = pymysql.Connect(
        host=HK_MYSQL_IP,
        port=HK_MYSQL_PORT,
        database=HK_MYSQL_DB,
        user=HK_MYSQL_USER_NAME,
        password=HK_MYSQL_USER_PASS
        )
    hk_cursor = hk_conn.cursor()
    # 1-从boomplay_artist_info_batch_task抽出歌手任务数据
    sql_artist_info_task = """
    SELECT gmg_artist_id,gmg_artist_name,boomplay_artist_id,boomplay_artist_name
    FROM boomplay_artist_info_batch_task
    """
    hk_cursor.execute(sql_artist_info_task)
    artist_info_task_data = hk_cursor.fetchall()
    # 1-1歌手任务数据：boomplay_artist_info_batch_task
    df_artist_info_task = pandas.DataFrame(artist_info_task_data,columns=['gmg_artist_id','gmg_artist_name','boomplay_artist_id','boomplay_artist_name'])
    
    # 2-从boomplay_album_info_batch_task抽出专辑任务数据
    sql_album_info_task = """
    SELECT album_id FROM boomplay_album_info_batch_task
    """
    hk_cursor.execute(sql_album_info_task)
    album_info_task_data = hk_cursor.fetchall()
    # 2-1专辑任务数据：boomplay_album_info_batch_task
    df_album_info_task = pandas.DataFrame(album_info_task_data,columns=['album_id'])

    # 3-从boomplay_track_info_batch_task抽出歌曲任务数据
    sql_track_info_task = """
    SELECT track_id FROM boomplay_track_info_batch_task
    """
    hk_cursor.execute(sql_track_info_task)
    track_info_task_data = hk_cursor.fetchall()
    # 3-1 歌曲任务数据：boomplay_track_info_batch_task
    df_track_info_task = pandas.DataFrame(track_info_task_data,columns=['track_id'])

    # 4-从boomplay_artist_album_batch_data抽出歌手-专辑映射数据
    sql_artist_album_map_data = """
    SELECT boomplay_artist_id,album_id FROM boomplay_artist_album_batch_data
    """
    hk_cursor.execute(sql_artist_album_map_data)
    artist_album_map_data = hk_cursor.fetchall()
    # 4-1 歌手-专辑映射数据：boomplay_artist_album_batch_data
    df_artist_album_map_data = pandas.DataFrame(artist_album_map_data,columns=['boomplay_artist_id','album_id'])

    # 5-从boomplay_artist_track_batch_data抽出歌手-歌曲映射数据
    sql_artist_track_map_data = """
    SELECT boomplay_artist_id,track_id FROM boomplay_artist_track_batch_data
    """
    hk_cursor.execute(sql_artist_track_map_data)
    artist_track_map_data = hk_cursor.fetchall()
    # 5-1 歌手-歌曲映射数据：
    df_artist_track_map_data = pandas.DataFrame(artist_track_map_data,columns=['boomplay_artist_id','track_id'])

    # 6-从boomplay_album_track_batch_data抽出专辑-歌曲映射数据
    sql_album_track_map_data = """
    SELECT album_id,track_id FROM boomplay_album_track_batch_data
    """
    hk_cursor.execute(sql_album_track_map_data)
    album_track_map_data = hk_cursor.fetchall()
    df_album_track_map_data = pandas.DataFrame(album_track_map_data,columns=['album_id','track_id'])

    hk_cursor.close()
    hk_conn.close()

    # 此处为测试，使用的为本地服务器
    bj_af_conn = pymysql.Connect(
        host=LOCAL_AF_MYSQL_IP,
        port=LOCAL_AF_MYSQL_PORT,
        database=LOCAL_AF_MYSQL_DB,
        user=LOCAL_AF_MYSQL_USER_NAME,
        password=LOCAL_AF_MYSQL_USER_PASS
        )
    bj_af_cursor = bj_af_conn.cursor()

    print("准备开始插入数据！")

    # 1-1-1 将从香港服务器抽取出来的boomplay_artist_info_task放入至北京服务器boomplay_artist_info_task
    for i in range(len(df_artist_info_task)):
        gmg_artist_id = df_artist_info_task.iloc[i]['gmg_artist_id']
        gmg_artist_name = df_artist_info_task.iloc[i]['gmg_artist_name']
        boomplay_artist_id = df_artist_info_task.iloc[i]['boomplay_artist_id']
        boomplay_artist_name = df_artist_info_task.iloc[i]['boomplay_artist_name']
        bj_boomplay_artist_info_task_sql = "INSERT IGNORE INTO boomplay_artist_info_batch_task(`gmg_artist_id`,`gmg_artist_name`,`boomplay_artist_id`,`boomplay_artist_name`) VALUES(%s,%s,%s,%s)"
        bj_af_cursor.execute(bj_boomplay_artist_info_task_sql,[gmg_artist_id,gmg_artist_name,boomplay_artist_id,boomplay_artist_name])
        bj_af_conn.commit()
    print("歌手任务数据传输完成！开始传输专辑任务数据")
    
    # 2-1-1 将从香港服务器抽取出来的boomplay_album_info_task放入至北京服务器boomplay_album_info_task
    for i in range(len(df_album_info_task)):
        album_id = df_album_info_task.iloc[i]['album_id']
        bj_boomplay_album_info_task_sql = "INSERT IGNORE INTO boomplay_album_info_batch_task(`album_id`) VALUES(%s)"
        bj_af_cursor.execute(bj_boomplay_album_info_task_sql,[album_id])
        bj_af_conn.commit()
    print("专辑任务数据传输完成！开始传输歌曲任务数据")

    # 3-1-1 将从香港服务器抽取出来的boomplay_track_info_task放入至北京服务器boomplay_track_info_task
    for i in range(len(df_track_info_task)):
        track_id = df_track_info_task.iloc[i]['track_id']
        bj_boomplay_track_info_task_sql = "INSERT IGNORE INTO boomplay_track_info_batch_task(`track_id`) VALUES(%s)"
        bj_af_cursor.execute(bj_boomplay_track_info_task_sql,[track_id])
        bj_af_conn.commit()
    print("歌曲任务数据传输完成！开始传输歌手-专辑映射数据")
    
    # 4-1-1 将从香港服务器抽取出来的boomplay_artist_album_batch_data放入至北京服务器boomplay_artist_album_batch_data
    for i in range(len(df_artist_album_map_data)):
        boomplay_artist_id = df_artist_album_map_data.iloc[i][0]
        album_id = df_artist_album_map_data.iloc[i][1]
        bj_boomplay_artist_album_batch_data_sql = "INSERT IGNORE INTO boomplay_artist_album_batch_data(`boomplay_artist_id`,`album_id`) VALUES(%s,%s)"
        bj_af_cursor.execute(bj_boomplay_artist_album_batch_data_sql,[boomplay_artist_id,album_id])
        bj_af_conn.commit()
    print("歌手-专辑数据传输完成！开始传输歌手-歌曲映射数据")

    # 5-1-1 将从香港服务器抽取出来的boomplay_artist_track_batch_data放入至北京服务器boomplay_artist_track_batch_data
    for i in range(len(df_artist_track_map_data)):
        boomplay_artist_id = df_artist_track_map_data.iloc[i][0]
        track_id = df_artist_track_map_data.iloc[i][1]
        bj_boomplay_artist_track_batch_data_sql = "INSERT IGNORE INTO boomplay_artist_track_batch_data(`boomplay_artist_id`,`track_id`) VALUES(%s,%s)"
        bj_af_cursor.execute(bj_boomplay_artist_track_batch_data_sql,[boomplay_artist_id,track_id])
        bj_af_conn.commit()
    print("歌手-歌曲数据传输完成！开始传输专辑-歌曲映射数据")

    # 6-1-1 将从香港服务器抽取出来的boomplay_album_track_batch_data放入至北京服务器器boomplay_album_track_batch_data
    for i in range(len(df_album_track_map_data)):
        album_id = df_album_track_map_data.iloc[i][0]
        track_id = df_album_track_map_data.iloc[i][1]
        bj_boomplay_album_track_batch_data_sql = "INSERT IGNORE INTO boomplay_album_track_batch_data(`album_id`,`track_id`) VALUES(%s,%s)"
        bj_af_cursor.execute(bj_boomplay_album_track_batch_data_sql,[album_id,track_id])
        bj_af_conn.commit()
    print("专辑-歌曲数据传输完成！传输任务结束")
    bj_af_cursor.close()
    bj_af_conn.close()

if __name__ == '__main__':
    transfer_task_data_hk_to_bj()