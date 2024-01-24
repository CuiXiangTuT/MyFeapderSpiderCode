import feapder
# from feapder import ArgumentParser
import time
from feapder.utils.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pprint import pprint
from copy import  deepcopy
from datetime import datetime,timedelta
import re

class MyTestAirspider4(feapder.AirSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language':'en-US',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        }
        return request

    def start_requests(self):
        task_id = 1
        task_gmg_artist_id = ""
        task_youtube_music_channel_id = ""
        task_youtube_music_albums_singles_id = ""
        task_youtube_music_albums_singles_url = "https://music.youtube.com/playlist?list=OLAK5uy_kKcnk3OT89jbl03JNyno2w-t4Gpamtf5w"
        yield feapder.Request(url=task_youtube_music_albums_singles_url,
            render=True,
            task_id=task_id,
            task_gmg_artist_id=task_gmg_artist_id,
            task_youtube_music_channel_id=task_youtube_music_channel_id,
            task_youtube_music_albums_singles_id=task_youtube_music_albums_singles_id,
            task_youtube_music_albums_singles_url=task_youtube_music_albums_singles_url
        )
        # print("执行结束",task_id)

    def parse(self, request, response):
        browser: WebDriver = response.browser
        browser.maximize_window()
        js = "window.scrollTo(0, document.body.scrollHeight)"
        browser.execute_script(js)
        time.sleep(4)

        d = dict()
        d["gmg_artist_id"] = None
        d["youtube_music_channel_id"] = None
        d["youtube_music_playlist_id"] = None
        d["youtube_music_playlist_url"] = None
        d["youtube_music_plate_remark"] = None
        d["serial_number"] = 0

        title_detail_info = browser.find_element(By.XPATH,'//div[@class="content-container style-scope ytmusic-detail-header-renderer"]//h2[@class="style-scope ytmusic-detail-header-renderer"]/yt-formatted-string[@class="title style-scope ytmusic-detail-header-renderer"]')
        d["title"] = title_detail_info.text

        subtitle_detail_info = browser.find_elements(By.XPATH,
                                                     '//yt-formatted-string[@class="subtitle style-scope ytmusic-detail-header-renderer"]')
        span_info_list = subtitle_detail_info[0].find_elements(By.XPATH, './/span')
        if len(span_info_list) > 3:
            playlist_type = subtitle_detail_info[0].find_element(By.XPATH, './/span[1]').text
            d['playlist_type'] = 'Playlist' if playlist_type == '播放列表' else None
            d["artist_name"] = subtitle_detail_info[0].find_element(By.XPATH, './/a').text
            d["publish_date"] = subtitle_detail_info[0].find_element(By.XPATH, './/span[4]').text
            d["artist_channel_id"] = subtitle_detail_info[0].find_element(By.XPATH, './/a').get_attribute("href")
        elif len(span_info_list) == 3:
            playlist_type = subtitle_detail_info[0].find_element(By.XPATH, './/span[1]').text
            d['playlist_type'] = 'Playlist' if playlist_type == '播放列表' else None
            at_last_span_info = subtitle_detail_info[0].find_element(By.XPATH, './/span[3]').text
            pattern = r"^\d{4}$"
            match = re.match(pattern, at_last_span_info)
            if match:
                d["artist_name"] = None
                d["publish_date"] = at_last_span_info
                d["artist_channel_id"] = None
            else:
                is_exist_artist_name = subtitle_detail_info[0].find_element(By.XPATH, './/a')
                if is_exist_artist_name:
                    d['artist_name'] = subtitle_detail_info[0].find_element(By.XPATH, './/a').text
                    d["artist_channel_id"] = subtitle_detail_info[0].find_element(By.XPATH, './/a').get_attribute(
                        "href")
                    d["publish_date"] = None
                else:
                    d["artist_name"] = at_last_span_info
                    d["publish_date"] = None
                    d["artist_channel_id"] = None

        # subtitle_detail_info = browser.find_elements(By.XPATH,'//yt-formatted-string[@class="subtitle style-scope ytmusic-detail-header-renderer"]')
        # playlist_type = subtitle_detail_info[0].find_element(By.XPATH,'.//span[1]').text
        # d['playlist_type'] = 'Playlist' if playlist_type=='播放列表' else None
        # d["artist_name"] = subtitle_detail_info[0].find_element(By.XPATH,'.//a').text
        # d["publish_date"] = subtitle_detail_info[0].find_element(By.XPATH,'.//span[4]').text
        # d["artist_channel_id"] = subtitle_detail_info[0].find_element(By.XPATH,'.//a').get_attribute("href")
        d["img_url"] = browser.find_element(By.XPATH,'.//ytmusic-cropped-square-thumbnail-renderer[@class="style-scope ytmusic-detail-header-renderer"]/yt-img-shadow/img').get_attribute('src')

        subtitle_detail_info_1 = browser.find_elements(By.XPATH,'.//yt-formatted-string[@class="second-subtitle style-scope ytmusic-detail-header-renderer"]')
        origin_songs_count = subtitle_detail_info_1[0].find_element(By.XPATH,'.//span[1]').text
        d['origin_songs_count'] = origin_songs_count
        d['songs_count'] = origin_songs_count.replace(' songs','').replace(' song','').replace(" 首歌曲","").strip()
        origin_total_duration = subtitle_detail_info_1[0].find_element(By.XPATH,'.//span[3]').text
        d['origin_total_duration'] = origin_total_duration
        d['total_duration'] = None
        d['url_canonical'] = None

        playlist_list = browser.find_elements(By.XPATH,'//ytmusic-responsive-list-item-renderer[@class="style-scope ytmusic-playlist-shelf-renderer"]')
        for i in playlist_list:
            item = deepcopy(d)

            video_detail_info = i.find_element(By.XPATH,'.//yt-formatted-string[@class="title style-scope ytmusic-responsive-list-item-renderer complex-string"]/a')
            # 歌曲名
            item["youtube_music_video_name"] = video_detail_info.text
            # 歌曲链接
            songs_url = video_detail_info.get_attribute('href')
            item['youtube_music_video_id'] = songs_url.split('v=')[1].split('&list')[0]
            item['youtube_music_video_url'] = songs_url.split('&list')[0]
            item['origin_youtube_music_video_url'] = songs_url
            item['youtube_music_video_url_split_playlist_id'] = songs_url.split('&list=')[1]
            item['youtube_music_video_url_split_playlist_url'] = "https://music.youtube.com/playlist?list="+str(item['youtube_music_video_url_split_playlist_id'])


            column_detail_info = i.find_elements(By.XPATH,'.//yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer complex-string"]')
            if len(column_detail_info)==2:
                artist_detail_info = i.find_elements(By.XPATH,
                                                     './/yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer complex-string"][1]//a')
                artist_list = list()
                artist_channel_id = list()
                for u in artist_detail_info:
                    # 歌手名
                    artist_list.append(u.text)
                    # 歌手channel Id
                    artist_channel_id.append(u.get_attribute("href"))
                if len(artist_list)==1:
                    # 歌手名
                    item["youtube_music_video_artist_name"] = artist_list[0]
                    # 歌手channel Id
                    item["youtube_music_video_artist_channel_id"] = artist_channel_id[0]
                elif len(artist_list)>1:
                    # 歌手名
                    item["youtube_music_video_artist_name"] = ";".join(artist_list)
                    # 歌手channel Id
                    item["youtube_music_video_artist_channel_id"] = ";".join(artist_channel_id)

                album_detail_info = i.find_element(By.XPATH,
                                                   './/yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer complex-string"][2]/a')

                # 专辑名
                item['youtube_music_video_playlist_name'] = album_detail_info.text
                # 专辑链接
                item[
                    "origin_youtube_music_playlist_url"] = album_detail_info.get_attribute("href")
                item['youtube_music_playlist_url_pre_redirect'] = \
                item["origin_youtube_music_playlist_url"]

                play_count_detail_info = i.find_element(By.XPATH,
                                                        './/yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer"]')
                # 播放量
                item["origin_youtube_music_video_play_count"] = play_count_detail_info.text
                play_count = item["origin_youtube_music_video_play_count"].replace(' 次播放', '').strip()
                item['youtube_music_video_play_count'] = int(
                    float(play_count.replace('万', '')) * 10000) if '万' in play_count else int(
                    float(play_count.replace('亿', '')) * 100000000) if '亿' in play_count else play_count


            elif len(column_detail_info)==1:
                detail_info =  i.find_element(By.XPATH,
                                                     './/yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer complex-string"][1]//a')
                href = detail_info.get_attribute('href')
                if "channel" in str(href):
                    item["youtube_music_video_artist_name"] = detail_info.text
                    item["youtube_music_video_artist_channel_id"] = href
                    item['youtube_music_video_playlist_name'] = i.find_element(By.XPATH,'.//yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer"][2]').text
                    item["origin_youtube_music_playlist_url"] = None
                elif "browse" in str(href):
                    item["youtube_music_video_artist_name"] = i.find_element(By.XPATH,'.//yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer"][1]').text
                    item["youtube_music_video_artist_channel_id"] = None
                    item['youtube_music_video_playlist_name'] = detail_info.text
                    item["origin_youtube_music_playlist_url"] = href

                play_count_detail_info = i.find_elements(By.XPATH,
                                                        './/yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer"]')
                if '次播放' in play_count_detail_info[0].text:
                    # 播放量
                    item["origin_youtube_music_video_play_count"] = play_count_detail_info[0].text
                    play_count = item["origin_youtube_music_video_play_count"].replace(' 次播放', '').strip()
                    item['youtube_music_video_play_count'] = int(
                        float(play_count.replace('万', '')) * 10000) if '万' in play_count else int(
                        float(play_count.replace('亿', '')) * 100000000) if '亿' in play_count else play_count
                if '次播放' in play_count_detail_info[1].text:
                    # 播放量
                    item["origin_youtube_music_video_play_count"] = play_count_detail_info[1].text
                    play_count = item["origin_youtube_music_video_play_count"].replace(' 次播放', '').strip()
                    item['youtube_music_video_play_count'] = int(
                        float(play_count.replace('万', '')) * 10000) if '万' in play_count else int(
                        float(play_count.replace('亿', '')) * 100000000) if '亿' in play_count else play_count

            elif len(column_detail_info)==0:
                detail_info = i.find_elements(By.XPATH,'.//[yt-formatted-string@class="flex-column style-scope ytmusic-responsive-list-item-renderer"]')
                item["youtube_music_video_artist_name"] = detail_info[0].text
                item["youtube_music_video_artist_channel_id"] = None
                item['youtube_music_video_playlist_name'] = detail_info[2].text
                item["origin_youtube_music_playlist_url"] = None
                item["origin_youtube_music_video_play_count"] = detail_info[1].text
                play_count = item["origin_youtube_music_video_play_count"].replace(' 次播放', '').strip()
                item['youtube_music_video_play_count'] = int(
                    float(play_count.replace('万', '')) * 10000) if '万' in play_count else int(
                    float(play_count.replace('亿', '')) * 100000000) if '亿' in play_count else play_count



            # album_detail_info = i.find_element(By.XPATH,'.//yt-formatted-string[@class="flex-column style-scope ytmusic-responsive-list-item-renderer complex-string"][2]/a')

            item['youtube_music_playlist_set_video_id'] = None

            # # 专辑名
            # item['youtube_music_video_playlist_name'] = album_detail_info.text
            # # 专辑链接
            # item["origin_youtube_music_playlist_url"] = album_detail_info.get_attribute("href")
            # item['youtube_music_albums_singles_url_pre_redirect'] = item["origin_youtube_music_playlist_url"]
            duration_info = i.find_element(By.XPATH,'.//div[@class="fixed-columns style-scope ytmusic-responsive-list-item-renderer"]/yt-formatted-string[@class="fixed-column MUSIC_RESPONSIVE_LIST_ITEM_COLUMN_DISPLAY_PRIORITY_HIGH style-scope ytmusic-responsive-list-item-renderer style-scope ytmusic-responsive-list-item-renderer"]')
            # 播放时长
            item["origin_duration"] = duration_info.text

            duration_list = item["origin_duration"].split(":")

            if len(duration_list) == 2:
                minutes, seconts = duration_list
                hours = 0
                minutes = int(minutes)
                seconts = int(seconts)
            elif len(duration_list) == 3:
                hours, minutes, seconts = duration_list
                hours = int(hours)
                minutes = int(minutes)
                seconts = int(seconts)
            else:
                seconts = duration_list[0]
                hours = 0
                minutes = 0
                seconts = int(seconts)
            total_seconds = hours * 3600 + minutes * 60 + seconts
            item['duration'] = total_seconds
            # pprint(item)
            item['is_playable'] = 1
            pprint(item)



if __name__ == "__main__":
    MyTestAirspider4().start()