"""
@description：
    主要目的是：在香港（非洲）服务器传输数据至北京服务器之后，根据数据表中的数据存在情况，
               将北京服务器任务表的状态修改为1
"""
import pymysql
from setting import *

def update_task_data_bj():
    """
    更新任务状态为1
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

    # 1-更新歌手任务状态为1
    sql_update_artist_info_task = """
    UPDATE boomplay_artist_info_batch_task
    SET state = 1
    WHERE boomplay_artist_id IN (
        SELECT crawl_boomplay_artist_id FROM boomplay_artist_info_batch_data
    )
    """
    bj_af_cursor.execute(sql_update_artist_info_task)
    bj_af_conn.commit()

    print("歌手任务表状态更新完成")

    # 2-更新专辑任务状态为1
    sql_update_album_info_task = """
    UPDATE boomplay_album_info_batch_task
    SET state = 1
    WHERE album_id IN (
        SELECT crawl_album_id FROM boomplay_album_info_batch_data
    )
    """
    bj_af_cursor.execute(sql_update_album_info_task)
    bj_af_conn.commit()

    print("专辑任务表状态更新完成")

    # 3-更新歌曲任务状态为1
    sql_update_track_info_task_state = """
    UPDATE boomplay_track_info_batch_task
    SET state = 1
    WHERE track_id IN (
        SELECT crawl_track_id FROM boomplay_track_info_batch_data
    )
    """
    bj_af_cursor.execute(sql_update_track_info_task_state)
    bj_af_conn.commit()

    print("歌曲任务表（state）状态更新完成")

    # 4-更新歌曲播放量任务状态为1
    sql_update_track_info_task_views_state = """
    UPDATE boomplay_track_info_batch_task
    SET views_state = 1
    WHERE track_id IN (
        SELECT track_id FROM boomplay_track_views_batch_data
    )
    """
    bj_af_cursor.execute(sql_update_track_info_task_views_state)
    bj_af_conn.commit()

    print("歌曲任务表（views_state）状态更新完成")

    bj_af_cursor.close()
    bj_af_conn.close()

if __name__ == '__main__':
    update_task_data_bj()
