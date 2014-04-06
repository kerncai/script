# -*- coding: utf-8 -*-

import os 
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

receivers = ['']
#receivers = ['kaicai@test.com']
source = '/home/kern-cai/log/zabbix20.corp.test.com/'


info = {
    'zabbix1.png':'呼兰机房到南汇一周机房专线流量',
    'zabbix2.png':'呼兰机房一周电信出口流量',
    'zabbix3.png':'南汇机房一周电信出口流量',
    'zabbix4.png':'南汇机房一周网通出口流量'
}


msg = MIMEMultipart('related')
msg['Subject'] = '一周关键流量图'
msg['From'] = 'monitor@char.com'
msg['To'] = ', '.join(receivers)

text = ''
mimgs = []
for i, filename in enumerate(os.listdir(source)):
    
    f = open('%s/%s' % (source, filename), 'r')
    img = f.read()
    f.close()
    text += '<div><h>%s</h><img src="cid:img%d"></div>' % (info.get(filename,''), i)    
#    text += '<div><h2>%s</h2><img src="cid:img%d"></div>' % (info.get(filename,''), i)
#    text += '<div><h2>%s</h2><img src="cid:img%d"></div>' % (info.get(filename, 'test'), i)
#    text += '<img src="cid:%s"><br>' % filename
#    mimg.add_header('Content-ID', '<%s>' % filename)
    mimg = MIMEImage(img, 'png')
    mimg.add_header('Content-ID', '<img%d>' % i)
    mimgs.append(mimg)
mtext = MIMEText('<h1>Hi, 上周关键流量图如下!</h1><br>' +text, 'html', _charset='utf-8')

#mtext = MIMEText('Hi, <strong>上周关键流量图如下</strong>!<br>' +text, 'html', _charset='utf-8')
msg.attach(mtext)

for mimg in mimgs:
    msg.attach(mimg)

s = smtplib.SMTP('smtp.101.com')
s.login('root', 'root')
s.sendmail('kaicai@test.com', receivers, msg.as_string())
s.quit()

