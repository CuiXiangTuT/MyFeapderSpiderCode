"""
@description：
    目的是将香港服务器上抓取到的数据（主要指boomplay）传输至北京服务器上
    
    注意：本程序仅做一次运行，第一次做全量传输，运行时间较长

    控制频率：
"""
from setting import *
import pymysql
import pandas



def transfer_info_data_hk_to_bj():
    """
    将香港服务器上的数据传输至北京服务器上
    """
    # 香港服务器
    hk_conn = pymysql.Connect(
        host=HK_MYSQL_IP,
        port=HK_MYSQL_PORT,
        database=HK_MYSQL_DB,
        user=HK_MYSQL_USER_NAME,
        password=HK_MYSQL_USER_PASS
        )
    hk_cursor = hk_conn.cursor()

    sql_artist_info_data = """
    SELECT gmg_artist_id,gmg_artist_name,crawl_artist_name,boomplay_artist_id,crawl_boomplay_artist_id,boomplay_artist_name,boomplay_artist_certification,batch,boomplay_artist_image,boomplay_artist_info,ranking_current,country_region,artist_favorite_count,artist_share_count,artist_comment_count FROM boomplay_artist_info_batch_data
    """
    hk_cursor.execute(sql_artist_info_data)
    # 抽取歌手信息数据
    artist_info_data = hk_cursor.fetchall()
    df_artist_info_data = pandas.DataFrame(artist_info_data,columns=['gmg_artist_id','gmg_artist_name','crawl_artist_name','boomplay_artist_id','crawl_boomplay_artist_id','boomplay_artist_name','boomplay_artist_certification','batch','boomplay_artist_image','boomplay_artist_info','ranking_current','country_region','artist_favorite_count','artist_share_count','artist_comment_count'])


    sql_album_info_data = """
    SELECT crawl_album_id,album_id,album_name,album_type,album_image,album_track_count,album_info,boomplay_artist_id,album_favorite_count,album_share_count,album_comment_count,batch FROM boomplay_album_info_batch_data
    """
    hk_cursor.execute(sql_album_info_data)
    # 抽取专辑信息数据
    album_info_data = hk_cursor.fetchall()
    df_album_info_data = pandas.DataFrame(album_info_data,columns=['crawl_album_id','album_id','album_name','album_type','album_image','album_track_count','album_info','boomplay_artist_id','album_favorite_count','album_share_count','album_comment_count','batch'])

    sql_track_info_data = """
    SELECT crawl_track_id,track_id,track_name,track_type,track_image,album_id,duration,boomplay_artist_id,boomplay_artist_name,capture_artist_id,capture_artist_name,capture_artist_image,capture_album_id,capture_album_name,capture_album_image,track_favorite_count,track_share_count,track_comment_count,genre,publish_date,lyrics_url,lyrics,batch FROM boomplay_track_info_batch_data
    """
    hk_cursor.execute(sql_track_info_data)
    # 抽取歌曲信息数据
    track_info_data = hk_cursor.fetchall()
    df_track_info_data = pandas.DataFrame(track_info_data,columns=['crawl_track_id','track_id','track_name','track_type','track_image','album_id','duration','boomplay_artist_id','boomplay_artist_name','capture_artist_id','capture_artist_name','capture_artist_image','capture_album_id','capture_album_name','capture_album_image','track_favorite_count','track_share_count','track_comment_count','genre','publish_date','lyrics_url','lyrics','batch'])

    sql_track_views_data = """
    SELECT track_id,views,batch,crawl_frequency FROM boomplay_track_views_batch_data
    """
    hk_cursor.execute(sql_track_views_data)
    # 抽取歌曲播放量
    track_views_data = hk_cursor.fetchall()
    df_track_views_data = pandas.DataFrame(track_views_data,columns=['track_id','views','batch','crawl_frequency'])

    # 抽取榜单信息数据
    sql_chart_data_daily = """
    SELECT `rank`,song_id,song_name,chart_artist_id,chart_artist_name,album_id,album_name,duration,chart_region,crawl_chart_country,batch,chart_site,chart_type,update_frequency,chart_language,chart_segment,chart_release_date,ranking_state_change,chart_name FROM chart_data_daily_boomplay
    """
    hk_cursor.execute(sql_chart_data_daily)
    chart_data_daily = hk_cursor.fetchall()
    df_chart_data_daily = pandas.DataFrame(chart_data_daily,columns=['rank','song_id','song_name','chart_artist_id','chart_artist_name','album_id','album_name','duration','chart_region','crawl_chart_country','batch','chart_site','chart_type','update_frequency','chart_language','chart_segment','chart_release_date','ranking_state_change','chart_name'])

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

    print("开始向服务器传输歌手信息数据")

    # 向北京服务器传输数据
    # 1-传输歌手信息数据
    for i in range(len(df_artist_info_data)):
        gmg_artist_id = df_artist_info_data.iloc[i]['gmg_artist_id']
        gmg_artist_name = df_artist_info_data.iloc[i]['gmg_artist_name']
        crawl_artist_name = df_artist_info_data.iloc[i]['crawl_artist_name']
        boomplay_artist_id = df_artist_info_data.iloc[i]['boomplay_artist_id']
        crawl_boomplay_artist_id = df_artist_info_data.iloc[i]['crawl_boomplay_artist_id']
        boomplay_artist_name = df_artist_info_data.iloc[i]['boomplay_artist_name']
        boomplay_artist_certification = df_artist_info_data.iloc[i]['boomplay_artist_certification']
        batch = df_artist_info_data.iloc[i]['batch']
        boomplay_artist_image = df_artist_info_data.iloc[i]['boomplay_artist_image']
        boomplay_artist_info = df_artist_info_data.iloc[i]['boomplay_artist_info']
        ranking_current = df_artist_info_data.iloc[i]['ranking_current']
        country_region = df_artist_info_data.iloc[i]['country_region']
        artist_favorite_count = df_artist_info_data.iloc[i]['artist_favorite_count']
        artist_share_count = df_artist_info_data.iloc[i]['artist_share_count']
        artist_comment_count = df_artist_info_data.iloc[i]['artist_comment_count']
        bj_artist_info_sql = "INSERT IGNORE INTO boomplay_artist_info_batch_data(gmg_artist_id,gmg_artist_name,crawl_artist_name,boomplay_artist_id,crawl_boomplay_artist_id,boomplay_artist_name,boomplay_artist_certification,batch,boomplay_artist_image,boomplay_artist_info,ranking_current,country_region,artist_favorite_count,artist_share_count,artist_comment_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        bj_af_cursor.execute(bj_artist_info_sql,[gmg_artist_id,gmg_artist_name,crawl_artist_name,boomplay_artist_id,crawl_boomplay_artist_id,boomplay_artist_name,boomplay_artist_certification,batch,boomplay_artist_image,boomplay_artist_info,ranking_current,country_region,artist_favorite_count,artist_share_count,artist_comment_count])
        bj_af_conn.commit()
    
    print("歌手信息数据传输完成，开始传输专辑信息数据")

    # 2-传输专辑信息数据
    for i in range(len(df_album_info_data)):
        crawl_album_id = df_album_info_data.iloc[i]['crawl_album_id']
        album_id = df_album_info_data.iloc[i]['album_id']
        album_name = df_album_info_data.iloc[i]['album_name']
        album_type = df_album_info_data.iloc[i]['album_type']
        album_image = df_album_info_data.iloc[i]['album_image']
        album_track_count = df_album_info_data.iloc[i]['album_track_count']
        album_info = df_album_info_data.iloc[i]['album_info']
        boomplay_artist_id = df_album_info_data.iloc[i]['boomplay_artist_id']
        album_favorite_count = df_album_info_data.iloc[i]['album_favorite_count']
        album_share_count = df_album_info_data.iloc[i]['album_share_count']
        album_comment_count = df_album_info_data.iloc[i]['album_comment_count']
        batch = df_album_info_data.iloc[i]['batch']
        bj_album_info_sql = "INSERT IGNORE INTO boomplay_album_info_batch_data(crawl_album_id,album_id,album_name,album_type,album_image,album_track_count,album_info,boomplay_artist_id,album_favorite_count,album_share_count,album_comment_count,batch) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        bj_af_cursor.execute(bj_album_info_sql,[crawl_album_id,album_id,album_name,album_type,album_image,album_track_count,album_info,boomplay_artist_id,album_favorite_count,album_share_count,album_comment_count,batch])
        bj_af_conn.commit()
    
    print("专辑信息数据传输完成，开始传输歌曲信息数据")
    
    # 3-传输歌曲信息数据
    for i in range(len(df_track_info_data)):
        crawl_track_id = df_track_info_data.iloc[i]['crawl_track_id']
        track_id = df_track_info_data.iloc[i]['track_id']
        track_name = df_track_info_data.iloc[i]['track_name']
        track_type = df_track_info_data.iloc[i]['track_type']
        track_image = df_track_info_data.iloc[i]['track_image']
        album_id = df_track_info_data.iloc[i]['album_id']
        duration = df_track_info_data.iloc[i]['duration']
        boomplay_artist_id = df_track_info_data.iloc[i]['boomplay_artist_id']
        boomplay_artist_name = df_track_info_data.iloc[i]['boomplay_artist_name']
        capture_artist_id = df_track_info_data.iloc[i]['capture_artist_id']
        capture_artist_name = df_track_info_data.iloc[i]['capture_artist_name']
        capture_artist_image = df_track_info_data.iloc[i]['capture_artist_image']
        capture_album_id = df_track_info_data.iloc[i]['capture_album_id']
        capture_album_name = df_track_info_data.iloc[i]['capture_album_name']
        capture_album_image = df_track_info_data.iloc[i]['capture_album_image']
        track_favorite_count = df_track_info_data.iloc[i]['track_favorite_count']
        track_share_count = df_track_info_data.iloc[i]['track_share_count']
        track_comment_count = df_track_info_data.iloc[i]['track_comment_count']
        genre = df_track_info_data.iloc[i]['genre']
        publish_date = df_track_info_data.iloc[i]['publish_date']
        lyrics_url = df_track_info_data.iloc[i]['lyrics_url']
        lyrics = df_track_info_data.iloc[i]['lyrics']
        batch = df_track_info_data.iloc[i]['batch']
        bj_track_info_sql = "INSERT IGNORE INTO boomplay_track_info_batch_data(crawl_track_id,track_id,track_name,track_type,track_image,album_id,duration,boomplay_artist_id,boomplay_artist_name,capture_artist_id,capture_artist_name,capture_artist_image,capture_album_id,capture_album_name,capture_album_image,track_favorite_count,track_share_count,track_comment_count,genre,publish_date,lyrics_url,lyrics,batch) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        bj_af_cursor.execute(bj_track_info_sql,[crawl_track_id,track_id,track_name,track_type,track_image,album_id,duration,boomplay_artist_id,boomplay_artist_name,capture_artist_id,capture_artist_name,capture_artist_image,capture_album_id,capture_album_name,capture_album_image,track_favorite_count,track_share_count,track_comment_count,genre,publish_date,lyrics_url,lyrics,batch])
        bj_af_conn.commit()
    
    print("歌曲信息数据传输完成，开始传输歌曲播放量数据")

    # 4-传输歌曲播放量
    for i in range(len(df_track_views_data)):
        track_id = df_track_views_data.iloc[i]['track_id']
        views = df_track_views_data.iloc[i]['views']
        batch = df_track_views_data.iloc[i]['batch']
        crawl_frequency = df_track_views_data.iloc[i]['crawl_frequency']
        bj_track_views_sql = "INSERT IGNORE INTO boomplay_track_views_batch_data(track_id,views,batch,crawl_frequency) VALUES(%s,%s,%s,%s)"
        bj_af_cursor.execute(bj_track_views_sql,[track_id,views,batch,crawl_frequency])
        bj_af_conn.commit()
    
    print("歌曲播放量数据传输完成，开始传输榜单数据")

    for i in range(len(df_chart_data_daily)):
        rank = df_chart_data_daily.iloc[i]['rank']
        song_id = df_chart_data_daily.iloc[i]['song_id']
        song_name = df_chart_data_daily.iloc[i]['song_name']
        chart_artist_id = df_chart_data_daily.iloc[i]['chart_artist_id']
        chart_artist_name = df_chart_data_daily.iloc[i]['chart_artist_name']
        album_id = df_chart_data_daily.iloc[i]['album_id']
        album_name = df_chart_data_daily.iloc[i]['album_name']
        duration = df_chart_data_daily.iloc[i]['duration']
        chart_region = df_chart_data_daily.iloc[i]['chart_region']
        crawl_chart_country = df_chart_data_daily.iloc[i]['crawl_chart_country']
        batch = df_chart_data_daily.iloc[i]['batch']
        chart_site = df_chart_data_daily.iloc[i]['chart_site']
        chart_type = df_chart_data_daily.iloc[i]['chart_type']
        update_frequency = df_chart_data_daily.iloc[i]['update_frequency']
        chart_language = df_chart_data_daily.iloc[i]['chart_language']
        chart_segment = df_chart_data_daily.iloc[i]['chart_segment']
        chart_release_date = df_chart_data_daily.iloc[i]['chart_release_date']
        ranking_state_change = df_chart_data_daily.iloc[i]['ranking_state_change']
        chart_name = df_chart_data_daily.iloc[i]['chart_name']
        bj_chart_data_daily_sql = "INSERT INTO chart_data_daily_boomplay(`rank`,song_id,song_name,chart_artist_id,chart_artist_name,album_id,album_name,duration,chart_region,crawl_chart_country,batch,chart_site,chart_type,update_frequency,chart_language,chart_segment,chart_release_date,ranking_state_change,chart_name,note) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        bj_af_cursor.execute(bj_chart_data_daily_sql,[rank,song_id,song_name,chart_artist_id,chart_artist_name,album_id,album_name,duration,chart_region,crawl_chart_country,batch,chart_site,chart_type,update_frequency,chart_language,chart_segment,chart_release_date,ranking_state_change,chart_name,'AF'])
        bj_af_conn.commit()


    bj_af_cursor.close()
    bj_af_conn.close()


if __name__ == '__main__':
    transfer_info_data_hk_to_bj()