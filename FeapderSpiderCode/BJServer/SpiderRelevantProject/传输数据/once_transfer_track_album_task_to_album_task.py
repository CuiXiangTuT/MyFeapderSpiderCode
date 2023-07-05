"""
将歌曲库中的capture_album_id放入至专辑任务表
"""
import pymysql
from setting import *

def transfer_task_to_album():
    bj_conn = pymysql.Connect(
        host=BJ_MYSQL_IP,
        port=BJ_MYSQL_PORT,
        user=BJ_MYSQL_USER_NAME,
        password=BJ_MYSQL_USER_PASS,
        db=BJ_MYSQL_DB
    )
    bj_cursor = bj_conn.cursor()
    sql_album_task = '''
    INSERT IGNORE INTO boomplay_album_info_batch_task(album_id)
    SELECT capture_album_id FROM boomplay_track_info_batch_data
    WHERE capture_album_id NOT IN (
        SELECT DISTINCT album_id FROM boomplay_album_info_batch_task
    );
    '''
    try:
        bj_cursor.execute(sql_album_task)
        bj_conn.commit()
    except:
        print('数据回滚')
        bj_conn.rollback()
    finally:
        bj_cursor.close()
        bj_conn.close()

if __name__ == '__main__':
    transfer_task_to_album()