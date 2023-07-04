"""
@description：
    本程序目的是将boomplay_isrc_track的信息更新到boomplay_track_info_batch_data
"""
from setting import *
import pymysql

def update_track_info_isrc():
    """
    更新boomplay_track_info_batch_data的ISRC相关信息
    """
    # 此处为测试，使用的为本地服务器
    bj_af_conn = pymysql.Connect(
        host=LOCAL_AF_MYSQL_IP,
        port=LOCAL_AF_MYSQL_PORT,
        database=LOCAL_AF_MYSQL_DB,
        user=LOCAL_AF_MYSQL_USER_NAME,
        password=LOCAL_AF_MYSQL_USER_PASS
        )
    bj_af_cursor = bj_af_conn.cursor()

    print("开始更新歌曲ISRC信息")
    sql_update_track_info_isrc = """
    UPDATE boomplay_track_info_batch_data a
    INNER JOIN boomplay_isrc_track b
    ON a.crawl_track_id = b.track_id
    SET a.`ISRC`=b.`ISRC`,a.`isrc_track_name`=b.`track_name`,a.`isrc_artist_name`=b.`artist_name`,a.`isrc_genre`=b.`Genre`,a.`CP`=b.`CP`,a.`Date Created`=b.`Date Created`
    """
    bj_af_cursor.execute(sql_update_track_info_isrc)
    bj_af_conn.commit()
    print("歌曲ISRC信息更新完成")

    bj_af_cursor.close()
    bj_af_conn.close()

if __name__ == '__main__':
    update_track_info_isrc()