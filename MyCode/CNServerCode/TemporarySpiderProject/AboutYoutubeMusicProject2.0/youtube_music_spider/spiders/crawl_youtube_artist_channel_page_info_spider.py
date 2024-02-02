# -*- coding: utf-8 -*-
"""
Created on 2023-12-12 14:36:17
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
import re
import httpx
from datetime import datetime
from pprint import pprint
from items.youtube_music_info_item import *
import json
import httpx



class CrawlYoutubeArtistChannelPageInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_gmg_artist_name = task.gmg_artist_name
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_channel_name = task.youtube_music_channel_name
        url = "https://music.youtube.com/channel/{}".format(task_youtube_music_channel_id)
        yield feapder.Request(url=url,task_gmg_artist_id=task_gmg_artist_id,task_gmg_artist_name=task_gmg_artist_name,
        task_youtube_music_channel_id=task_youtube_music_channel_id,task_youtube_music_channel_name=task_youtube_music_channel_name,
        task_id=task_id)

    def parse(self, request, response):
        pattern = r"initialData\.push\({([\s\S]*?)}\);"
        response.encoding = response.apparent_encoding
        matches = re.findall(pattern, response.text)
        if len(matches) >= 2:
            second_data = matches[1]
            match = re.search(r"data: '(.*)'", second_data)
            if match:
                data_value = match.group(1)
                data = bytes(data_value, 'UTF-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
                json_data = json.loads(data)
                youtube_music_channel_id_batch_data_item = YoutubeMusicChannelIdBatchDataItem()
                youtube_music_channel_crawl_situation_batch_data_item = YoutubeMusicChannelIdCrawlSituationBatchDataItem()
                youtube_music_artist_page_plate_info_batch_data_item = YoutubeMusicArtistPagePlateInfoBatchDataItem()
                youtube_music_artist_page_plate_info_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_artist_page_plate_info_batch_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_channel_crawl_situation_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_channel_crawl_situation_batch_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_channel_crawl_situation_batch_data_item["youtube_music_channel_name"] = request.task_youtube_music_channel_name
                youtube_music_channel_id_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_channel_id_batch_data_item["gmg_artist_name"] = request.task_gmg_artist_name
                youtube_music_channel_id_batch_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_channel_id_batch_data_item["youtube_music_channel_name"] = request.task_youtube_music_channel_name
                # 1-歌手名
                youtube_music_channel_id_batch_data_item["youtube_music_artist_name"] = json_data["header"]["musicImmersiveHeaderRenderer"]["title"]["runs"][0]["text"]
                youtube_music_channel_crawl_situation_batch_data_item["youtube_music_artist_name"] = youtube_music_channel_id_batch_data_item["youtube_music_artist_name"]
                # 2-歌手channelid
                youtube_music_channel_id_batch_data_item["youtube_music_artist_channel_id"] = json_data["header"]["musicImmersiveHeaderRenderer"]["subscriptionButton"]["subscribeButtonRenderer"]["channelId"]
                # 3-歌手订阅数
                youtube_music_channel_id_batch_data_item["youtube_music_artist_subscriber_count"] = json_data["header"]["musicImmersiveHeaderRenderer"]["subscriptionButton"]["subscribeButtonRenderer"]["subscriberCountWithSubscribeText"]["runs"][0]["text"]
                # 4-歌手简介
                youtube_music_channel_id_batch_data_item["youtube_music_artist_description"] = json_data["header"]["musicImmersiveHeaderRenderer"]["description"]["runs"][0]["text"] if "description" in json_data["header"]["musicImmersiveHeaderRenderer"] else None
                youtube_music_channel_crawl_situation_batch_data_item["youtube_music_infomation_is_exist_remark"] = "EI" if youtube_music_channel_id_batch_data_item["youtube_music_artist_description"] else "NI"
                # 5-歌手主页背景图
                youtube_music_channel_id_batch_data_item["youtube_music_artist_background_image_url"] = json_data["header"]["musicImmersiveHeaderRenderer"]["thumbnail"]["musicThumbnailRenderer"]["thumbnail"]["thumbnails"][0]["url"]
                # 6-歌手被查看次数
                youtube_music_channel_id_batch_data_item["views"] = json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][-1]["musicDescriptionShelfRenderer"]["subheader"]["runs"][0]["text"] if "musicDescriptionShelfRenderer" in json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"] else 0
                # 7-歌手所有歌曲的URL
                if "musicShelfRenderer" in str(json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]) and "browseEndpoint" in str(json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicShelfRenderer"]["title"]["runs"][0]):
                    youtube_music_channel_id_batch_data_item["youtube_music_all_songs_id"] = json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicShelfRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"][2:]
                    youtube_music_channel_id_batch_data_item["youtube_music_all_songs_url"] = "https://music.youtube.com/playlist?list="+youtube_music_channel_id_batch_data_item["youtube_music_all_songs_id"]
                    youtube_music_artist_plate_batch_task_item = YoutubeMusicArtistPlateBatchTaskItem()
                    youtube_music_artist_plate_batch_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                    youtube_music_artist_plate_batch_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                    youtube_music_artist_plate_batch_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_songs_id"][2:]
                    youtube_music_artist_plate_batch_task_item["youtube_music_playlist_url"] = "https://music.youtube.com/playlist?list="+youtube_music_channel_id_batch_data_item["youtube_music_all_songs_id"]
                    youtube_music_artist_plate_batch_task_item["youtube_music_plate_remark"] = "Songs"
                    youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_songs_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_songs_id"]
                    youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_songs_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_songs_url"] 
                    yield youtube_music_artist_plate_batch_task_item
                    youtube_music_channel_crawl_situation_batch_data_item["youtube_music_songs_plate_is_exist_remark"] = "EI"
                else:
                    youtube_music_channel_crawl_situation_batch_data_item["youtube_music_songs_plate_is_exist_remark"] = "NI"
                    if "musicShelfRenderer" in str(json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]):
                        youtube_music_channel_id_batch_data_item["youtube_music_all_songs_id"] = None
                        youtube_music_channel_id_batch_data_item["youtube_music_all_songs_url"] = None
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_songs_id"] = None
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_songs_url"] = None
                        # 歌曲数量少，需要将歌手页面的歌曲全部拿下来
                        json_songs_data = json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicShelfRenderer"]["contents"]
                        for per_songs in json_songs_data:
                            youtube_music_artist_page_songs_batch_data_item = YoutubeMusicArtistPageSongsBatchDataItem()
                            youtube_music_artist_page_songs_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_artist_page_songs_batch_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_artist_page_songs_batch_data_item["youtube_video_id"] = per_songs["musicResponsiveListItemRenderer"]["overlay"]["musicItemThumbnailOverlayRenderer"]["content"]["musicPlayButtonRenderer"]["playNavigationEndpoint"]["watchEndpoint"]["videoId"]
                            youtube_music_artist_page_songs_batch_data_item["youtube_video_img"] =  per_songs["musicResponsiveListItemRenderer"]["thumbnail"]["musicThumbnailRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
                            for per_flex in per_songs["musicResponsiveListItemRenderer"]["flexColumns"]:
                                if "MUSIC_VIDEO_TYPE_ATV" in str(per_flex):
                                    youtube_music_artist_page_songs_batch_data_item["youtube_video_name"] = per_flex["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                                elif "MUSIC_PAGE_TYPE_ARTIST" in str(per_flex):
                                    youtube_music_artist_page_songs_batch_data_item["youtube_video_artist_channel_id"] = ';'.join([k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in per_flex["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"] if "navigationEndpoint" in k])
                                    youtube_music_artist_page_songs_batch_data_item["youtube_video_artist_channel_name"] = ';'.join([k["text"] for k in per_flex["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"] if "navigationEndpoint" in k])
                                elif "MUSIC_PAGE_TYPE_ALBUM" in str(per_flex):
                                    youtube_music_artist_page_songs_batch_data_item["youtube_video_album_id"] = per_flex["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                                    youtube_music_artist_page_songs_batch_data_item["youtube_video_album_name"] = per_flex["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                                elif "pageType" not in str(per_flex) and "plays" in str(per_flex):
                                    youtube_music_artist_page_songs_batch_data_item["original_views"] = per_flex["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                                    flex_views = youtube_music_artist_page_songs_batch_data_item["original_views"].replace(" plays","")
                                    youtube_music_artist_page_songs_batch_data_item["views"] = int(float(flex_views.lower().replace("k",""))*1000) if "k" in flex_views.lower() else int(float(flex_views.lower().replace('m',""))*1000000) if "m" in flex_views.lower() else int(flex_views)
                            youtube_music_video_task_item = YoutubeMusicVideoTaskItem()
                            youtube_music_video_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_video_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_video_task_item["youtube_music_video_id"] = youtube_music_artist_page_songs_batch_data_item["youtube_video_id"]
                            youtube_music_video_task_item["youtube_music_video_url"] = "https://www.youtube.com/watch?v="+youtube_music_video_task_item["youtube_music_video_id"]
                            youtube_music_video_task_item["youtube_music_source_remark"] = "Songs"
                            youtube_music_video_task_item["youtube_music_source_playlist_url"] = None
                            youtube_music_artist_page_songs_batch_data_item["batch"] = self.batch_date
                            yield youtube_music_video_task_item
                            yield youtube_music_artist_page_songs_batch_data_item
                        # yield youtube_music_artist_page_songs_batch_data_item
                    else:
                        youtube_music_channel_id_batch_data_item["youtube_music_all_songs_id"] = None
                        youtube_music_channel_id_batch_data_item["youtube_music_all_songs_url"] = None
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_songs_id"] = None
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_songs_url"] = None
                # 将musicCarouselShelfRenderer单独抽出添加至一个新的空列表进行存储
                json_result_data = json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
                musicCarouselShelfRenderer_data_list = [j for j in json_result_data if "musicCarouselShelfRenderer" in j]
                # 8-歌手【专辑、单曲】的URL
                for k in musicCarouselShelfRenderer_data_list:
                    key_label = k["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["accessibilityData"]["accessibilityData"]["label"]
                    if key_label=="Albums":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_album_plate_is_exist_remark"] = "EI" 
                        youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_id"] = "MPAD"+request.task_youtube_music_channel_id
                        youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_url"] = "https://music.youtube.com/browse/MPAD"+request.task_youtube_music_channel_id
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_albums_singles_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_id"]
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_albums_singles_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_url"]
                        youtube_music_albums_singles_task_item = YoutubeMusicAlbumsSinglesTaskItem()
                        youtube_music_albums_singles_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                        youtube_music_albums_singles_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                        youtube_music_albums_singles_task_item["youtube_music_albums_singles_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_id"]
                        youtube_music_albums_singles_task_item["youtube_music_albums_singles_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_url"]
                        yield youtube_music_albums_singles_task_item

                        # youtube_music_artist_plate_batch_task_item = YoutubeMusicArtistPlateBatchTaskItem()
                        # youtube_music_artist_plate_batch_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                        # youtube_music_artist_plate_batch_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                        # youtube_music_artist_plate_batch_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_id"]
                        # youtube_music_artist_plate_batch_task_item["youtube_music_playlist_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_url"]
                        # youtube_music_artist_plate_batch_task_item["youtube_music_plate_remark"] = "Albums"
                        # yield youtube_music_artist_plate_batch_task_item

                    elif key_label=="Singles":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_singles_plate_is_exist_remark"] = "EI" 
                        youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_id"] = "MPAD"+request.task_youtube_music_channel_id
                        youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_url"] = "https://music.youtube.com/browse/MPAD"+request.task_youtube_music_channel_id
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_albums_singles_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_id"]
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_albums_singles_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_url"]
                        youtube_music_albums_singles_task_item = YoutubeMusicAlbumsSinglesTaskItem()
                        youtube_music_albums_singles_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                        youtube_music_albums_singles_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                        youtube_music_albums_singles_task_item["youtube_music_albums_singles_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_id"] 
                        youtube_music_albums_singles_task_item["youtube_music_albums_singles_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_url"] 
                        yield youtube_music_albums_singles_task_item

                        # youtube_music_artist_plate_batch_task_item = YoutubeMusicArtistPlateBatchTaskItem()
                        # youtube_music_artist_plate_batch_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                        # youtube_music_artist_plate_batch_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                        # youtube_music_artist_plate_batch_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_id"]
                        # youtube_music_artist_plate_batch_task_item["youtube_music_playlist_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_albums_singles_url"]
                        # youtube_music_artist_plate_batch_task_item["youtube_music_plate_remark"] = "Singles"
                        # yield youtube_music_artist_plate_batch_task_item

                    elif key_label=="Videos":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_videos_plate_is_exist_remark"] = "EI"
                        youtube_music_channel_id_batch_data_item["youtube_music_all_videos_id"] = k["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"][2:]
                        youtube_music_channel_id_batch_data_item["youtube_music_all_videos_url"] = "https://music.youtube.com/playlist?list="+youtube_music_channel_id_batch_data_item["youtube_music_all_videos_id"] if youtube_music_channel_id_batch_data_item["youtube_music_all_videos_id"] else None
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_videos_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_videos_id"]
                        youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_videos_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_videos_url"]
                        youtube_music_artist_plate_batch_task_item = YoutubeMusicArtistPlateBatchTaskItem()
                        youtube_music_artist_plate_batch_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                        youtube_music_artist_plate_batch_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                        youtube_music_artist_plate_batch_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_item["youtube_music_all_videos_id"]
                        youtube_music_artist_plate_batch_task_item["youtube_music_playlist_url"] = youtube_music_channel_id_batch_data_item["youtube_music_all_videos_url"]
                        youtube_music_artist_plate_batch_task_item["youtube_music_plate_remark"] = "Videos"
                        yield youtube_music_artist_plate_batch_task_item

                    
                    elif key_label=="Featured on":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_featured_on_plate_is_exist_remark"] = "EI" 
                        # 需要做列表处理
                        featured_list = k["musicCarouselShelfRenderer"]["contents"]
                        for featured_per in featured_list:
                            # 精选集标题
                            youtube_music_artist_page_featured_batch_data_item = YoutubeMusicArtistPageFeaturedBatchDataItem()
                            youtube_music_artist_page_featured_batch_data_item["featured_title"] = featured_per["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                            youtube_music_artist_page_featured_batch_data_item["featured_id"] = featured_per["musicTwoRowItemRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            youtube_music_artist_page_featured_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_artist_page_featured_batch_data_item["youtube_music_artist_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_artist_page_featured_batch_data_item["youtube_music_artist_channel_name"] = request.task_youtube_music_channel_name
                            youtube_music_artist_page_featured_batch_data_item["featured_url"] =  "https://music.youtube.com/playlist?list=" + youtube_music_artist_page_featured_batch_data_item["featured_id"] if youtube_music_artist_page_featured_batch_data_item["featured_id"] else None
                            youtube_music_artist_page_featured_batch_data_item["batch"] = self.batch_date
                            yield youtube_music_artist_page_featured_batch_data_item

                    elif key_label=="Fans might also like":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_fans_might_also_like_plate_is_exist_remark"] = "EI"
                        # 需要做列表处理
                        fans_also_like_list = k["musicCarouselShelfRenderer"]["contents"]
                        for fans_also_like_per in fans_also_like_list:
                            # 粉丝可能还会喜欢的艺人名
                            youtube_music_artist_fans_also_like_batch_data_item = YoutubeMusicArtistFansAlsoLikeBatchDataItem()
                            youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_name"] = fans_also_like_per["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                            youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_channel_id"] = fans_also_like_per["musicTwoRowItemRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            youtube_music_artist_fans_also_like_batch_data_item["origin_fans_also_like_artist_subscriber_count"] = fans_also_like_per["musicTwoRowItemRenderer"]["subtitle"]["runs"][0]["text"]
                            subscriber_count = youtube_music_artist_fans_also_like_batch_data_item["origin_fans_also_like_artist_subscriber_count"].replace(" subscribers","").replace(" subscriber","")
                            youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_subscriber_count"] = int(float(subscriber_count.lower().replace("k",""))*1000) if "k" in subscriber_count.lower() else int(float(subscriber_count.lower().replace('m',""))*1000000) if "m" in subscriber_count.lower() else int(subscriber_count.strip())
                            
                            youtube_music_artist_fans_also_like_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_artist_fans_also_like_batch_data_item["gmg_artist_name"] = request.task_gmg_artist_name
                            youtube_music_artist_fans_also_like_batch_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_artist_fans_also_like_batch_data_item["youtube_music_channel_name"] = request.task_youtube_music_channel_name
                            youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_channel_url"] = "https://music.youtube.com/channel/"+youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_channel_id"]
                            youtube_music_artist_fans_also_like_batch_data_item["batch"] = self.batch_date
                            yield youtube_music_artist_fans_also_like_batch_data_item
                    elif key_label=="Latest episodes":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_latest_episodes_plate_is_exist_remark"] = None
                    elif key_label=="Podcasts":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_podcasts_plate_is_exist_remark"] = None
                        

                    if youtube_music_channel_crawl_situation_batch_data_item["youtube_music_album_plate_is_exist_remark"]!="EI":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_album_plate_is_exist_remark"]="NI"
                    if youtube_music_channel_crawl_situation_batch_data_item["youtube_music_singles_plate_is_exist_remark"] != "EI":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_singles_plate_is_exist_remark"]="NI"
                    if youtube_music_channel_crawl_situation_batch_data_item["youtube_music_videos_plate_is_exist_remark"]!="EI":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_videos_plate_is_exist_remark"]="NI"
                    if youtube_music_channel_crawl_situation_batch_data_item["youtube_music_featured_on_plate_is_exist_remark"]!="EI":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_featured_on_plate_is_exist_remark"]="NI"
                    if youtube_music_channel_crawl_situation_batch_data_item["youtube_music_fans_might_also_like_plate_is_exist_remark"]!="EI":
                        youtube_music_channel_crawl_situation_batch_data_item["youtube_music_fans_might_also_like_plate_is_exist_remark"]="NI"
                youtube_music_channel_crawl_situation_batch_data_item["batch"] = self.batch_date
                youtube_music_channel_id_batch_data_item["batch"] = self.batch_date
                youtube_music_artist_page_plate_info_batch_data_item["batch"] = self.batch_date
                yield youtube_music_channel_id_batch_data_item
                yield youtube_music_artist_page_plate_info_batch_data_item
                yield youtube_music_channel_crawl_situation_batch_data_item
                yield self.update_task_batch(request.task_id, 1) 
        else:               
            print("无法找到第二个initialData.push的值")


if __name__ == "__main__":
    spider = CrawlYoutubeArtistChannelPageInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeArtistChannelPageInfoSpider爬虫")

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
    # python crawl_youtube_artist_channel_page_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_artist_channel_page_info_spider.py --start_worker  # 启动爬虫
