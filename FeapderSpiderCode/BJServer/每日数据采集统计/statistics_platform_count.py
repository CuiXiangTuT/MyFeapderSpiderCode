"""
统计各平台每日数量
各平台：Twitter、YouTube、Tik Tok、Instagram
"""
import pymysql
from setting import *

def update_count_func(bj_conn,bj_cursor):
    
    sql_youtube = "UPDATE work_status.chart_daily_status(tiktok_listeners) a INNER JOIN (SELECT batch,COUNT(*) FROM music_data.tiktok_artist_info_batch_data WHERE batch={}) b ON a.batch=b.batch SET a.tiktok_listeners = b.c;".format()
    bj_cursor.execute(sql_youtube)

    sql_tiktok = """
    UPDATE work_status.chart_daily_status a
    INNER JOIN 
    (SELECT batch,COUNT(*) c
    FROM tiktok_artist_info_batch_data
    GROUP BY batch
    ORDER BY batch DESC) b
    ON a.batch=b.batch
    SET a.tiktok_listeners = b.c;
    """
    bj_cursor.execute(sql_tiktok)

    sql_twitter = """
    UPDATE work_status.chart_daily_status a
    INNER JOIN 
    (SELECT batch,COUNT(*) c
    FROM music_data.artist_info_batch_data 
    WHERE artist_site='twitter'
    GROUP BY batch
    ORDER BY batch DESC) b
    ON a.batch=b.batch
    SET a.twitter_listeners = b.c;
    """
    bj_cursor.execute(sql_twitter)

    sql_ins = """
    UPDATE work_status.chart_daily_status a
    INNER JOIN 
    (SELECT batch,COUNT(*) c
    FROM artist_info_batch_data 
    WHERE artist_site='instagram'
    GROUP BY batch
    ORDER BY batch DESC) b
    ON a.batch=b.batch
    SET a.instagram_listeners = b.c;
    """
    try:
        bj_cursor.execute(sql_ins)
        bj_conn.commit()
        print("数据更新完成")
    except:
        print("数据回滚")
        bj_cursor.rollback()
    finally:
        bj_cursor.close()
        bj_conn.close()


if __name__ == '__main__':

    # 连接北京服务器
    bj_conn = pymysql.Connect(
        host=BJ_MYSQL_IP,
        port=BJ_MYSQL_PORT,
        user=BJ_MYSQL_USER_NAME,
        password=BJ_MYSQL_USER_PASS,
        db=BJ_MYSQL_DB
    )
    bj_cursor = bj_conn.cursor()

    update_count_func(bj_conn,bj_cursor)

    


