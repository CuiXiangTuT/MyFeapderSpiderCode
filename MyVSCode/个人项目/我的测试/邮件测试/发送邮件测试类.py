import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

class SendEmail:
    def __init__(self,host,port,user,password):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.smtp = smtplib.SMTP()
        # 链接指定服务器
        self.smtp.connect(host=self.__host,port=self.__port)
        # 登陆，需要登陆邮箱和授权密码
        self.smtp.login(user=self.__user, password=self.__password)
    
    def send_message(self, content, subtype, charset=None, from_addr=None, to_addrs=None,header_text=None):
        # 构造MIMEText对象，参数为：正文，MIME的subtype，编码方式
        self.message= MIMEMultipart()
        self.message.attach(MIMEText(content, subtype, charset))# 正文内容   plain代表纯文本,html代表支持html文本
        # self.message = MIMEText(content,subtype, charset)
        self.message["From"] = Header(from_addr) # 可自定义
        if isinstance(to_addrs, list):
            to_addrs_str = ','.join(to_addrs)
        else:
            to_addrs_str = to_addrs
        self.message["To"] = Header(to_addrs_str)
        self.message['Subject'] = Header(header_text, 'utf-8') 
        self.smtp.sendmail(from_addr=from_addr, to_addrs=to_addrs_str, msg=self.message.as_string())


if __name__ == "__main__":
    SendEmail(host="smtp.163.com", port=25, user="CuiXiang_1024@163.com", password="OYUXFNMVRYNIJYTP").send_message(content="""<h1 style="color:red">仅用于测试</h1>""",subtype='html',charset='utf-8',from_addr=
    "CuiXiang_1024@163.com",to_addrs=["CuiXiang_1024@163.com","1123244374@qq.com"],header_text="每日热榜数据测试")
