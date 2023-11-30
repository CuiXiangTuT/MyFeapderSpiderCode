# # -*- coding: utf-8 -*-

# # Sample Python code for youtube.search.list
# # See instructions for running these code samples locally:
# # https://developers.google.com/explorer-help/code-samples#python

# import os

# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors

# scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# def main():
#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "AIzaSyB2NA5XjF2My7xva4xvcwwThSPSdyjla84"

#     api_service_name = "youtube"
#     api_version = "v3"
#     client_secrets_file = "D:\\Program Files (x86)\\YouTubeAPI\\steel-index-381906-c21050f178f2.json"

#     # Get credentials and create an API client
#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         client_secrets_file, scopes)
#     credentials = flow.run_console()
#     youtube = googleapiclient.discovery.build(
#         api_service_name, api_version, credentials=credentials)

#     request = youtube.search().list(
#         part="snippet",
#         q="destiny black sherif"
#     )
#     response = request.execute()

#     print(response)

# if __name__ == "__main__":
# #     main()
# l = [('116593112'),('68495054'),('65720674'),('68495053'),('75855763'),('92977948'),('116593106'),('53618325'),('92981460'),('68495051'),('74718000'),('41202842'),('116588110'),('47116867'),('68499829'),('92977974'),('115321112'),('116588111'),('68499826'),('92981438'),('93703003'),('116593107'),('12283793'),('20306980'),('42120139'),('47116870'),('92981458'),('112895071'),('115321111'),('12371402'),('47606840'),('92981441'),('93702997'),('116588105'),('12371367'),('9139412'),('38223939'),('9139485'),('9131651'),('65348148'),('9136374'),('9136503'),('65348161'),('9139411'),('9136458'),('9136479'),('9136308'),('9136316'),('9139408'),('9149066'),('119131141'),('112895072'),('12283789'),('115316780'),('119085243'),('115271968'),('115083662'),('115083670'),('111802860'),('115316778'),('12371384'),('98325903'),('19872511'),('19872904'),('9136460'),('20217046'),('9150328'),('20218055'),('61193144'),('38295872'),('9140694'),('19340950'),('38295637'),('38295453'),('61196838'),('19342920'),('19342929'),('9140698'),('19342960'),('38294367'),('9136464'),('19309207'),('19325896'),('9151246'),('19325867'),('60603754'),('19325913'),('9151248'),('9150240'),('20218389'),('60591749'),('9136372'),('9136502'),('20218323'),('61818340'),('9149173'),('9136497'),('20218637'),('60595389'),('9155307'),('60050061'),('9155119'),('60005226'),('60005689'),('9149175'),('22469990'),('5015143'),('116593129'),('41202872'),('116381939'),('12283786'),('5131828'),('5131829'),('7567339'),('7567340'),('92981456'),('115321109'),('5225102'),('38294368'),('20218643'),('6150665'),('60598700'),('60600082'),('38295631'),('5225110'),('20218361'),('6152013'),('38295122'),('53803880'),('78902300'),('53803881'),('53799578'),('89554386'),('53799579'),('54131855'),('81086529'),('44705055')]
# print(l)

import requests
import json,re


url = "https://www.youtube.com/watch?v=cMPEd8m79Hw"
headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

}

response = requests.get(url,headers)
res = response.text
youtube_video_link_info_batch_item = dict()
if 'likeCount' in res or 'viewCount' in res:
    view_count = re.findall(r'\"viewCount\":\"(.*?)\"', res)[0]
    title = re.findall(r'\"title\":\"(.*?)\"', res)[0]
    json_str = re.findall(r'\"videoOwnerRenderer\":(.*?)\]\},\"subscriptionButton\"', res)[0].split('"runs":')[
                    1][1:]

    json_data = json.loads(json_str)
    channel_name = json_data["text"]
    channel_id = json_data["navigationEndpoint"]["browseEndpoint"]["browseId"]
    # youtube_video_link_info_batch_item['youtube_link'] = request.task_youtube_video_link
    youtube_video_link_info_batch_item['youtube_title'] = title
    youtube_video_link_info_batch_item['youtube_channel_id'] = channel_id
    youtube_video_link_info_batch_item['youtube_channel_name'] = channel_name
    youtube_video_link_info_batch_item['youtube_views'] = view_count
    # youtube_video_link_info_batch_item['batch'] = self.batch_date
    print(youtube_video_link_info_batch_item)