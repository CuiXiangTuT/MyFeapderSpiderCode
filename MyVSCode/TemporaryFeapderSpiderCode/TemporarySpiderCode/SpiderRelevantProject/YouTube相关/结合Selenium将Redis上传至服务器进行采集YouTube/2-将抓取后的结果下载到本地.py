import redis
import xlrd
import pandas
import os
import json

def download_hk_redis_to_excel(redis_key,excel_name):
    if os.path.isfile(excel_name):
        os.remove(excel_name)
        print("文件已存在，删除文件成功")
    rd = redis.Redis(host='8.218.99.123',port=6379,db=10,password='GMG.redis',decode_responses=True)
    result = rd.smembers(redis_key)
    df = pandas.DataFrame(result)
    df.to_excel(excel_name)
    return True

def updata_excel_data(excel_name):
    book = xlrd.open_workbook(excel_name)
    sheet = book.sheet_by_index(0)
    cols = sheet.nrows
    data = list()
    for i in range(1,cols):         #根据行数循环插入
        result = json.loads(sheet.row_values(i)[1])
        data.append(result)
    df = pandas.DataFrame(data)
    df.to_excel('./MyFile/searchyoutubeinfo20230920.xlsx')

if __name__ == "__main__":
    redis_key = 'youtube_view_spider:view:searchyoutubeinfo20230920'
    excel_name = './MyFile/down_load_data.xlsx'
    isFlag = download_hk_redis_to_excel(redis_key,excel_name)
    if isFlag:
        updata_excel_data(excel_name=excel_name)

