import requests


def get_info_data_func(artist_id,artist_name,track_id,track_name):
    key = 'AIzaSyCty9rsiIdbyr85FrjqkqxPqsQeaCL0XkE'
    song_name = track_name
    url = 'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={}&key={}'.format(song_name+' '+artist_name,key)
    headers = {
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url,headers).json()['items'][0]
        # 用于存储youtube信息
        youtube_info = dict()
        # etag
        youtube_info['etag'] = response['etag']
        # kind
        youtube_info['kind'] = response['id']['kind']
        # video_id
        youtube_info['youtube_video_id'] = response['id']['videoId']
        # youtube_link
        youtube_info['youtube_link'] = 'https://www.youtube.com/watch?v='+response['id']['videoId']
        # 发布时间
        youtube_info['publish_time'] = response['snippet']['publishTime']
        # channelTitle
        youtube_info['youtube_channel_title'] = response['snippet']['channelTitle']
        # channelId
        youtube_info['youtube_channel_id'] = response['snippet']['channelId']
        # youtube_title
        youtube_info['youtube_title'] = response['snippet']['title']
        view_url = 'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(youtube_info['youtube_video_id'],key)
        youtube_info['views'] = requests.get(url=view_url,headers=headers).json()['items'][0]['statistics']['viewCount']
        print(views)
    except:
        print("key量今日已达上限")