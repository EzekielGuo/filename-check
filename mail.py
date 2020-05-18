import os
import time
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


my_sender = 'xx@xx.com'  # 发件人邮箱账号
my_pass = 'xx'  # 发件人邮箱密码
my_user = 'xx@xx.com'  # 收件人邮箱账号，我这边发送给自己
my_user2 = 'xx@xx.com'  # 收件人邮箱账号，我这边发送给自己

# 邮件方法
def mail(content_info,titles):
    ret = True
    try:
        # msg = MIMEText(content_info, 'plain', 'utf-8')
        msg = MIMEText(content_info, 'plain', 'utf-8')
        msg['From'] = formataddr(["xxx", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["xxx", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = formataddr(["xxx", my_user2])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = titles  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP()
        server.connect("mail.xx.com", 25)
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user,my_user2,], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret



# 拼凑备份文件夹名称
localtime = time.localtime(time.time())
year_str = str(localtime[0])
month = localtime[1]
day = localtime[2]
month_str = ""
day_str = ""
if month < 10:
    month_str = "0" + str(month)
if day < 10:
    day_str = "0" + str(day)
table = year_str+"-"+month_str+"-"+day_str
# print(table)

# 获取已备份的设备列表
filename_list_actual = []
file_mem = os.popen("ls -l /home/backup/hbyw/{}".format(table))
file_mem_read = file_mem.read()
file_mem_read_split = file_mem_read.split("\n")
# print(file_mem_read_split)
for file in file_mem_read_split[1:-1]:
    file_split = file.split(" ")
    filename = file_split[-1]
    # print(filename)
    filename_list_actual.append(filename)
len_filename_list_actual = len(filename_list_actual)
print("filename_list_actual:{}".format(filename_list_actual))
print("len_filename_list_actual:{}".format(len_filename_list_actual))

# 获取总设备列表
filename_list_total = []
db = pymysql.connect("xx.xx.xx.xx", "username", "passwd", "dbname")
cursor = db.cursor()
sql = "select hostname from xx"
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    # print("results:{}".format(results))
    for row in results:
        row0 = row[0]
        # print(row0)
        filename_list_total.append(row0)
except:
    print("Error")
# 关闭数据库连接
db.close()
len_filename_list_total = len(filename_list_total)
print("filename_list_total:{}".format(filename_list_total))
print("len_filename_list_total:{}".format(len_filename_list_total))

# 已备份但未在设备列表中的设备
filename_list_extra = []
for filename_extra in filename_list_actual:
    if filename_extra not in filename_list_total:
        filename_list_extra.append(filename_extra)
len_filename_list_extra = len(filename_list_extra)
print("filename_list_extra:{}".format(filename_list_extra))
print("len_filename_list_extra:{}".format(len_filename_list_extra))

# 未备份设备列表
filename_list_missing = []
for filename_missing in filename_list_total:
    if filename_missing not in filename_list_actual:
        filename_list_missing.append(filename_missing)
len_filename_list_missing = len(filename_list_missing)
print("filename_list_missing:{}".format(filename_list_missing))
print("len_filename_list_missing:{}".format(len_filename_list_missing))


splitter = '\n'
content_missing = splitter.join(filename_list_missing)
# print(content_missing)
content_extra = splitter.join(filename_list_extra)
content_actual = splitter.join(filename_list_actual)

content = "********************  {} 配置备份统计  ********************\n" \
          "数据库中的设备总数：{}\n" \
          "已备份的设备数量：{}\n" \
          "已备份但设备名不存在于数据库中的设备数量：{}\n" \
          "未备份的设备数量：{}\n\n" \
          "----------未备份的设备名称----------\n" \
          "{}\n\n" \
          "----------已成功备份的设备名称----------\n" \
          "{}\n\n" \
          "----------已备份但设备名不存在于数据库中的设备名称----------\n" \
          "{}\n\n" \
          "" \
          "".format(table,
                    len_filename_list_total,
                    len_filename_list_actual,
                    len_filename_list_extra,
                    len_filename_list_missing,
                    content_missing,
                    content_actual,
                    content_extra,
                    )
print(content)

mail(content,"配置备份今日统计")


