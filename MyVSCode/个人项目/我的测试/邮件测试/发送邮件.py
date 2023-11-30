import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_emailMessage():
    # 创建 SMTP 对象
    smtp = smtplib.SMTP()
    # 连接（connect）指定服务器
    smtp.connect(host="smtp.163.com", port=25)
    # 登录，需要：登录邮箱和授权码
    smtp.login(user="CuiXiang_1024@163.com", password="OODQGPYCAGJFNAMP")
    message = MIMEText('数据一致，无需操作', 'plain', 'utf-8')
    message['From'] = Header("CuiXiang_1024@163.com")  # 发件人的昵称
    message['To'] = Header("CuiXiang_1024@163.com,1123244374@qq.com")  # 收件人的昵称
    message['Subject'] = Header('每日监控数据情况报告', 'utf-8')  # 定义主题内容
    print(message)
    smtp.sendmail(from_addr="CuiXiang_1024@163.com", to_addrs="CuiXiang_1024@163.com,1123244374@qq.com", msg=message.as_string())

if __name__=='__main__':
    send_emailMessage()