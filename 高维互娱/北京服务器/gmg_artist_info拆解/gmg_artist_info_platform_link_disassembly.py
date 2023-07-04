"""
拆解各平台链接进行分别入库
平台包括：Instagram、Twitter、YouTube、Facebook、Wikipedia、Tik Tok
"""
from setting import *
import pymysql
import pandas

def deal_gmg_artist_info_instagram_func(bj_conn,local_conn):
    sql_instagram_info = '''
    SELECT gmg_artist_id,gmg_artist_name,instagram_link FROM gmg_artist_follows
    WHERE instagram_link IS NOT NULL AND instagram_link != '-';
    '''
    bj_cursor = bj_conn.cursor()
    bj_cursor.execute(sql_instagram_info)
    instagram_info_data = bj_cursor.fetchall()
    df_instagram_info = pandas.DataFrame(instagram_info_data,columns=['gmg_artist_id','gmg_artist_name','instagram_link'])
    bj_cursor.close()
    bj_conn.close()
    df_instagram_info['instagram_link_split'] = df_instagram_info['instagram_link'].map(lambda x:x.split(';')[0])
    df_instagram_info['artist_id'] = df_instagram_info['instagram_link_split'].map(lambda x:x.split('.com')[1].split('/')[1])
    print(df_instagram_info)
    sql_insert_data = 'INSERT INTO gmg_artist_info_instagram(gmg_artist_id,gmg_artist_name,instagram_link,instagram_link_split,artist_id) VALUES({},{},{},{},{})'
    local_cursor = local_conn.cursor()
    try:
        df_instagram_info.to_sql(name="gmg_artist_info_instagram",con=local_conn,if_exists='replace')
        print("数据插入成功")
    except:
        local_conn.rollback()
        print("数据回滚")
    finally:
        local_conn.close()
        


    pass

def deal_gmg_artist_info_twitter_func():
    pass

def deal_gmg_artist_info_youtube_func():
    pass

def deal_gmg_artist_info_facebook_func():
    pass

def deal_gmg_artist_info_wikipedia_func():
    pass

def deal_gmg_artist_info_tiktok_func():
    pass


if __name__ == '__main__':
    bj_conn = pymysql.Connect(
        host=BJ_MYSQL_IP,
        port=BJ_MYSQL_PORT,
        user=BJ_MYSQL_USER_NAME,
        password=BJ_MYSQL_USER_PASS,
        db=BJ_MYSQL_DB
    )
    local_conn = pymysql.Connect(
        host=LOCAL_MYSQL_IP,
        port=LOCAL_MYSQL_PORT,
        user=LOCAL_MYSQL_USER_NAME,
        password=LOCAL_MYSQL_USER_PASS,
        db=LOCAL_MYSQL_DB
    )
    deal_gmg_artist_info_instagram_func(bj_conn,local_conn)
    pass
