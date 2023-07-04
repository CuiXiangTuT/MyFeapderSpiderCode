import re

import pymysql


def split_feat_func(track_name):
    """
    拆分出feat后的内容
    :param track_name:
    :return:
    """

    feat_pattern = 'ft\.(.*)|ft\. (.*)|ft (.*)|feat\.(.*)|feat\. (.*)|feat (.*)'
    if re.findall(feat_pattern,track_name, re.IGNORECASE):
        feat_name = ''.join(re.findall(feat_pattern, track_name, re.IGNORECASE)[0]).strip()
        if '(' not in feat_name and ')' in feat_name:
            feat_name = feat_name.replace(')','')
        return feat_name
    else:
        return ""



def split_version_func(track_name):
    """
    拆分出版本信息
    :param track_name:
    :return:
    """
    if '-' not in track_name and '|' not in track_name:
        version_pattern = r'Amapiano|remix|outro|Slowed and Reverb|Prod[\.] by|fast|Skit|Slowed|Reverb|0rchestral Edit|Freestyle Video|Freestyle|Produced by|Prod[\.\s]by|Directed[\.]{0,1} by|unofficial|bootleg|Acapella|Acoustic Version|Acoustic|album version|album|BMP Edit|BMP|Bonus Track|Bonus|Bootleg|Clean Version|Clean|Club Edit|club mix|Club|Countinuous Mix|Countinuous|Cover|Deluxe Version|Deluxe Mix|Deluxe Edition|DEMO|Digital Remaster|Digital|Dub Mix|enhanced CD|EP Version|EP|Explicit Version|Extended Mix|Extended Play|Extended Version|Explicit|Flip\.|Flip|Instrumental\.|Instrumental|Inst\.|Instru\.|Instru|Instruments\.|Instruments|intro\.|intro|Live Version|Live Performance|Live|Mashup|Memo|Mixtape|No Vocal|off Vocal|Original Mix|Original|Percapella|Radio Edit|Radio|Radio version|Refix\.|Refix|Relift|Remake|Remastered|Remaster|Remix ver\.|Remix ver|Remix\.|Remix|Remixes|Remix|Reprise|Restrung|Rework|sss Remix Ver|sss Remix|The Extended Cut|theatre Version|variation In Production|VIP|Vocal Edit|Vocal Mix|Vocal Version|Edit|Special Version|Special|Acoustic version|Acoustic|Raw Version|Raw|interlude version|interlude|Choir Version|Choir|Unplugged|Reggaeton Mix|Reggaeton|Acoustic|Inst|Version|Official|Audio|Video|Lirik|Music|mixed'
        if '(' in track_name or '[' in track_name or '{' in track_name:
            pattern = r'\((.*)\)|\{(.*)\}|\[(.*)\]'
            if re.findall(pattern,track_name,re.IGNORECASE):
                mid_version = ''.join([i for i in re.findall(pattern,track_name,re.IGNORECASE)[0]])
                if re.findall(version_pattern,mid_version,re.IGNORECASE):
                    if '(' in mid_version and ')' in mid_version:
                        left_brackets = mid_version.strip().find('(')
                        right_brackets = mid_version.strip().find(')')
                        if right_brackets<left_brackets:
                            left_str = mid_version[:right_brackets]
                            right_str = mid_version[left_brackets:]
                            if re.findall(version_pattern,left_str,re.IGNORECASE):
                                if re.findall(version_pattern,right_str,re.IGNORECASE):
                                    return mid_version.strip().replace('(','').replace(')',''),mid_version
                                else:
                                    return left_str.strip().replace('(', '').replace(')', ''), mid_version
                            else:
                                return right_str.strip().replace('(','').replace(')',''),mid_version
                        else:
                            return mid_version.strip(),mid_version
                    if '(' in mid_version and ')' not in mid_version:
                        return mid_version.strip().replace('(', ''),mid_version
                    if ')' in mid_version and '(' not in mid_version:
                        return mid_version.strip().replace(')', ''),mid_version
                    else:
                        return mid_version.strip(),mid_version
                else:
                    return "",mid_version
            else:
                return "",""
        else:
            return "",""
    else:
        track_name_r = track_name.replace('[', '(').replace('{', '(').replace(']', '(').replace('}', '(').replace(')', '(').replace('|', '(').replace('-', '(').replace('/', '(')
        version_pattern = r'Amapiano|remix|outro|Slowed and Reverb|Prod[\.] by|fast|Skit|Slowed|Reverb|0rchestral Edit|Freestyle Video|Freestyle|Produced by|Prod[\.\s]by|Directed[\.]{0,1} by|unofficial|bootleg|Acapella|Acoustic Version|Acoustic|album version|album|BMP Edit|BMP|Bonus Track|Bonus|Bootleg|Clean Version|Clean|Club Edit|club mix|Club|Countinuous Mix|Countinuous|Cover|Deluxe Version|Deluxe Mix|Deluxe Edition|DEMO|Digital Remaster|Digital|Dub Mix|enhanced CD|EP Version|\sEP|EP\s|Explicit Version|Extended Mix|Extended Play|Extended Version|Explicit|Flip\.|Flip|Instrumental\.|Instrumental|Inst\.|Instru\.|Instru|Instruments\.|Instruments|intro\.|intro|Live Version|Live Performance|Live|Mashup|Memo|Mixtape|No Vocal|off Vocal|Original Mix|Original|Percapella|Radio Edit|Radio|Radio version|Refix\.|Refix|Relift|Remake|Remastered|Remaster|Remix ver\.|Remix ver|Remix\.|Remix|Remixes|Remix|Reprise|Restrung|Rework|sss Remix Ver|sss Remix|The Extended Cut|theatre Version|variation In Production|VIP|Vocal Edit|Vocal Mix|Vocal Version|Edit|Special Version|Special|Acoustic version|Acoustic|Raw Version|Raw|interlude version|interlude|Choir Version|Choir|Unplugged|Reggaeton Mix|Reggaeton|Acoustic|Inst|Version|Official|Audio|Video|Lirik|Loud Line Music|Music|Mixed'
        if '(' in track_name_r:
            # 将歌曲按照'('切分
            track_list = track_name_r.split('(') # "七里香 （ 周杰伦 （ 袁咏琳(remix(Long Version)) 香港"
            is_flag = False
            for track_per in range(len(track_list)):
                if len(track_list[track_per].strip()): # 七里香，周杰伦，袁咏琳，remix，Long Version)) 香港
                    # 匹配当前字段 ，是否含有版本等信息，如果有，返回获取当前字符串的下标地址，进行
                    if re.findall(version_pattern,track_list[track_per],re.IGNORECASE):
                        version_index = track_name_r.find(track_list[track_per])
                        print("version_index :",version_index)
                        last_index = track_name_r.find('(',version_index+1)
                        print("last_index :",last_index)
                        is_flag = True
                        if last_index != -1:
                            version = track_name[version_index:last_index]
                            if '(' not in version and ')' in version:
                                print("1")
                                return track_name[version_index:last_index].strip(),""
                            if '[' not in version and ']' in version:
                                print("2")
                                return track_name[version_index:last_index].strip(),""
                            if '{' not in version and '}' in version:
                                print("3")
                                return track_name[version_index:last_index].strip(),""
                            else:
                                print("4")
                                return version.strip(),""
                        else:
                            print("5")
                            return track_name[version_index:].strip(),""
                    else:
                        pass
                else:
                    pass
                if is_flag:
                    break 
            else:
                return "",""
            
        else:
            return "",""


