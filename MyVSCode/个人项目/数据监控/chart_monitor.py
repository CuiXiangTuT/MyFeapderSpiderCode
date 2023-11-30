# -*- coding: utf-8 -*-
"""
Created on 2022-06-09 11:10:40
---------
@summary:
---------
@author: supdev
"""

import feapder
from feapder.utils.email_sender import EmailSender
from setting import BJ_MYSQL_NODE
import re
from feapder.utils import tools
from feapder.utils.log import log
from feapder.db.mysqldb import MysqlDB
# import time
import pandas as pd


class MonitorChartAndArtist(feapder.Spider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        LOG_LEVEL="DEBUG",
        SPIDER_THREAD_COUNT=1,
        # MYSQL_IP="122.115.36.92",
        # MYSQL_PORT=3306,
        # MYSQL_DB="music_data",
        # MYSQL_USER_NAME="crawler",
        # MYSQL_USER_PASS="crawler.mysql",
    )
    db = MysqlDB()
    bj_db = MysqlDB(ip=BJ_MYSQL_NODE['MYSQL_IP'], port=3306, db=BJ_MYSQL_NODE['MYSQL_DB'], user_name=BJ_MYSQL_NODE['MYSQL_USER_NAME'] , user_pass=BJ_MYSQL_NODE['MYSQL_USER_PASS'])
    batch = tools.format_time('今天').split(' ')[0]
    yesterday = tools.format_time('昨天').split(' ')[0]

    def start_requests(self):
        yield feapder.Request("https://www.baidu.com")

    def parse(self, request, response):
        pass

    def spider_end(self):
        select_count_batch_sql = """
            SELECT `chart_site`, `batch`, count(*) total FROM (
                SELECT `batch`, `crawl_chart_country`, `chart_site`, `chart_type`, `update_frequency`,
                    `chart_language`, `chart_segment`, `song_name`, `chart_artist_name`, `rank`
                FROM `chart_data_daily`
                WHERE `batch`='{}'
                GROUP BY `crawl_chart_country`, `chart_site`, `chart_type`, `update_frequency`,
                    `chart_language`, `chart_segment`, `song_name`, `chart_artist_name`, `rank`
            ) a
            GROUP BY `chart_site`
            ORDER BY `total`
            """

        insert_monitor_record_sql = """
            INSERT IGNORE INTO `work_status`.`chart_data_daily_monitor_record` (
                `chart_region`, `crawl_chart_country`, `batch`, `chart_site`, `chart_segment`,
                `capture_amount`, `chart_type`, `update_frequency`, `chart_language`, `chart_release_date`
            )
            SELECT
                `chart_region`, `crawl_chart_country`, `batch`, `chart_site`,
                `chart_segment`, count(`rank`) as `capture_amount`,
                `chart_type`, `update_frequency`, `chart_language`, `chart_release_date`
            FROM (
                SELECT
                    `chart_region`, `crawl_chart_country`, `batch`, `chart_site`,
                    `chart_segment`, `rank`, `chart_type`,
                    `update_frequency`, `chart_language`, `chart_release_date`
                FROM `chart_data_daily`
                WHERE `chart_data_daily`.`batch`='{}'
                GROUP BY `chart_region`, `crawl_chart_country`, `chart_site`, `chart_segment`, `chart_type`, `update_frequency`,
                         `chart_language`, `song_name`, `chart_artist_name`, `rank`, `chart_release_date`
            ) a
            GROUP BY `chart_region`, `crawl_chart_country`, `chart_site`, `chart_segment`, `chart_type`,
                `update_frequency`, `chart_language`, `chart_release_date`
            ORDER BY `chart_region`, `crawl_chart_country`, `chart_site`, `chart_type`,
                `update_frequency`, `chart_language`, `chart_segment` DESC
            """

        update_monitor_record_sql = """
            UPDATE `work_status`.`chart_data_daily_monitor_record` AS `record`
            INNER JOIN `chart_url`
                ON `record`.`chart_region`=`chart_url`.`chart_region`
                AND `record`.`chart_site`=`chart_url`.`chart_site`
                AND `record`.`chart_type`=`chart_url`.`chart_type`
                AND `record`.`chart_segment`=`chart_url`.`chart_segment`
                AND `record`.`crawl_chart_country`=`chart_url`.`crawl_chart_country`
                AND `record`.`chart_language`=`chart_url`.`chart_language`
                AND `record`.`update_frequency`=`chart_url`.`update_frequency`
            SET
                `record`.`api`=`chart_url`.`api`,
                `record`.`chart_remarks`=`chart_url`.`chart_remarks`,
                `record`.`web_note`=`chart_url`.`web_note`,
                `record`.`update_time`=`chart_url`.`update_time`,
                `record`.`front_end_web`=`chart_url`.`front_end_web`
            WHERE
                `chart_url`.`chart_status`='used'
                AND `record`.`batch`='{}';
            """

        update_monitor_verify_sql = """
            UPDATE `work_status`.`chart_data_daily_monitor_record` AS `record`
            SET
                `record`.`verified_amount`=`record`.`capture_amount`,
                `record`.`checked`=1
            WHERE
                `record`.`chart_segment`=`record`.`capture_amount`
                AND `record`.`batch`='{}';
            """

        update_monitor_verify_sql_by_site = """
                    UPDATE `work_status`.`chart_data_daily_monitor_record` AS `record`
                    SET
                        `record`.`verified_amount`=`record`.`capture_amount`,
                        `record`.`checked`=1
                    WHERE
                        `record`.`chart_site` IN ({site})
                        AND `record`.`batch`='{batch}';
                    """

        update_monitor_verify_sql_where_spotify = """
                    UPDATE `work_status`.`chart_data_daily_monitor_record` AS `record`
                    SET
                        `record`.`verified_amount`=`record`.`capture_amount`,
                        `record`.`checked`=1
                    WHERE
                        `record`.`chart_site`='spotify'
                        AND `record`.`batch`='{batch}';
                    """

        # update_work_status_sql = """
        #     UPDATE `work_status`.`chart_daily_status`
        #     SET
        #         `spotify_listeners`=(
        #             SELECT COUNT(1)
        #             FROM `spotify_artist_info_batch_data`
        #             WHERE `batch`='{batch}'),
        #         `chart_daily`=(
        #             SELECT COUNT(1)
        #             FROM `chart_data_daily`
        #             WHERE `batch`='{batch}')
        #     WHERE `batch`='{batch}';
        #     """
        
        count_artist = """
            SELECT COUNT(1)
            FROM `spotify_artist_info_batch_data`
            WHERE `batch`='{}';
        """
        count_artist = self.db.find(count_artist.format(self.batch), limit=1)[0]
        count_chart = """
            SELECT COUNT(1)
            FROM `chart_data_daily`
            WHERE `batch`='{}';
        """
        count_chart = self.db.find(count_chart.format(self.batch), limit=1)[0]
        update_work_status_sql = """
            INSERT IGNORE INTO `work_status`.`chart_daily_status`
            (`batch`, `spotify_listeners`, `chart_daily`)
            VALUES
            ('{}', {}, {});
            """.format(self.batch, count_artist, count_chart)

        get_monitor_record_sql = """
            SELECT
                `chart_region`, `crawl_chart_country`, `batch`, `chart_site`, `chart_segment`,
                `capture_amount`, `checked`, `chart_type`, `update_frequency`, `chart_language`
            FROM `work_status`.`chart_data_daily_monitor_record`
            WHERE `batch`='{}'
            ORDER BY `chart_region`, `crawl_chart_country`, `chart_site`, `chart_type`, `update_frequency`, `chart_language`;
            """

        # 榜单数据按批次/榜单/更新频率/榜单类型等 分类统计的结果 监控数据
        self.db.execute(insert_monitor_record_sql.format(self.batch))
        self.db.execute(update_monitor_record_sql.format(self.batch))
        self.db.execute(update_monitor_verify_sql.format(self.batch))
        self.db.execute(update_work_status_sql.format(batch=self.batch))

        count_chart_today = pd.DataFrame(
                self.db.find(
                    select_count_batch_sql.format(self.batch),
                    to_json=True
                ), dtype='str')
        count_chart_yesterday = pd.DataFrame(
                self.db.find(
                    select_count_batch_sql.format(self.yesterday),
                    to_json=True
                ), dtype='str')
        if 'chart_site' in count_chart_yesterday.columns and 'chart_site' in count_chart_today.columns:
            count = pd.merge(count_chart_today,count_chart_yesterday,
            on='chart_site',
            how='outer')
            count.columns = ['chart_site', '本批次日期', '本批次去重总量', '上批次日期', '上批次去重总量']
        else:
            count = count_chart_today# or count_chart_yesterday
            count.columns = ['chart_site', '本批次日期', '本批次去重总量']

        count.drop_duplicates(inplace=True)
        count.fillna('-', inplace=True)

       # verified_sites = count['chart_site'][count['本批次去重总量'] == count['上批次去重总量']].to_list()
       # # 榜单总量和上次一样时, 直接checked=1
       # if len(verified_sites) > 0:
       #     verified_sites = ["'{}'".format(i) for i in verified_sites]
       #     verified_sites = ",".join(verified_sites)
       #     self.db.execute(update_monitor_verify_sql_by_site.format(site=verified_sites, batch=self.batch))
       # # spotify, 直接checked=1
       # self.db.execute(update_monitor_verify_sql_where_spotify.format(batch=self.batch))

        count = count.to_html()

        data = self.db.find(get_monitor_record_sql.format(self.batch), to_json=True)
        data = pd.DataFrame(data).to_html()
        data = re.sub('<td>0</td>', '<td bgcolor="#FFFF00">0</td>', data)

        html = """
        <!DOCTYPE html>
        <html>
        <meta charset="utf-8">
        <head>
            <title>榜单每日爬虫监控数据</title>
        </head>
        <body>
        <div id="container">
            <h1> 当前批次为 {date} </h1>
            <h3> 按每种网址去重统计的数量 </h3>
            <div id="artist">
                {artist_frame}
            </div>
            <br>
            <h3> 按每种网址去重统计的数量 </h3>
            <div id="segment">
                {count_frame}
            </div>
            <br>
            <h3> 按每个榜单去重统计的数量 </h3>
            <div id="content">
                {data_frame}
            </div>
        </div>
        </body>
        </html>
        """
        artist_msg = self.monitor_artist(self.db, self.bj_db)

        data = html.format(date=self.batch, data_frame=data, count_frame=count, artist_frame=artist_msg)

        email_sender = "18538523231@163.com"    # 发件人 setting.EMAIL_SENDER
        email_password = "PUTZOEPYZAHTQBOC"     # 授权码 setting.EMAIL_PASSWORD
        email_receiver = "bwyao@gmg.fund"       # 收件人 setting.EMAIL_RECEIVER
        email_smtpserver = "smtp.163.com"       # 邮件服务器 setting.EMAIL_SMTPSERVER

        if isinstance(email_receiver, str):
            email_receiver = [email_receiver]

        with EmailSender(
            username=email_sender, password=email_password, smtpserver=email_smtpserver
        ) as email:
            email.send(receivers=email_receiver, title="每日榜单爬虫监控记录", content=data, content_type="html")
            log.info("邮件发送成功")

    def monitor_artist(self, hk_db, bj_db):
        # hk_db = MysqlDB(ip=HK_MYSQL_NODE['MYSQL_IP'], port=HK_MYSQL_NODE['MYSQL_PORT'], user_name=HK_MYSQL_NODE['MYSQL_USER_NAME'], user_pass=HK_MYSQL_NODE['MYSQL_USER_PASS'])
        # bj_db = MysqlDB(ip=BJ_MYSQL_NODE['MYSQL_IP'], port=BJ_MYSQL_NODE['MYSQL_PORT'], user_name=BJ_MYSQL_NODE['MYSQL_USER_NAME'], user_pass=BJ_MYSQL_NODE['MYSQL_USER_PASS'])
        # 获取任务表总量
        task = self.get_count_artist_task(hk_db)
        batch = self.batch
        last_batch = self.yesterday
        # 按批次获取不同服务器的数据部总量
        bj_data_now = self.get_count_artist_data(bj_db, batch=batch)
        bj_data_last = self.get_count_artist_data(bj_db, batch=last_batch)
        hk_data_now = self.get_count_artist_data(hk_db, batch=batch)
        hk_data_last = self.get_count_artist_data(hk_db, batch=last_batch)
        # 处理消息数据
        task_msg = self.handle_dict(task)
        bj_data_now_msg = self.handle_dict(bj_data_now)
        bj_data_last_msg = self.handle_dict(bj_data_last)
        hk_data_now_msg = self.handle_dict(hk_data_now)
        hk_data_last_msg = self.handle_dict(hk_data_last)
        msg = f"""
            <b>任务表</b><br>
            {task_msg}<br>
            <b>北京 数据表 {batch}</b><br>
            {bj_data_now_msg}<br>
            <b>香港 数据表 {batch}</b><br>
            {hk_data_now_msg}<br>
            <b>北京 数据表 {last_batch}</b><br>
            {bj_data_last_msg}<br>
            <b>香港 数据表 {last_batch}</b><br>
            {hk_data_last_msg}<br>
        """
        return msg

    def handle_dict(self, dict_data: dict):
        msg = []
        for k, v in dict_data.items():
            msg.append("{}: {}".format(k, v))
        return "; ".join(msg)

    def get_count_artist_task(self, db):
        spotify_task_sql = """
            SELECT COUNT(1)
            FROM `spotify_artist_info_batch_task`
            WHERE `spotify_artist_id` IS NOT NULL
            AND `spotify_artist_id` != '-';
        """
        twitter_task_sql = """
            SELECT COUNT(1)
            FROM `twitter_artist_info_batch_task`
            WHERE `artist_url` IS NOT NULL
            AND `artist_url` != '-';
        """
        instagram_task_sql = """
            SELECT COUNT(1)
            FROM `instagram_artist_info_batch_task`
            WHERE `artist_url` IS NOT NULL
            AND `artist_url` != '-';
        """
        tiktok_task_sql = """
            SELECT COUNT(1)
            FROM `tiktok_artist_info_batch_task`
            WHERE `sec_uid` IS NOT NULL
            OR `user_name`  IS NOT NULL;
        """
        youtube_task_sql = """
            SELECT COUNT(1)
            FROM `youtube_artist_info_batch_task`
            WHERE `youtube_link` IS NOT NULL
            AND `youtube_link` != '-';
        """
        value = {
            "tiktok": db.find(tiktok_task_sql, limit=1)[0],
            "twitter": db.find(twitter_task_sql, limit=1)[0],
            "spotify": db.find(spotify_task_sql, limit=1)[0],
            "youtube": db.find(youtube_task_sql, limit=1)[0],
            "instagram": db.find(instagram_task_sql, limit=1)[0],
        }
        return value

    def get_count_artist_data(self, db, batch):
        aka_sql = """
            SELECT count(`id`)
            FROM `GMG_DATA_ASSETS`.`gmg_artist_aka`
            WHERE site='spotify'
            AND `id` IS NOT NULL
            AND `id` != '-';
        """
        spotify_data_sql = """
            SELECT COUNT(1)
            FROM (
                SELECT `spotify_artist_id`
                FROM `spotify_artist_info_batch_data`
                WHERE batch='{}'
                GROUP BY `spotify_artist_id`
            ) a;
        """.format(batch)
        twitter_data_sql = """
            SELECT COUNT(1)
            FROM `artist_info_batch_data`
            WHERE `artist_site`='twitter'
            AND `batch`='{}';
        """.format(batch)
        instagram_data_sql = """
            SELECT COUNT(1)
            FROM `artist_info_batch_data`
            WHERE `artist_site`='instagram'
            AND `batch`='{}';
        """.format(batch)
        tiktok_data_sql = """
            SELECT COUNT(1)
            FROM `tiktok_artist_info_batch_data`
            WHERE `batch`='{}';
        """.format(batch)
        youtube_data_sql = """
            SELECT COUNT(1)
            FROM `youtube_artist_info_batch_data`
            WHERE `batch`='{}';
        """.format(batch)
        value = {
            "aka": db.find(aka_sql, limit=1)[0],
            "tiktok": db.find(tiktok_data_sql, limit=1)[0],
            "twitter": db.find(twitter_data_sql, limit=1)[0],
            "spotify": db.find(spotify_data_sql, limit=1)[0],
            "youtube": db.find(youtube_data_sql, limit=1)[0],
            "instagram": db.find(instagram_data_sql, limit=1)[0],
        }
        return value


if __name__ == "__main__":
    MonitorChartAndArtist(redis_key="chart:monitor").start()
