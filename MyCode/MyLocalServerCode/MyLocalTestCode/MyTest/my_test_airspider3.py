import feapder
# from feapder import ArgumentParser
import time
from feapder.utils.webdriver import WebDriver
from selenium.webdriver.common.by import By


class MyTestAirspider3(feapder.AirSpider):

    def start_requests(self):
        # 'youtube_music_channel_id','youtube_music_album_single_playlist_url'
        task_id = 1
        task_youtube_music_channel_id = "UCL2MDNdwEtV6aYUgNjFQGZA"
        task_youtube_music_album_single_playlist_url = "https://music.youtube.com/channel/MPADUCL2MDNdwEtV6aYUgNjFQGZA"
        yield feapder.Request(url=task_youtube_music_album_single_playlist_url,
        render=True,
        task_id=task_id,
        task_youtube_music_channel_id=task_youtube_music_channel_id,
        task_youtube_music_album_single_playlist_url=task_youtube_music_album_single_playlist_url
        )

    def parse(self, request, response):
        browser: WebDriver = response.browser
        js = "window.scrollTo(0, document.body.scrollHeight)"
        browser.execute_script(js)
        time.sleep(4)

        playlist_list = browser.find_elements(By.XPATH,'//ytmusic-two-row-item-renderer[@aspect-ratio="MUSIC_TWO_ROW_ITEM_THUMBNAIL_ASPECT_RATIO_SQUARE"]/a')
        for i in playlist_list:
            # 获取的值为重定向前的URL
            pre_redirect_url = i.get_attribute('href')
            title = i.get_attribute('title')

            yield feapder.Request(
                url=pre_redirect_url,
                render=True,
                title=title,
                pre_redirect_url=pre_redirect_url,
                callback=self.parse_redirect,
                task_gmg_artist_id=request.task_gmg_artist_id,
                youtube_music_albums_singles_id=request.youtube_music_albums_singles_id,
                task_youtube_music_channel_id = request.task_youtube_music_channel_id,
                task_youtube_music_album_single_playlist_url = request.task_youtube_music_album_single_playlist_url
            )
            
        # yield self.update_task_batch(request.task_id, 1)
    
    def parse_redirect(self,request,response):
        browser1: WebDriver = response.browser
        current_url = browser1.current_url

        youtube_music_albums_singles_data_item = dict()
        youtube_music_albums_singles_data_item["gmg_artist_id"] = request.task_gmg_artist_id
        youtube_music_albums_singles_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
        youtube_music_albums_singles_data_item["youtube_music_albums_singles_id"] = request.task_youtube_music_albums_singles_id
        youtube_music_albums_singles_data_item['youtube_music_albums_singles_url'] = request.task_youtube_music_albums_singles_url
        youtube_music_albums_singles_data_item["title"] = request.title
        youtube_music_albums_singles_data_item['youtube_music_album_single_url_pre_redirect'] = request.task_youtube_music_albums_singles_url
        youtube_music_albums_singles_data_item['youtube_music_albums_singles_url_after_redirect'] = current_url
        # youtube_music_albums_singles_data_item["batch"] = self.batch_date

        youtube_music_artist_plate_batch_task_item = dict()
        youtube_music_artist_plate_batch_task_item['gmg_artist_id'] = request.task_gmg_artist_id
        youtube_music_artist_plate_batch_task_item['youtube_music_channel_id'] = request.task_youtube_music_channel_id
        youtube_music_artist_plate_batch_task_item["youtube_music_playlist_id"] = current_url.split("?list=")[1]
        youtube_music_artist_plate_batch_task_item["youtube_music_playlist_url"] = current_url
        youtube_music_artist_plate_batch_task_item["youtube_music_playe_remark"] = "Albums/Singles"

        print(youtube_music_albums_singles_data_item)
        print(youtube_music_artist_plate_batch_task_item)


if __name__ == "__main__":
    MyTestAirspider3().start()