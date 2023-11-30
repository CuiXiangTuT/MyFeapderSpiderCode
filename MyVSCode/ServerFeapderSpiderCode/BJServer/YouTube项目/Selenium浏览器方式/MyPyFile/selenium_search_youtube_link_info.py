from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.support import expected_conditions as EC

# import random
import time
import json
import pandas as pd
import re
import redis


crawl_type = 'name'
task_file = '../MyFile/mena.xlsx'

crawl_date = 'searchyoutubetrack20230330' # 更改
sheet_name = 'searchyoutubetrack20230330'

redisClient = redis.StrictRedis('8.218.99.123', 6379, 10, password='GMG.redis')
redis_task_key = 'youtube_view_spider:task:{}'.format(crawl_date)
redis_href_key = 'youtube_view_spider:href:{}'.format(crawl_date)

def get_driver():
    chrome_option = Options()
    chrome_option.add_argument('lang=en_US')
    No_Image_loading = {"profile.managed_default_content_settings.images": 2}
    chrome_option.add_experimental_option("prefs", No_Image_loading)
    driver = webdriver.Chrome(options=chrome_option)
    wait = WebDriverWait(driver, 10)
    return driver, wait


def add_task(task_file_name, type_='name', task_sheet_name='Sheet1'):
    df = pd.read_excel(task_file_name, sheet_name=task_sheet_name)
    print("excel任务量", len(df))
    task_ = []  # 需要抓video_id的任务
    href_ = []  # 有video_id的任务

    # 已经抓完的部分任务
    history = set()
    history.update(redisClient.smembers(redis_href_key))
    history.update(redisClient.smembers(redis_task_key))
    history = [json.loads(i)['NO.'] for i in history]
    history = set(history)
    print("已完成任务量", len(history))

    columns = set(df.columns.tolist())
    # 判断列名有效性
    if type_ == 'name' and ({'artist_name', 'song_name', 'NO.'} - columns):
        raise ValueError("表中必须包含 'artist_name', 'song_name', 'NO.' 三列")
    elif type_ == 'isrc' and ({'isrc', 'NO.'} - columns):
        raise ValueError("表中必须包含 'isrc', 'NO.' 两列")
    elif type_ == 'song' and ({'song_name', 'NO.'} - columns):
        raise ValueError("表中必须包含 'song_name', 'NO.' 两列")
    elif type_ == 'video' and ({'video_id', 'NO.'} - columns):
        raise ValueError("表中必须包含 'video_id', 'NO.' 两列")

    data = df.to_json(orient='records')
    for i in json.loads(data):
        # 剔除history已有数据, 根据video_id是否为空, 将任务分配到相应队列里
        if i['NO.'] in history:
            continue
        if i.get('video_id', None) is not None:
            href_.append(i)
        else:
            task_.append(i)
    print('add {} tasks to `task_`.'.format(len(task_)))
    print('add {} tasks to `href_`.'.format(len(href_)))
    # 没有video_id的所有任务写入redis_task_key
    if len(task_) > 0:
        task_df = [json.dumps(i) for i in task_]
        # redisClient.delete(redis_task_key)
        redisClient.sadd(redis_task_key, *task_df)
        print('add {} tasks to `{}`.'.format(len(task_df), redis_task_key))
    # 有video_id的所有任务写入redis_href_key
    if len(href_) > 0:
        href_df = [json.dumps(i) for i in href_]
        redisClient.sadd(redis_href_key, *href_df)
        print('add {} tasks to `{}`.'.format(len(href_df), redis_href_key))


def search_view_by_name(driver, item):
    # 先搜歌手+歌曲
    if 'video_id' not in item and 'search_view' not in item:
        item['version'] = item['version'] if item['version'] else "official"
        driver.get('https://music.youtube.com/search?q={}+{}+{}'.format(
            item['artist_name'].replace('&', ' and '),
            item['song_name'].replace('&', ' and '),
            item['version'].replace('&', ' and ')
        ))
    # 再搜歌曲+歌手
    else:
        item['version'] = item['version'] if item['version'] else "official"
        driver.get('https://music.youtube.com/search?q={}+{}+{}'.format(
            item['song_name'].replace('&', ' and '),
            item['artist_name'].replace('&', ' and '),
            item['version'].replace('&', ' and ')
        ))
    element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//yt-formatted-string[text()='Top result']|//yt-formatted-string[text()='No results found']"))
    )
    # 无搜索结果
    if element.text == 'No results found':
        item['youtube_title'] = 'No results found'
        item['youtube_channel'] = 'No results found'
        item['video_id'] = '-'
        item['search_type'] = 'No'
        item['search_view'] = -9
        return item
    # # 最佳匹配结果
    # 歌曲标题及链接
    track_info = driver.find_element_by_xpath('.//div[@class="metadata-container style-scope ytmusic-card-shelf-renderer"]/yt-formatted-string/a')
    # # 用来暂存本次抓取结果, 用于后面判断是否需要覆盖上次抓取结果
    value_item = {"youtube_title": track_info.get_attribute("text")}
    video_id = track_info.get_attribute("href")
    value_item['video_id'] = video_id.split('?v=')[-1].split('&')[0]

    # 歌曲类型/channel/播放量
    track_info_type = driver.find_element(
        By.XPATH,
        './/div[@class="subtitle-container style-scope ytmusic-card-shelf-renderer"]/yt-formatted-string'
        )
    title = track_info_type.get_attribute('title')
    value_item['youtube_channel'] = title.split('•')[1].strip()
    type_view = title.split('•')[0].strip()
    # 视频时, 解析其id
    if type_view == 'Video':
        top_view = re.search(r'•(.+?)views', title)
        top_view = top_view and top_view[1] or '0'
        top_view = top_view.split('•')[-1].strip()

        if 'K' in top_view:
            top_view = int(float(top_view[:-1]) * 1000)
        elif 'M' in top_view:
            top_view = int(float(top_view[:-1]) * 1000000)
        elif 'B' in top_view:
            top_view = int(float(top_view[:-1]) * 1000000000)
        else:
            try:
                top_view = int(top_view)
            except:
                top_view = 0
        value_item['search_view'] = top_view
        # 没有view字段时, 说明这是第一次抓取, 给个-999特殊值标记一下
        view = item.get('search_view', -999)
        # 本次搜索播放量＞上次搜索播放量时, 用本次抓取结果覆盖上次抓取结果
        # 第一次抓取时, 用本次抓取结果填充
        if top_view >= view:
            item.update(value_item)
            item['search_type'] = 'video'
    elif type_view == 'Song':
        # 抓到歌曲, 且没有search_view, 用本次结果填充
        if item.get('search_view', -999) == -999:
            item.update(value_item)
            item['search_type'] = 'song'
    else:
        item.update(value_item)
        item['search_view'] = -1
        item['search_type'] = type_view.lower()
    return item


def main(type_='name'):
    while True:
        song = redisClient.spop(redis_task_key)
        if not song:
            print('end')
            break
        item = json.loads(song.decode())
        try:
            if type_ == 'name':
                item = search_view_by_name(driver, item=item)
                if item.get('search_view', -1) != -1:
                    item = search_view_by_name(driver, item=item)
            else:
                break
        except Exception as e:
            print(song, e)
        print(item)
        redisClient.sadd(redis_href_key, json.dumps(item))


if __name__ == '__main__':
    add_task(task_file, type_=crawl_type, task_sheet_name=sheet_name)

    driver, wait = get_driver()
    try:
        main(type_=crawl_type)
    finally:
        driver.close()
        driver.quit()

