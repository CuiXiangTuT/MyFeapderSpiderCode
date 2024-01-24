import feapder
from feapder import ArgumentParser
from feapder.db.redisdb import RedisDB
from queue import Queue
from feapder.utils.log import log
import os

class MyTestAirspider(feapder.AirSpider):
    redis_db = RedisDB(decode_responses=True)
    # baidu_url = ""
    # url = "https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=id&part=liveStreamingDetails&part=localizations&part=player&part=recordingDetails&part=snippet&part=statistics&part=status&part=topicDetails&maxResults=50"
    youtube_key = "&key={}"

    # def init_task(self):
    #     pass

    def download_midware(self, request):
        request.headers = {
            'Accept': 'application/json'
        }
        all_keys = self.redis_db.keys()
        l = list()
        for key in all_keys:
            if self.redis_db.type(key) == 'zset':
                print("有序集合名称：", key)
                l.append(key)
        if len(l):
            # 提取只包含键的列表
            youtube_quota_list = self.redis_db.zrange('youtube_quota', start=0, end=-1, withscores=True)
            keys = [member[0] for member in youtube_quota_list]
            if len(keys) >= 1:
                youtube_quota_score = self.redis_db.zscore(name="youtube_quota", value=keys[0])
                print("分数：", youtube_quota_score)
                if youtube_quota_score > 0:
                    self.redis_db.zincrby("youtube_quota", -1, keys[0])
                    return request
                else:
                    self.redis_db.zrem("youtube_quota", keys[0])
                    return request
            else:
                print("不存在键值")
                os._exit(137)
        else:
            print("不存在键值")
            os._exit(137)

    def start_requests(self):
        baidu_url = "https://www.google.com/"
        # print("链接为：",url)
        yield feapder.Request(url=baidu_url)

    def parse(self, request, response):
        # print("链接为：",request.url)
        pass

if __name__ == "__main__":
    for i in range(1,100):
        MyTestAirspider().start()
        print("第{}次执行".format(i))
    # MyTestAirspider().start()
