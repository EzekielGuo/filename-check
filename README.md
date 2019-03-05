# filename-check
检查文件夹中的文件，与数据库中的文件名核对缺少则告出邮件


##以文字形式发送邮件
msg = MIMEText(content_info, 'plain', 'utf-8')
##以html形式发送邮件
msg = MIMEText(content_info, 'html', 'utf-8')
