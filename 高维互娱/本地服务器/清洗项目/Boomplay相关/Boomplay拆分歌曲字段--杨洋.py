import re

import pymysql


def split_feat_func(track_name):
    """
    拆分出feat后的内容
    :param track_name:
    :return:
    """

    feat_pattern = 'ft\.(.*)|ft (.*)|feat\.(.*)|feat (.*)'
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
    version_pattern = r'Amapiano|remix|outro|Slowed and Reverb|Prod[\.] by|fast|Skit|Slowed|Reverb|0rchestral Edit|Freestyle Video|Freestyle|Produced by|Prod[\.\s]by|Directed[\.]{0,1} by|unofficial|bootleg|Acapella|Acoustic Version|Acoustic|album version|album|BMP Edit|BMP|Bonus Track|Bonus|Bootleg|Clean Version|Clean|Club Edit|club mix|Club|Countinuous Mix|Countinuous|Cover|Deluxe Version|Deluxe Mix|Deluxe Edition|DEMO|Digital Remaster|Digital|Dub Mix|enhanced CD|EP Version|EP|Explicit Version|Extended Mix|Extended Play|Extended Version|Explicit|Flip\.|Flip|Instrumental\.|Instrumental|Inst\.|Instru\.|Instru|Instruments\.|Instruments|intro\.|intro|Live Version|Live Performance|Live|Mashup|Memo|Mixtape|No Vocal|off Vocal|Original Mix|Original|Percapella|Radio Edit|Radio|Radio version|Refix\.|Refix|Relift|Remake|Remastered|Remaster|Remix ver\.|Remix ver|Remix\.|Remix|Remixes|Remix|Reprise|Restrung|Rework|sss Remix Ver|sss Remix|The Extended Cut|theatre Version|variation In Production|VIP|Vocal Edit|Vocal Mix|Vocal Version|Edit|Special Version|Special|Acoustic version|Acoustic|Raw Version|Raw|interlude version|interlude|Choir Version|Choir|Unplugged|Reggaeton Mix|Reggaeton|Acoustic|Inst|Version'
    if '(' in track_name:
        pattern = r'\((.*)\)|\{(.*)\}|\[(.*)\]'
        if re.findall(pattern,track_name,re.IGNORECASE):
            version = ''.join([i for i in re.findall(pattern,track_name,re.IGNORECASE)[0]])
            print(version)
            if re.findall(version_pattern,version,re.IGNORECASE):
                if '(' in version and ')' in version:
                    left_brackets = version.strip().find('(')
                    right_brackets = version.strip().find(')')
                    if right_brackets<left_brackets:
                        return version.strip().replace('(','').replace(')','')
                    else:
                        return version.strip()
                if '(' in version and ')' not in version:
                    return version.strip().replace('(', '')
                if ')' in version and '(' not in version:
                    return version.strip().replace(')', '')
                else:
                    return version.strip()
            else:
                return ""
        else:
            return ""
    else:
        return ""


def cleaned_track_name_func(track_name,feat_name,version):
    """
    清洗歌曲名
    :param track_name:
    :param feat_name:
    :param version:
    :return:
    """
    if feat_name in version:
        track_name_str = track_name.replace(version.strip(), "")
    elif version in feat_name:
        track_name_str = track_name.replace(feat_name.strip(), "")
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
    pattern = r'.*\((.*?)\).*'
    if re.findall(pattern,track_name_cleaned):
        mid_track_name = re.findall(pattern, track_name_cleaned)[0].strip()
        if len(mid_track_name)==0:
            track_name_cleaned = track_name_cleaned.replace('(', '').replace(')', '').strip()
    feat_pattern = r'([\s\(\{]feat\..*|[\s\(\{]feat.*|[\s\(\{]ft\..*|[\s\(\{]ft.*)'
    if re.findall(feat_pattern, track_name_cleaned):
        track_name_cleaned = re.sub(feat_pattern, '', track_name_cleaned)
    return track_name_cleaned


def main():
    conn = pymysql.Connect(host='127.0.0.1',user='root',password='123456',port=3306,db='mydb01')
    cursor = conn.cursor()
    sql='SELECT track_id,track_name FROM `boomplay_track_info_batch_data`'
    cursor.execute(sql)
    data = cursor.fetchall()

    for tuple_track_info in data:
        feat_name = split_feat_func(tuple_track_info[1])
        version = split_version_func(tuple_track_info[1])
        track_name_cleaned = str(cleaned_track_name_func(tuple_track_info[1],feat_name,version))
        print("id：",tuple_track_info[0])
        print("track_name：",tuple_track_info[1])
        print("feat_name：",feat_name)
        print("version：",version)
        print("track_name_cleaned：",track_name_cleaned)
        print("-------------------------------------------------------------")
        sql = """INSERT IGNORE INTO track_clean_table_test(`track_id`,`track_name`,`track_name_cleaned`,`feat_artist_name`,`version`)values ("{}","{}","{}","{}","{}")"""
        cursor.execute(sql.format(tuple_track_info[0],tuple_track_info[1],track_name_cleaned,feat_name,version))
        conn.commit()

if __name__ == '__main__':
    main()