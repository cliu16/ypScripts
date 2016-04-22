#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host="smtp.gmail.com"  #设置服务器
mail_user="dingbaoxiechen@gmail.com"    #用户名
mail_pass="Jerry890213"   #口令


sender = 'lc890213@gmail.com'
receivers = ['lc890213@gmail.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

def sendMsg(subject, msg):
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("Raise Discount Alert", 'utf-8')
    message['To'] =  Header("Chen", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)    # 25 为 SMTP 端口号
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
        smtpObj.close()
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
