"""
将gmg_artist_info表中的相关平台数据
经过处理之后放入至各对应的任务表中
"""
from setting import *
import pymysql

# 连接本地数据库
local_conn = pymysql.Connect(
    host=LOCAL_MYSQL_IP,
    port=LOCAL_MYSQL_PORT,
    user=LOCAL_MYSQL_USER_NAME,
    password=LOCAL_MYSQL_USER_PASS,
    db='gmg_data_assets'
)
local_cursor = local_conn.cursor()

def instagram_task_func(local_conn,local_cursor):
    """
    抽出Instagram任务数据
    """
    sql_ins_task = """
    INSERT IGNORE INTO instagram_artist_info_batch_task(gmg_artist_id,gmg_artist_name,artist_url)
    SELECT gmg_artist_id,gmg_artist_name,instagram_link
    FROM gmg_data_assets.gmg_artist_follows
    WHERE instagram_link IS NOT NULL AND instagram_link != '-';
    """
    try:
        local_cursor.execute(sql_ins_task)
        local_conn.commit()
        print("Instagram 数据提交成功")
    except:
        local_conn.rollback()
        print("Instagram 数据回滚")
    finally:
        local_cursor.close()
        local_conn.close()

def twitter_task_func(local_conn,local_cursor):
    """
    抽出Twitter任务数据
    """
    sql_twitter_task = """
    INSERT IGNORE INTO twitter_artist_info_batch_task(gmg_artist_id,gmg_artist_name,artist_url)
    SELECT gmg_artist_id,gmg_artist_name,twitter_link
    FROM gmg_data_assets.gmg_artist_follows
    WHERE twitter_link IS NOT NULL AND twitter_link != '-';
    """
    try:
        local_cursor.execute(sql_twitter_task)
        local_conn.commit()
        print("Twitter 数据提交成功")
    except:
        local_conn.rollback()
        print("Twitter 数据回滚")
    finally:
        local_cursor.close()
        local_conn.close()

def tiktok_task_func(local_conn,local_cursor):
    """
    抽出Tik Tok任务数据
    """
    sql_tiktok_task = """
    INSERT IGNORE INTO tiktok_artist_info_batch_task(gmg_artist_id,gmg_artist_name,tiktok_url)
    SELECT gmg_artist_id,gmg_artist_name,tiktok_link
    FROM gmg_data_assets.gmg_artist_follows
    WHERE tiktok_link IS NOT NULL AND tiktok_link != '-';
    """
    try:
        local_cursor.execute(sql_tiktok_task)
        local_conn.commit()
        print("Tik Tok 数据提交成功")
    except:
        local_conn.rollback()
        print("Tik Tok 数据回滚")
    finally:
        local_cursor.close()
        local_conn.close()


def youtube_task_func(local_conn,local_cursor):
    """
    抽出YouTube任务数据
    """
    sql_youtube_task = """
    INSERT IGNORE INTO youtube_artist_info_batch_task(gmg_artist_id,gmg_artist_name,artist_url)
    SELECT gmg_artist_id,gmg_artist_name,youtube_link
    FROM gmg_data_assets.gmg_artist_follows
    WHERE youtube_link IS NOT NULL AND youtube_link != '-';
    """
    try:
        local_cursor.execute(sql_youtube_task)
        local_conn.commit()
        print("Tik Tok 数据提交成功")
    except:
        local_conn.rollback()
        print("Tik Tok 数据回滚")
    finally:
        local_cursor.close()
        local_conn.close()


if __name__ == '__main__':
    tiktok_task_func(local_conn,local_cursor)