def cleaned_track_name_func(track_name,feat_name,version,mid_version):
    """
    清洗歌曲名
    :param track_name:
    :param feat_name:
    :param version:
    :param mid_version:
    :return:
    """

    if feat_name.strip() in version.strip():
        track_name_str = track_name.replace(version.strip(), "").replace(feat_name.strip(),"")
    elif version.strip() in feat_name.strip():
        track_name_str = track_name.replace(feat_name.strip(), "").replace(version.strip(),"")
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
    if re.findall(pattern,track_name_cleaned):
        # mid_track_name = re.findall(pattern, track_name_cleaned)[0].strip()
        mid_track_name = ''.join([i for i in re.findall(pattern, track_name_cleaned)[0]]).strip()
        if len(mid_track_name)==0:
            track_name_cleaned = track_name_cleaned.replace('(', '').replace(')', '').strip()
            return track_name_cleaned
        else:
            if ")" in mid_track_name or "(" in mid_track_name:
                left_brackets = mid_track_name.strip().find('(')
                right_brackets = mid_track_name.strip().find(')')
                if right_brackets<left_brackets:
                    left_str = mid_track_name[:right_brackets]
                    right_str = mid_track_name[left_brackets:].replace('(',"")
                    if len(right_str)==0:
                        mid_track_name = mid_track_name[:left_brackets]
                        feat_pattern = 'ft\.(.*)|ft\. (.*)|ft (.*)|feat\.(.*)|feat\. (.*)|feat (.*)'
                        if re.findall(feat_pattern, mid_track_name):
                            left_brackets_2 = track_name_cleaned.strip().find('(')
                            track_name_cleaned = track_name_cleaned[:left_brackets_2]
                            return track_name_cleaned
                        else:
                            right_brackets_2 = track_name_cleaned.strip().find(')')
                            track_name_cleaned = track_name_cleaned[:right_brackets_2+1]
                            return track_name_cleaned
                    if len(left_str)==0:
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

