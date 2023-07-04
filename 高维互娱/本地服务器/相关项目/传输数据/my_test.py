"""
@description：
    目的仅仅做一些测试使用，可删
"""
from setting import *
import pymysql
import pandas
import datetime


def compare_db_data_func():
    """
    将两个数据库之间的数据进行比较，仅抽取数据库数据不一致的数据
    """
    # 此处为测试，使用的为本地服务器
    bj_af_conn = pymysql.Connect(
        host=HK_MYSQL_IP,
        port=HK_MYSQL_PORT,
        database=HK_MYSQL_DB,
        user=HK_MYSQL_USER_NAME,
        password=HK_MYSQL_USER_PASS
        )
    bj_af_cursor = bj_af_conn.cursor()
    sql_artist_info_data = """
    SELECT * FROM boomplay_artist_info_batch_data
    """
    bj_af_cursor.execute(sql_artist_info_data)
    # 抽取出歌手信息数据
    artist_info_data = bj_af_cursor.fetchall()
    # print(artist_info_data)
    df_artist_info_data = pandas.DataFrame(artist_info_data,columns=['id','gmg_artist_id','gmg_artist_name','boomplay_artist_name','crawl_boomplay_artist_id','boomplay_artist_id','crawl_artist_name','boomplay_artist_certification','batch','boomplay_artist_image','boomplay_artist_info','ranking_current','ranking_alltime','country_region','artist_favorite_count','artist_share_count','artist_comment_count','gtime','note'])

def sort_list():
    l1 = [1,5,4,2,3]
    l2 = ['g','e','d','e','a']

    li=list(zip(l1,l2))
    sort_li = sorted(li,key=lambda sl: (sl[1],sl[0]))
    print(sort_li)


def generate_time():
    """
    生成时间
    """
    # 当前时间
    current_date = datetime.datetime.now()
    prev_date = current_date + datetime.timedelta(days=-1)
    current_batch = current_date.strftime("%Y-%m-%d")
    prev_batch = prev_date.strftime("%Y-%m-%d")
    print("current_batch:",current_batch)
    print("prev_batch:",prev_batch)


def for_func():
    l = []
    for i in range(len(l)):
        print(i)
        print(l[i])


def str_test():
    s = ""
    print(s.lower())
    print("---")

if __name__ == '__main__':
    str_test()

