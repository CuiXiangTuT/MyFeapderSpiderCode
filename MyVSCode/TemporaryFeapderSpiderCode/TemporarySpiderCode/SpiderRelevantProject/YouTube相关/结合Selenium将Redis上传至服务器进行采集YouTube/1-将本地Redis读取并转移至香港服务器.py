import redis
import xlrd
import pandas
import os

def local_redis_to_excel(redis_key,excel_name):
    if os.path.isfile(excel_name):
        os.remove(excel_name)
        print("文件已存在，删除文件成功")
    rd = redis.Redis(host='192.168.10.135',port=6379,db=10,password='123456',decode_responses=True)
    result = rd.smembers(redis_key)
    df = pandas.DataFrame(result)
    df.to_excel(excel_name)

def transfer_info_to_hk_redis(redis_key,excel_name):
    """
    将本地生成的Excel传输数据至香港Redis服务器上
    """
    #创建book对象
    book = xlrd.open_workbook(excel_name)
    sheet = book.sheet_by_index(0) # 打开第1个sheet
    # IP='服务器地址'
    # PORT=端口号
    #连接redis
    rd = redis.Redis(host='8.218.99.123',port=6379,db=10,password='GMG.redis',decode_responses=True)
    #把excel行数复制给cols
    cols = sheet.nrows
    for i in range(1,cols):         #根据行数循环插入
        result = sheet.row_values(i)   #获取第i行数据是一个列表
        for j in range(1,len(result)): #获取列表长度，从第二个数据开始写入值
            # rd.rpush(resault[0], resault[j])    #第0个数据作为键名
            # rd.sadd("youtube_view_spider:href:searchyoutubetrack20230404", resault[j])
            rd.sadd(redis_key, result[j])
            print(f'正在插入第{result[0]}的第{j}个数据')

if __name__=='__main__':
    redis_key = 'youtube_view_spider:href:searchyoutubeinfo20230920'
    excel_name = './MyFile/youtube_search_data.xlsx'
    local_redis_to_excel(redis_key=redis_key,excel_name=excel_name)
    transfer_info_to_hk_redis(redis_key=redis_key,excel_name=excel_name)
