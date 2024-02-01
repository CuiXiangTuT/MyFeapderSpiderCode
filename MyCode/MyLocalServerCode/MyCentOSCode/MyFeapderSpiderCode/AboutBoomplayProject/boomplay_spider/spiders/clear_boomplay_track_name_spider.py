# -*- coding: utf-8 -*-
"""
Created on 2023-11-08 16:44:04
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
import re


class ClearBoomplayTrackNameSpider(feapder.BatchSpider):
    def download_midware(self, request):
        request.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_track_id = task.track_id
        task_track_name = task.track_name
        url = "https://www.baidu.com/"
        yield feapder.Request(url=url, task_id=task_id, task_track_id=task_track_id, task_track_name=task_track_name)

    def parse(self, request, response):
        task_track_id = request.task_track_id
        task_track_name = request.task_track_name
        feat_name = self.split_feat_func(task_track_name)
        version, mid_version = self.split_version_func(task_track_name)
        track_name_cleaned = str(
            self.cleaned_track_name_func(task_track_name, feat_name, version, mid_version)).replace('"', "'")
        update_sql = """
        UPDATE boomplay_track_name_cleaned_data
        SET track_name_cleaned = {task_track_name_cleaned},feat_artist_name = {task_feat_artist_name},`version` = {task_version}
        WHERE track_id = {task_track_id}
        """.format(task_track_name_cleaned='"'+track_name_cleaned.lower()+'"',task_feat_artist_name='"'+feat_name.lower()+'"',task_version='"'+version.lower()+'"',task_track_id=task_track_id)
        yield self.update_task_batch(request.task_id, 1)
        return self._mysqldb.update(update_sql)

    def split_feat_func(self, track_name):
        """
        拆分出feat后的内容
        :param track_name:
        :return:
        """

        feat_pattern = 'ft\.(.*)|ft\. (.*)|ft (.*)|feat\.(.*)|feat\. (.*)|feat (.*)'
        if re.findall(feat_pattern, track_name, re.IGNORECASE):
            feat_name = ''.join(re.findall(feat_pattern, track_name, re.IGNORECASE)[0]).strip()
            if '(' not in feat_name and ')' in feat_name:
                feat_name = feat_name.replace(')', '')
            return feat_name
        else:
            return ""

    def split_version_func(self, track_name):
        """
        拆分出版本信息
        :param track_name:
        :return:
        """
        if '-' not in track_name and '|' not in track_name:
            version_pattern = r'Amapiano|remix|outro|Slowed and Reverb|Prod[\.] by|fast|Skit|Slowed|Reverb|0rchestral Edit|Freestyle Video|Freestyle|Produced by|Prod[\.\s]by|Directed[\.]{0,1} by|unofficial|bootleg|Acapella|Acoustic Version|Acoustic|album version|album|BMP Edit|BMP|Bonus Track|Bonus|Bootleg|Clean Version|Clean|Club Edit|club mix|Club|Countinuous Mix|Countinuous|Cover|Deluxe Version|Deluxe Mix|Deluxe Edition|DEMO|Digital Remaster|Digital|Dub Mix|enhanced CD|EP Version|EP|Explicit Version|Extended Mix|Extended Play|Extended Version|Explicit|Flip\.|Flip|Instrumental\.|Instrumental|Inst\.|Instru\.|Instru|Instruments\.|Instruments|intro\.|intro|Live Version|Live Performance|Live|Mashup|Memo|Mixtape|No Vocal|off Vocal|Original Mix|Original|Percapella|Radio Edit|Radio|Radio version|Refix\.|Refix|Relift|Remake|Remastered|Remaster|Remix ver\.|Remix ver|Remix\.|Remix|Remixes|Remix|Reprise|Restrung|Rework|sss Remix Ver|sss Remix|The Extended Cut|theatre Version|variation In Production|VIP|Vocal Edit|Vocal Mix|Vocal Version|Edit|Special Version|Special|Acoustic version|Acoustic|Raw Version|Raw|interlude version|interlude|Choir Version|Choir|Unplugged|Reggaeton Mix|Reggaeton|Acoustic|Inst|Version|Official|Audio|Video|Lirik|Music|mixed'
            if '(' in track_name or '[' in track_name or '{' in track_name:
                pattern = r'\((.*)\)|\{(.*)\}|\[(.*)\]'
                if re.findall(pattern, track_name, re.IGNORECASE):
                    mid_version = ''.join([i for i in re.findall(pattern, track_name, re.IGNORECASE)[0]])
                    if re.findall(version_pattern, mid_version, re.IGNORECASE):
                        if '(' in mid_version and ')' in mid_version:
                            left_brackets = mid_version.strip().find('(')
                            right_brackets = mid_version.strip().find(')')
                            if right_brackets < left_brackets:
                                left_str = mid_version[:right_brackets]
                                right_str = mid_version[left_brackets:]
                                if re.findall(version_pattern, left_str, re.IGNORECASE):
                                    if re.findall(version_pattern, right_str, re.IGNORECASE):
                                        return mid_version.strip().replace('(', '').replace(')', ''), mid_version
                                    else:
                                        return left_str.strip().replace('(', '').replace(')', ''), mid_version
                                else:
                                    return right_str.strip().replace('(', '').replace(')', ''), mid_version
                            else:
                                return mid_version.strip(), mid_version
                        if '(' in mid_version and ')' not in mid_version:
                            return mid_version.strip().replace('(', ''), mid_version
                        if ')' in mid_version and '(' not in mid_version:
                            return mid_version.strip().replace(')', ''), mid_version
                        else:
                            return mid_version.strip(), mid_version
                    else:
                        return "", mid_version
                else:
                    return "", ""
            else:
                return "", ""
        else:
            track_name_r = track_name.replace('[', '(').replace('{', '(').replace(']', '(').replace('}', '(').replace(
                ')', '(').replace('|', '(').replace('-', '(').replace('/', '(')
            version_pattern = r'Amapiano|remix|outro|Slowed and Reverb|Prod[\.] by|fast|Skit|Slowed|Reverb|0rchestral Edit|Freestyle Video|Freestyle|Produced by|Prod[\.\s]by|Directed[\.]{0,1} by|unofficial|bootleg|Acapella|Acoustic Version|Acoustic|album version|album|BMP Edit|BMP|Bonus Track|Bonus|Bootleg|Clean Version|Clean|Club Edit|club mix|Club|Countinuous Mix|Countinuous|Cover|Deluxe Version|Deluxe Mix|Deluxe Edition|DEMO|Digital Remaster|Digital|Dub Mix|enhanced CD|EP Version|\sEP|EP\s|Explicit Version|Extended Mix|Extended Play|Extended Version|Explicit|Flip\.|Flip|Instrumental\.|Instrumental|Inst\.|Instru\.|Instru|Instruments\.|Instruments|intro\.|intro|Live Version|Live Performance|Live|Mashup|Memo|Mixtape|No Vocal|off Vocal|Original Mix|Original|Percapella|Radio Edit|Radio|Radio version|Refix\.|Refix|Relift|Remake|Remastered|Remaster|Remix ver\.|Remix ver|Remix\.|Remix|Remixes|Remix|Reprise|Restrung|Rework|sss Remix Ver|sss Remix|The Extended Cut|theatre Version|variation In Production|VIP|Vocal Edit|Vocal Mix|Vocal Version|Edit|Special Version|Special|Acoustic version|Acoustic|Raw Version|Raw|interlude version|interlude|Choir Version|Choir|Unplugged|Reggaeton Mix|Reggaeton|Acoustic|Inst|Version|Official|Audio|Video|Lirik|Loud Line Music|Music|Mixed'
            if '(' in track_name_r:
                # 将歌曲按照'('切分
                track_list = track_name_r.split('(')  # "七里香 （ 周杰伦 （ 袁咏琳(remix(Long Version)) 香港"
                is_flag = False
                for track_per in range(len(track_list)):
                    if len(track_list[track_per].strip()):  # 七里香，周杰伦，袁咏琳，remix，Long Version)) 香港
                        # 匹配当前字段 ，是否含有版本等信息，如果有，返回获取当前字符串的下标地址，进行
                        if re.findall(version_pattern, track_list[track_per], re.IGNORECASE):
                            version_index = track_name_r.find(track_list[track_per])
                            print("version_index :", version_index)
                            last_index = track_name_r.find('(', version_index + 1)
                            print("last_index :", last_index)
                            is_flag = True
                            if last_index != -1:
                                version = track_name[version_index:last_index]
                                if '(' not in version and ')' in version:
                                    print("1")
                                    return track_name[version_index:last_index].strip(), ""
                                if '[' not in version and ']' in version:
                                    print("2")
                                    return track_name[version_index:last_index].strip(), ""
                                if '{' not in version and '}' in version:
                                    print("3")
                                    return track_name[version_index:last_index].strip(), ""
                                else:
                                    print("4")
                                    return version.strip(), ""
                            else:
                                print("5")
                                return track_name[version_index:].strip(), ""
                        else:
                            pass
                    else:
                        pass
                    if is_flag:
                        break
                else:
                    return "", ""

            else:
                return "", ""

    def cleaned_track_name_func(self, track_name, feat_name, version, mid_version):
        """
        清洗歌曲名
        :param track_name:
        :param feat_name:
        :param version:
        :param mid_version:
        :return:
        """

        if feat_name.strip() in version.strip():
            track_name_str = track_name.replace(version.strip(), "").replace(feat_name.strip(), "")
        elif version.strip() in feat_name.strip():
            track_name_str = track_name.replace(feat_name.strip(), "").replace(version.strip(), "")
        else:
            track_name_str = track_name.replace(feat_name.strip(), "").replace(version.strip(), "")
        track_name_cleaned = track_name_str
        if track_name_cleaned.strip().endswith(" ft."):
            track_name_cleaned = track_name_cleaned.replace(" ft.", "")
        if track_name_cleaned.strip().endswith(" ft"):
            track_name_cleaned = track_name_cleaned.replace(" ft", "")
        if track_name_cleaned.strip().endswith(" feat."):
            track_name_cleaned = track_name_cleaned.replace(" feat.", "")
        if track_name_cleaned.strip().endswith(" feat"):
            track_name_cleaned = track_name_cleaned.replace(" feat", "")
        if track_name_cleaned.strip().endswith(" Feat"):
            track_name_cleaned = track_name_cleaned.replace(" Feat", "")
        if track_name_cleaned.strip().endswith(" Feat."):
            track_name_cleaned = track_name_cleaned.replace(" Feat.", "")
        if track_name_cleaned.strip().endswith(" Ft"):
            track_name_cleaned = track_name_cleaned.replace(" Ft", "")
        if track_name_cleaned.strip().endswith(" Ft."):
            track_name_cleaned = track_name_cleaned.replace(" Ft.", "")
        if track_name_cleaned.strip().endswith("-"):
            track_name_cleaned = track_name_cleaned.replace("-", "")
        if track_name_cleaned.strip().endswith("|"):
            track_name_cleaned = track_name_cleaned.replace("|", "")
        if track_name_cleaned.strip().startswith("-"):
            track_name_cleaned = track_name_cleaned.replace("-", "")
        if track_name_cleaned.strip().startswith("|"):
            track_name_cleaned = track_name_cleaned.replace("|", "")
        pattern = r'\((.*)\)|\[(.*)\]|\{(.*)\}'
        if re.findall(pattern, track_name_cleaned):
            # mid_track_name = re.findall(pattern, track_name_cleaned)[0].strip()
            mid_track_name = ''.join([i for i in re.findall(pattern, track_name_cleaned)[0]]).strip()
            if len(mid_track_name) == 0:
                track_name_cleaned = track_name_cleaned.replace('(', '').replace(')', '').strip()
                return track_name_cleaned
            else:
                if ")" in mid_track_name or "(" in mid_track_name:
                    left_brackets = mid_track_name.strip().find('(')
                    right_brackets = mid_track_name.strip().find(')')
                    if right_brackets < left_brackets:
                        left_str = mid_track_name[:right_brackets]
                        right_str = mid_track_name[left_brackets:].replace('(', "")
                        if len(right_str) == 0:
                            mid_track_name = mid_track_name[:left_brackets]
                            feat_pattern = 'ft\.(.*)|ft\. (.*)|ft (.*)|feat\.(.*)|feat\. (.*)|feat (.*)'
                            if re.findall(feat_pattern, mid_track_name):
                                left_brackets_2 = track_name_cleaned.strip().find('(')
                                track_name_cleaned = track_name_cleaned[:left_brackets_2]
                                return track_name_cleaned
                            else:
                                right_brackets_2 = track_name_cleaned.strip().find(')')
                                track_name_cleaned = track_name_cleaned[:right_brackets_2 + 1]
                                return track_name_cleaned
                        if len(left_str) == 0:
                            left_brackets_2 = track_name_cleaned.strip().find('(')
                            track_name_cleaned = track_name_cleaned[:left_brackets_2]
                            return track_name_cleaned
                else:
                    feat_pattern = 'ft\.(.*)|ft\. (.*)|ft (.*)|feat\.(.*)|feat\. (.*)|feat (.*)'
                    if re.findall(feat_pattern, track_name_cleaned):
                        left_brackets_2 = track_name_cleaned.strip().find('(')
                        track_name_cleaned = track_name_cleaned[:left_brackets_2]
                    return track_name_cleaned
        else:
            return track_name_cleaned


if __name__ == "__main__":
    spider = ClearBoomplayTrackNameSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="ClearBoomplayTrackNameSpider爬虫")

    parser.add_argument(
        "--start_master",
        action="store_true",
        help="添加任务",
        function=spider.start_monitor_task,
    )
    parser.add_argument(
        "--start_worker", action="store_true", help="启动爬虫", function=spider.start
    )

    parser.start()

    # 直接启动
    # spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python clear_boomplay_track_name_spider.py --start_master  # 添加任务
    # python clear_boomplay_track_name_spider.py --start_worker  # 启动爬虫
