# filename-check
检查文件夹中的文件，与数据库中的文件名核对缺少则告出邮件

原理：

先获取文件服务器（A）上今日份的文件名列表，再在数据库（B）中获取总的文件名列表，进行核实，若文件名称存在于A而不存在于B，统计生成一个列表C，为extra列表，以供核实，若文件存在于B而不存在于A，统计生成一个列表D，为missing列表，是缺失的文件名称，然后每日定时发送邮件，以供核实





##以文字形式发送邮件

msg = MIMEText(content_info, 'plain', 'utf-8')


##以html形式发送邮件

msg = MIMEText(content_info, 'html', 'utf-8')
