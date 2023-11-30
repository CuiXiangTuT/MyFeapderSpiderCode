from setting import *
import pymysql
import datetime

"""
@description：
    补录boomplay榜单数据至chart_data_daily
    逻辑如下：
        1.获取当前日期下chart_data_daily表中，chart_site='boomplay'的数据
        2.从music_data的chart_data_daily_boomplay_af中获取当前日期下的榜单数据，理论结果为400
        3.如果能从music_data的chart_data_daily_boomplay_af中中获取到相关数据，那么将【当前日期】下的chart_data_daily关于boomplay数据清除
          如果不能，则保留当前榜单内容
"""

def inspection_boomplay_chart_data():
    music_data_hk_conn = pymysql.Connect(
        host=BJ_MYSQL_IP,
        port=BJ_MYSQL_PORT,
        database=BJ_MYSQL_DB_HK,
        user=BJ_MYSQL_USER_NAME,
        password=BJ_MYSQL_USER_PASS
        )
    music_data_hk_cursor = music_data_hk_conn.cursor()

    # 从music_data_hk中获取当前日期下的榜单数据
    sql_music_data_hk = 'SELECT COUNT(*) FROM chart_data_daily_boomplay WHERE batch=CURRENT_DATE'
    music_data_hk_cursor.execute(sql_music_data_hk)
    result = music_data_hk_cursor.fetchall()[0][0]

    
    # 核验每个地区查询数据是否为100： ghana,kenya,tanzania,nigeria
    sql_chart_ghana = 'SELECT COUNT(*) FROM chart_data_daily_boomplay WHERE batch=CURRENT_DATE AND crawl_chart_country="ghana"'
    music_data_hk_cursor.execute(sql_chart_ghana)
    result_ghana = music_data_hk_cursor.fetchall()[0][0]
    sql_chart_kenya = 'SELECT COUNT(*) FROM chart_data_daily_boomplay WHERE batch=CURRENT_DATE AND crawl_chart_country="kenya"'
    music_data_hk_cursor.execute(sql_chart_kenya)
    result_kenya = music_data_hk_cursor.fetchall()[0][0]
    sql_chart_tanzania = 'SELECT COUNT(*) FROM chart_data_daily_boomplay WHERE batch=CURRENT_DATE AND crawl_chart_country="tanzania"'
    music_data_hk_cursor.execute(sql_chart_tanzania)
    result_tanzania = music_data_hk_cursor.fetchall()[0][0]
    sql_chart_nigeria = 'SELECT COUNT(*) FROM chart_data_daily_boomplay WHERE batch=CURRENT_DATE AND crawl_chart_country="nigeria"'
    music_data_hk_cursor.execute(sql_chart_nigeria)
    result_nigeria = music_data_hk_cursor.fetchall()[0][0]


    # 验证四个地区当天日期下的榜单条目数均为100
    if str(result_ghana)==str(result_kenya)==str(result_tanzania)==str(result_nigeria)=='100':
        # 判断数据库music_data下chart_data_daily表中是否含有当前日期的boomplay的相关数据
        sql_chart_data_daily = 'SELECT COUNT(*) FROM music_data.chart_data_daily WHERE chart_site="boomplay" AND batch=CURRENT_DATE'
        music_data_hk_cursor.execute(sql_chart_data_daily)
        result_chart_data_daily = music_data_hk_cursor.fetchall()[0][0]

        if str(result_chart_data_daily)=='400':
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today+"：今日榜单数据400条，无需操作")
            pass
        else:
            if str(result_chart_data_daily) != '0':
                sql_delete_data = 'DELETE FROM music_data.chart_data_daily WHERE chart_site="boomplay" AND batch=CURRENT_DATE;'
                music_data_hk_cursor.execute(sql_delete_data)
                music_data_hk_conn.commit()
                print("删除当前music_data库中的数据")

            # 当前日期下，非洲抓到相关榜单数据
            sql_insert_data = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
                FROM music_data.chart_data_daily_boomplay_af
                WHERE  batch = CURRENT_DATE;
            '''
            music_data_hk_cursor.execute(sql_insert_data)
            music_data_hk_conn.commit()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today+"：非洲榜单上传数据成功")
    
    elif max([result_ghana,result_kenya,result_tanzania,result_nigeria])==100:
        is_flag_ghana=is_flag_kenya=is_flag_tanzania=is_flag_nigeria=True

        if result_ghana==100:
            # 先删除榜单中本已存在的当前日期下的加纳数据
            sql_delete_data_ghana = 'DELETE FROM music_data.chart_data_daily WHERE crawl_chart_country="ghana" AND batch = CURRENT_DATE'
            music_data_hk_cursor.execute(sql_delete_data_ghana)
            music_data_hk_conn.commit()
            print("删除music_data中已存在的ghana数据")
            # 将加纳数据导入至热榜榜单表
            sql_insert_data_ghana = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
                FROM music_data.chart_data_daily_boomplay_af
                WHERE crawl_chart_country="ghana" AND batch = CURRENT_DATE;
            '''
            music_data_hk_cursor.execute(sql_insert_data_ghana)
            music_data_hk_conn.commit()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today+"：加纳榜单上传数据成功")
            is_flag_ghana = False

        if result_kenya==100:
            # 先删除榜单中本已存在的当前日期下的肯尼亚数据
            sql_delete_data_kenya = 'DELETE FROM music_data.chart_data_daily WHERE crawl_chart_country="kenya" AND batch = CURRENT_DATE'
            music_data_hk_cursor.execute(sql_delete_data_kenya)
            music_data_hk_conn.commit()
            print("删除music_data中已存在的kenya数据")
            # 将肯尼亚数据导入至热榜榜单表
            sql_insert_data_kenya = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
                FROM music_data.chart_data_daily_boomplay_af
                WHERE crawl_chart_country="kenya" AND batch = CURRENT_DATE;
            '''
            music_data_hk_cursor.execute(sql_insert_data_kenya)
            music_data_hk_conn.commit()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today+"：肯尼亚榜单上传数据成功")
            is_flag_kenya = False

        if result_tanzania==100:
            # 先删除榜单中本已存在的当前日期下的坦桑尼亚数据
            sql_delete_data_tanzania = 'DELETE FROM music_data.chart_data_daily WHERE crawl_chart_country="tanzania" AND batch = CURRENT_DATE'
            music_data_hk_cursor.execute(sql_delete_data_tanzania)
            music_data_hk_conn.commit()
            print("删除music_data中已存在的tanzania数据")
            # 将坦桑尼亚数据导入至热榜榜单表
            sql_insert_data_tanzania = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
                FROM music_data.chart_data_daily_boomplay_af
                WHERE crawl_chart_country="tanzania" AND batch = CURRENT_DATE;
            '''
            music_data_hk_cursor.execute(sql_insert_data_tanzania)
            music_data_hk_conn.commit()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today+"：坦桑尼亚榜单上传数据成功")
            is_flag_tanzania = False
        if result_nigeria==100:
            # 先删除榜单中本已存在的当前日期下的尼日利亚数据
            sql_delete_data_nigeria = 'DELETE FROM music_data.chart_data_daily WHERE crawl_chart_country="nigeria" AND batch = CURRENT_DATE'
            music_data_hk_cursor.execute(sql_delete_data_nigeria)
            music_data_hk_conn.commit()
            print("删除music_data中已存在的nigeria数据")
            # 将尼日利亚数据导入至热榜榜单表
            sql_insert_data_nigeria = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
                FROM music_data.chart_data_daily_boomplay_af
                WHERE crawl_chart_country="nigeria" AND batch = CURRENT_DATE;
            '''
            music_data_hk_cursor.execute(sql_insert_data_nigeria)
            music_data_hk_conn.commit()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today+"：尼日利亚榜单上传数据成功")
            is_flag_nigeria = False

        if is_flag_ghana:
            # 将不足100的加纳数据与music_data中的chart_data_daily当日数据进行合并汇总
            sql_insert_data_ghana_1 = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )	
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay_af
            WHERE crawl_chart_country="ghana" AND batch = CURRENT_DATE AND song_id NOT IN (
            SELECT song_id FROM music_data.chart_data_daily WHERE crawl_chart_country="ghana" AND batch = CURRENT_DATE AND chart_site='boomplay'
            );
            '''
            music_data_hk_cursor.execute(sql_insert_data_ghana_1)
            music_data_hk_conn.commit()
            print('将不足100的加纳数据与music_data中的chart_data_daily当日数据进行合并汇总')
        if is_flag_kenya:
            # 将不足100的肯尼亚数据与music_data中的chart_data_daily当日数据进行合并汇总
            sql_insert_data_kenya_1 = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )	
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay_af
            WHERE crawl_chart_country="kenya" AND batch = CURRENT_DATE AND song_id NOT IN (
            SELECT song_id FROM music_data.chart_data_daily WHERE crawl_chart_country="kenya" AND batch = CURRENT_DATE AND chart_site='boomplay'
            );
            '''
            music_data_hk_cursor.execute(sql_insert_data_kenya_1)
            music_data_hk_conn.commit()
            print('将不足100的肯尼亚数据与music_data中的chart_data_daily当日数据进行合并汇总')
        if is_flag_tanzania:
            # 将不足100的坦桑尼亚数据与music_data中的chart_data_daily当日数据进行合并汇总
            sql_insert_data_tanzania_1 = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )	
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay_af
            WHERE crawl_chart_country="tanzania" AND batch = CURRENT_DATE AND song_id NOT IN (
            SELECT song_id FROM music_data.chart_data_daily WHERE crawl_chart_country="tanzania" AND batch = CURRENT_DATE AND chart_site='boomplay'
            );
            '''
            music_data_hk_cursor.execute(sql_insert_data_tanzania_1)
            music_data_hk_conn.commit()
            print('将不足100的坦桑尼亚数据与music_data中的chart_data_daily当日数据进行合并汇总')
        if is_flag_nigeria:
            # 将不足100的尼日利亚数据与music_data中的chart_data_daily当日数据进行合并汇总
            sql_insert_data_nigeria_1 = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )	
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay_af
            WHERE crawl_chart_country="nigeria" AND batch = CURRENT_DATE AND song_id NOT IN (
            SELECT song_id FROM music_data.chart_data_daily WHERE crawl_chart_country="nigeria" AND batch = CURRENT_DATE AND chart_site='boomplay'
            );
            '''
            music_data_hk_cursor.execute(sql_insert_data_nigeria_1)
            music_data_hk_conn.commit()
            print('将不足100的尼日利亚数据与music_data中的chart_data_daily当日数据进行合并汇总')

    elif 0<max([result_ghana,result_kenya,result_tanzania,result_nigeria])<100:
        # 将抓取到的四个地区的数据与music_data中的chart_data_daily当日数据进行合并汇总
        sql_insert_data_ghana_1 = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )	
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay_af
            WHERE crawl_chart_country="ghana" AND batch = CURRENT_DATE AND song_id NOT IN (
            SELECT song_id FROM music_data.chart_data_daily WHERE crawl_chart_country="ghana" AND batch = CURRENT_DATE AND chart_site='boomplay'
            );
            '''
        music_data_hk_cursor.execute(sql_insert_data_ghana_1)
        music_data_hk_conn.commit()
        print("补充ghana数据")
        sql_insert_data_kenya_1 = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )	
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay_af
            WHERE crawl_chart_country="kenya" AND batch = CURRENT_DATE AND song_id NOT IN (
            SELECT song_id FROM music_data.chart_data_daily WHERE crawl_chart_country="kenya" AND batch = CURRENT_DATE AND chart_site='boomplay'
            );
            '''
        music_data_hk_cursor.execute(sql_insert_data_kenya_1)
        music_data_hk_conn.commit()
        print("补充kenya数据")
        sql_insert_data_tanzania_1 = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )	
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay_af
            WHERE crawl_chart_country="tanzania" AND batch = CURRENT_DATE AND song_id NOT IN (
            SELECT song_id FROM music_data.chart_data_daily WHERE crawl_chart_country="tanzania" AND batch = CURRENT_DATE AND chart_site='boomplay'
            );
            '''
        music_data_hk_cursor.execute(sql_insert_data_tanzania_1)
        music_data_hk_conn.commit()
        print("补充tanzania数据")
        sql_insert_data_nigeria_1 = '''
            INSERT INTO music_data.chart_data_daily(
                table_No
                ,`rank`
                ,song_id
                ,song_name
                ,chart_artist_id
                ,chart_artist_name
                ,album_id
                ,album_name
                ,duration
                ,views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,sub_chart_type
                ,update_frequency
                ,chart_language
                ,chart_segment
                ,chart_release_date
                ,chart_update_date
                ,chart_unique_name
                )	
                SELECT  
                NULL AS table_No
                ,`rank`
                ,song_id
                ,LOWER(song_name) AS song_name
                ,chart_artist_id
                ,LOWER(chart_artist_name) AS chart_artist_name
                ,album_id
                ,LOWER(album_name) AS album_name
                ,duration
                ,'0' AS views
                ,chart_region
                ,crawl_chart_country
                ,batch
                ,chart_site
                ,chart_type
                ,'-' AS sub_chart_type
                ,'weekly' update_frequency
                ,chart_language
                ,'100' chart_segment
                ,'-' AS chart_release_date
                ,'' AS chart_update_date
                ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay_af
            WHERE crawl_chart_country="nigeria" AND batch = CURRENT_DATE AND song_id NOT IN (
            SELECT song_id FROM music_data.chart_data_daily WHERE crawl_chart_country="nigeria" AND batch = CURRENT_DATE AND chart_site='boomplay'
            );
            '''
        music_data_hk_cursor.execute(sql_insert_data_nigeria_1)
        music_data_hk_conn.commit()
        print("补充nigeria数据")

    else:
        # 当前日期下，非洲断开链接，未进行抓取数据，使用北京抓取的数据做补充
        # 判断数据库music_data下chart_data_daily表中是否含有当前日期的boomplay的相关数据
        sql_chart_data_daily = 'SELECT COUNT(*) FROM music_data.chart_data_daily WHERE chart_site="boomplay" AND batch=CURRENT_DATE;'
        music_data_hk_cursor.execute(sql_chart_data_daily)
        result_chart_data_daily = music_data_hk_cursor.fetchall()[0][0]

        if int(result_chart_data_daily)>0:
            # 当前日期下，已存在boomplay榜单数据，无需操作
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today+"：当前日期下存在数据，无需操作")
        else:
            # 当前日期下，不存在boomplay榜单数据，那么使用music_data中的数据做补充
            sql_music_data_chart = '''
            INSERT INTO music_data.chart_data_daily(
            table_No
            ,`rank`
            ,song_id
            ,song_name
            ,chart_artist_id
            ,chart_artist_name
            ,album_id
            ,album_name
            ,duration
            ,views
            ,chart_region
            ,crawl_chart_country
            ,batch
            ,chart_site
            ,chart_type
            ,sub_chart_type
            ,update_frequency
            ,chart_language
            ,chart_segment
            ,chart_release_date
            ,chart_update_date
            ,chart_unique_name
            )
            SELECT  
            NULL AS table_No
            ,`rank`
            ,song_id
            ,LOWER(song_name) AS song_name
            ,chart_artist_id
            ,LOWER(chart_artist_name) AS chart_artist_name
            ,album_id
            ,LOWER(album_name) AS album_name
            ,duration
            ,'0' AS views
            ,chart_region
            ,crawl_chart_country
            ,batch
            ,chart_site
            ,chart_type
            ,'-' AS sub_chart_type
            ,'weekly' update_frequency
            ,chart_language
            ,'100' chart_segment
            ,'-' AS chart_release_date
            ,'' AS chart_update_date
            ,'' AS chart_unique_name
            FROM music_data.chart_data_daily_boomplay
            WHERE  batch = CURRENT_DATE;
            '''
            music_data_hk_cursor.execute(sql_music_data_chart)
            music_data_hk_conn.commit()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today+"：北京榜单上传数据成功")


if __name__ == '__main__':
    inspection_boomplay_chart_data()