def main():
    # 北京服务器IP
    # MYSQL_IP = "122.115.36.92"
    # 香港服务器
    MYSQL_IP = "8.218.99.123"
    MYSQL_PORT = 3306
    # 临时数据库
    MYSQL_DB = "temporary_data"
    MYSQL_USER_NAME = "crawler"
    MYSQL_USER_PASS = "crawler.mysql"
    conn = pymysql.Connect(host=MYSQL_IP,user=MYSQL_USER_NAME,password=MYSQL_USER_PASS,port=MYSQL_PORT,db=MYSQL_DB)
    cursor = conn.cursor()
    insert_sql = """
    INSERT IGNORE INTO `boomplay_track_name_cleaned_data`(track_id,track_name)
    SELECT track_id,TRIM(LOWER(track_name)) track_name FROM `boomplay_track_info_batch_data`
    """
    cursor.execute(insert_sql)
    conn.commit()

    sql='SELECT track_id,track_name FROM `boomplay_track_name_cleaned_data` WHERE state=0'
    cursor.execute(sql)
    data = cursor.fetchall()

    for tuple_track_info in data:
        feat_name = split_feat_func(tuple_track_info[1])
        version, mid_version = split_version_func(tuple_track_info[1])
        track_name_cleaned = str(cleaned_track_name_func(tuple_track_info[1], feat_name, version, mid_version)).replace('"', "'")
        print("id：",tuple_track_info[0])
        print("track_name：",tuple_track_info[1])
        print("feat_name：",feat_name)
        print("version：",version)
        print("track_name_cleaned：",track_name_cleaned)
        print("-------------------------------------------------------------")
        # sql_insert = """
        # INSERT IGNORE INTO boomplay_track_name_cleaned_data(`track_id`,`track_name`,`track_name_cleaned`,`feat_artist_name`,`version`)values ("{}","{}","{}","{}","{}")""".format(tuple_track_info[0],tuple_track_info[1],track_name_cleaned,feat_name,version)
        sql_update = """UPDATE boomplay_track_name_cleaned_data SET track_name_cleaned=%s,feat_artist_name=%s,version=%s,state=1 WHERE track_id=%s AND state = 0"""
        cursor.execute(sql_update,[track_name_cleaned.lower(),feat_name.lower(),version.lower(),tuple_track_info[0]])
        conn.commit()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()