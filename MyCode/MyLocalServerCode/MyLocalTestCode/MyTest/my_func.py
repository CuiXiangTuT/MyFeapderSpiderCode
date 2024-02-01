from datetime import datetime

# 输入的字符串
s = "Joined Oct 29, 2019"

# 使用字符串处理方法提取日期部分
date_string = s.replace("Joined ", "")

# 使用datetime库解析日期字符串
date = datetime.strptime(date_string, "%b %d, %Y")

# 将日期转换为指定格式
formatted_date = date.strftime("%Y-%m-%d")

print(formatted_date)