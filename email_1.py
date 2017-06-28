import smtplib
from email.mime.text import MIMEText
from email.header import Header
mail_to_list=['1424419913@qq.com']           #收件人(列表)
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址
mail_user="15122550163"                           #用户名
mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com


def send_mail(to_list,sub,content):
    me="<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = Header(sub)
    msg['From'] = Header(me)
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host,25)                            #连接服务器
        server.login("15122550163@163.com","wanglu135")    #登录操作,密码是授权码，而不是邮箱登录密码
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False
for i in range(1):                             #发送1封，上面的列表是几个人，这个就填几
    if send_mail(mail_to_list,"电话","电话是XXX辅导辅导辅导"):  #邮件主题和邮件内容
        #这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信
        print ("done!")