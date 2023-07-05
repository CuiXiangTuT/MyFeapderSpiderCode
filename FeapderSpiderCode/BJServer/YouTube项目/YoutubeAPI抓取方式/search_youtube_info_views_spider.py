# -*- coding: utf-8 -*-
"""
Created on 2023-05-22 14:16:41
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder


class SearchYoutubeInfoViewsSpider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            'Accept': 'application/json'
        }
        return request

    def start_requests(self):
        # task_id = task.id
        task_artist_id = ''
        task_artist_name = '周杰伦'
        task_track_id = ''
        task_track_name = '七里香'
        youtube_key = 'AIzaSyCty9rsiIdbyr85FrjqkqxPqsQeaCL0XkE'
        yield feapder.Request("https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={}&key={}".format(task_track_name+' '+task_artist_name,youtube_key),
            # task_id=task_id,
            task_artist_id=task_artist_id,
            task_artist_name=task_artist_name,
            task_track_id=task_track_id,
            task_track_name=task_track_name,
            youtube_key=youtube_key
        )

    def parse(self, request, response):
        youtube_info = dict()
        res = response.json['items'][0]
        youtube_info['artist_id'] = request.task_artist_id
        youtube_info['artist_name'] = request.task_artist_name
        youtube_info['track_id'] = request.task_track_id
        youtube_info['track_name'] = request.task_track_name
        # etag
        youtube_info['etag'] = res['etag']
        # kind
        youtube_info['kind'] = res['id']['kind']
        # video_id
        youtube_info['youtube_video_id'] = res['id']['videoId']
        # youtube_link
        youtube_info['youtube_link'] = 'https://www.youtube.com/watch?v='+res['id']['videoId']
        # 发布时间
        youtube_info['publish_time'] = res['snippet']['publishTime']
        # channelTitle
        youtube_info['youtube_channel_title'] = res['snippet']['channelTitle']
        # channelId
        youtube_info['youtube_channel_id'] = res['snippet']['channelId']
        # youtube_title
        youtube_info['youtube_title'] = res['snippet']['title']
        view_url = 'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(youtube_info['youtube_video_id'],request.youtube_key)
        headers = {
            'Accept': 'application/json'
        }
        yield feapder.Request(url=view_url,headers=headers,youtube_info=youtube_info,callback=self.parse_views)
        
    
    def parse_views(self,request,response):
        youtube_info = request.youtube_info
        youtube_info['views'] = response.json['items'][0]['statistics']['viewCount']
        # youtube_info['batch'] = self.batch_date
        # yield youtube_info
        print(youtube_info)


if __name__ == "__main__":
    SearchYoutubeInfoViewsSpider().start()