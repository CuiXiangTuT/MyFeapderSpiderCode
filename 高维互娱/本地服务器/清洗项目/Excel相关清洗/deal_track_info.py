import pymysql
import re

def split_album_artist(album_artist):
    """
    返回值：歌手名、feat歌手名
    """
    if album_artist.strip():
        if '|' in album_artist:
            album_artist_mid = album_artist.replace('|',' feat',1)
            album_artist = album_artist_mid.replace('|',',')
        feat_pattern = 'ft\.(.*)|ft\. (.*)|ft (.*)|feat\.(.*)|feat\. (.*)|feat (.*)'
        if re.findall(feat_pattern,album_artist, re.IGNORECASE):
            feat_name = ''.join(re.findall(feat_pattern, album_artist, re.IGNORECASE)[0]).strip()
            feat_p = '(.*?) ft\. |(.*?) ft |(.*) feat\.|(.*) feat'
            artist_name = ''.join(re.findall(feat_p, album_artist, re.IGNORECASE)[0]).strip()
            if '(' not in feat_name and ')' in feat_name:
                feat_name = feat_name.replace(')','')
            return artist_name.strip(),feat_name.strip()
        else:
            return album_artist.strip(),""
    else:
        return "",""


def split_track_name(track_name):
    """
    返回值：歌曲名、歌曲版本
    """
    if track_name.strip():
        if '(' in track_name or '|' in track_name or '-' in track_name: 
            track_name_r = track_name.replace('[', '(').replace('{', '(').replace(']', '(').replace('}', '(').replace(')', '(').replace('|', '(').replace('-', '(').replace('/', '(')
            version_pattern = r'Amapiano|remix|outro|Slowed and Reverb|Prod[\.] by|fast|Skit|Slowed|Reverb|0rchestral Edit|Freestyle Video|Freestyle|Produced by|Prod[\.\s]by|Directed[\.]{0,1} by|unofficial|bootleg|Acapella|Acoustic Version|Acoustic|album version|album|BMP Edit|BMP|Bonus Track|Bonus|Bootleg|Clean Version|Clean|Club Edit|club mix|Club|Countinuous Mix|Countinuous|Cover|Deluxe Version|Deluxe Mix|Deluxe Edition|DEMO|Digital Remaster|Digital|Dub Mix|enhanced CD|EP Version|\sEP|EP\s|Explicit Version|Extended Mix|Extended Play|Extended Version|Explicit|Flip\.|Flip|Instrumental\.|Instrumental|Inst\.|Instru\.|Instru|Instruments\.|Instruments|intro\.|intro|Live Version|Live Performance|Live|Mashup|Memo|Mixtape|No Vocal|off Vocal|Original Mix|Original|Percapella|Radio Edit|Radio|Radio version|Refix\.|Refix|Relift|Remake|Remastered|Remaster|Remix ver\.|Remix ver|Remix\.|Remix|Remixes|Remix|Reprise|Restrung|Rework|sss Remix Ver|sss Remix|The Extended Cut|theatre Version|variation In Production|VIP|Vocal Edit|Vocal Mix|Vocal Version|Edit|Special Version|Special|Acoustic version|Acoustic|Raw Version|Raw|interlude version|interlude|Choir Version|Choir|Unplugged|Reggaeton Mix|Reggaeton|Acoustic|Inst|Version|Official|Audio|Video|Lirik|Loud Line Music|Music|versi ben edan'
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
                                    return track_name[version_index:last_index].strip()
                                if '[' not in version and ']' in version:
                                    print("2")
                                    return track_name[version_index:last_index].strip()
                                if '{' not in version and '}' in version:
                                    print("3")
                                    return track_name[version_index:last_index].strip()
                                else:
                                    print("4")
                                    return version.strip()
                            else:
                                print("5")
                                return track_name[version_index:].strip()
                        else:
                            pass
                    else:
                        pass
                    if is_flag:
                        break 
                else:
                    return ""
        else:
            return ""
    else:
        return ""


def track_name_clean_func(track_name,version):
    if track_name.strip():
        track_name_clean = track_name.replace(version,"").strip().replace("()","").strip()
        return track_name_clean
    else:
        return ""


        

if __name__ == "__main__":
    conn = pymysql.Connect(host='192.168.10.100',user='root',password='123456',port=3306,db='MYTEST')
    cursor = conn.cursor()

    sql = """
    SELECT album_artist,track_name FROM deal_track_info
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in range(len(data)):
        print("序号：",i)
        artist,feat_artist = split_album_artist(data[i][0])
        print("原album_artist：",data[i][0])
        print("artist：",artist)
        print("feat_artist：",feat_artist)
        version = split_track_name(data[i][1])
        track_name_clean = track_name_clean_func(data[i][1],version)
        print("原Track Name：",data[i][1])
        print("version：",version)
        print("track_name_clean：",track_name_clean)
        update_sql = """
        UPDATE `deal_track_info` SET artist="{}",feat_artist="{}",track_name_clean="{}",track_version="{}"
        WHERE album_artist="{}" and track_name="{}"
        """.format(artist,feat_artist,track_name_clean,version,data[i][0],data[i][1])
        cursor.execute(update_sql)
        conn.commit()
        print("----------------------------------------------")