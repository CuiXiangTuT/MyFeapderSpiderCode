import redis
import xlrd
#创建book对象
book = xlrd.open_workbook(r'./youtube_info.xlsx')
sheet = book.sheet_by_index(0) # 打开第1个sheet
# IP='服务器地址'
# PORT=端口号
#连接redis
# rd = redis.Redis(host='8.218.99.123',port=6379,db=10,password='GMG.redis',decode_responses=True)
#把excel行数复制给cols
cols = sheet.nrows
print(cols)
print(sheet.row_values(cols-1))
# for i in range(0,cols):         #根据行数循环插入
#     print(sheet.row_values(i))
#     break
    # resault = sheet.row_values(i)   #获取第i行数据是一个列表
    # for j in range(1,len(resault)): #获取列表长度，从第二个数据开始写入值
    #     # rd.rpush(resault[0], resault[j])    #第0个数据作为键名
    #     rd.sadd("youtube_view_spider:href:searchyoutubetrack20230404", resault[j])
    #     print(f'正在插入第{resault[0]}的第{j}个数据')