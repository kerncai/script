#!/usr/bin/python

# -*- coding: utf-8 -*-

import json
import urllib2
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

data = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
        'user': 'admin',
        'password': 'zabbix'
    },
    'id': 1
}

req = urllib2.Request(url='http://10.20.3.234/api_jsonrpc.php',
                      data=json.dumps(data),
                      headers={'Content-Type': 'application/json-rpc'})
f = urllib2.urlopen(req)
token = json.loads(f.read())['result']
f.close()

req = urllib2.Request(url='http://zabbix20.corp.test/chart2.php?graphid=1615&period=604800&stime=20140604093337&updateProfile=1&profileIdx=web.screens&profileIdx2=1615&sid=b871042ffe1f18f8&width=1391&curtime=1370916306412',
                      headers={'Cookie': 'zbx_sessionid=%s' % token})
f = urllib2.urlopen(req)
img = f.read()
f.close()

msg = MIMEMultipart('related')
msg['Subject'] = 'Test Image'
msg['From'] = 'kaicai@test'
msg['To'] = 'kaicai@test'

msg.attach(MIMEText('Hi, <strong>Jerry</strong>!<br><img src="cid:img1">', 'html'))
mimg = MIMEImage(img, 'png')
mimg.add_header('Content-ID', '<img1>')
msg.attach(mimg)

s = smtplib.SMTP('mail.test')
s.login('root', 'root')
s.sendmail('kaicai@test', 'kaicai@test', msg.as_string())
s.quit()
