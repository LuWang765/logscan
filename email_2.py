import smtplib
from email.mime.text import MIMEText
from email.header import Header


mail_to_list = ['1424419913@qq.com', ]      #接收邮件地址
mail_user = '15122550163@163.com'                     #发送邮件地址
mail_user_psw = '******'                   #邮箱密码
mail_host = 'smtp.163.com'


def send_mail(sub):
    mail_from = 'hello' + '<' + mail_user + '>'
    #mail_to = 'me' + receiver
    message = MIMEText('How are you ?',_subtype='plain')
    message['From'] = Header(mail_from)
    message['To'] = Header(';'.join(mail_to_list))
    message['Subject'] = Header(sub)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host,25)
        smtp.login(mail_user, mail_user_psw)
        smtp.sendmail(mail_from, mail_to_list, message.as_string())
        smtp.close()
        print('OK!')
    except Exception as e:
        print(e)

#for i in mail_to_list:
send_mail('问候')