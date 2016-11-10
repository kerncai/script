#!/usr/bin/env python
#-- coding:utf-8-
import urllib2
import os,sys
import datetime,time
import chardet
import xml.dom.minidom
import smtplib
import format_datetime
from email.mime.text import MIMEText
from pyh import *

reload(sys)  
sys.setdefaultencoding('utf8')
imdays = ['09','10','11','12','13','14','15'] #日期
start = datetime.datetime(2007, 9,18,21,00) #相恋开始日期
now = datetime.datetime.now()
end  = now - start
days = str(end).split()[0]
hours = str(end).split()[2].split(':')[0]
mins = str(end).split()[2].split(':')[1]
friends = "%s 天 %s 小时 %s 分" %(days,hours,mins)
class run:
    def __init__(self):
        self.city = "上海"
        self.host = 'smtp.qq.com'
        self.sender = 'xxxx@qq.com'
        self.pwd = 'mdmjyvikuxqnbijf'
        self.port = '465'

    def getday(self):
	#获取天数
        today = datetime.date.today()
        CaDay = str(today).split('-')[-1]
        if int(CaDay) <= int('09'):
            formattime = format_datetime.get_today_month(0)
        else:
            formattime = format_datetime.get_today_month(1)
        month = formattime.split('-')[1]
        year = formattime.split('-')[0]
        newday = "%s-%s-09" %(year,month)
        date_newday = datetime.datetime.strptime(newday,'%Y-%m-%d')
        diff = date_newday - now
        tnums =  str(diff).split()[0]
        if CaDay in imdays:
            importdays = int(CaDay) - int('09')
            pre = str(importdays/float(7)*100)[:5]
            womendays = '888'
            print (importdays,pre,womendays)
            return (importdays,pre,womendays)
        else:
            return tnums

    def sendmail(self,receiver,title,body):
	#格式化邮件
        msg = MIMEText(body, 'html','utf-8')
        msg['subject'] = title
        msg['from'] = self.sender
        msg['To'] = ','.join(receiver)
        try:  
            s = smtplib.SMTP_SSL(self.host,self.port)
            s.login(self.sender, self.pwd)
            s.sendmail(self.sender, receiver, msg.as_string())
            print 'The mail named %s to %s is sended successly.' % (title, receiver)
        except Exception,e:
            print "失败："+str(e)
    
    def weather(self):
	#获取天气信息
        unicodeData = self.city.decode("UTF-8")
        gbkData = unicodeData.encode("gbk")
        format_city = repr(gbkData).replace("\\x","%").upper().split("'")[1]
        url = ('http://php.weather.sina.com.cn/xml.php?city=%s&password=DJOYnieT8234jlsK&day=0') %format_city
        print url
        centent = urllib2.urlopen(url).read()
        doc = xml.dom.minidom.parseString(centent)
        root = doc.documentElement
        morning = root.getElementsByTagName('status1')[0].firstChild.data
        night = root.getElementsByTagName('status2')[0].firstChild.data
        morning_wind = root.getElementsByTagName('direction1')[0].firstChild.data
        night_wind = root.getElementsByTagName('direction2')[0].firstChild.data
        moining_temperature = root.getElementsByTagName('temperature1')[0].firstChild.data
        night_temperature = root.getElementsByTagName('temperature2')[0].firstChild.data
        chy_shuoming = root.getElementsByTagName('chy_shuoming')[0].firstChild.data
        weatherNotion = root.getElementsByTagName('yd_s')[0].firstChild.data
        update = root.getElementsByTagName('udatetime')[0].firstChild.data
        
        a = '早上好！MissXXX'
        k = '这是第 %s' %friends
        if len(list(self.getday())) > 2:
            h = '大姨妈进行中，当前已完成%s 天，受难期为7天，完成度%s%%' %(self.getday()[0],self.getday()[1])
        else:
            h = '距离下次大姨妈还有 %s 天' %self.getday()
        b = '白天天气: %s, 晚上天气: %s ' %(morning,night)
        c = '白天风向: %s, 晚上风向：%s' %(morning_wind,night_wind)
        d = '白天温度: %s 摄氏度, 晚上温度: %s 摄氏度 '%(moining_temperature,night_temperature)
        e = '适宜穿着: %s' %chy_shuoming
        f = '当日提醒: %s '%weatherNotion
        g = '掐指一算时间: %s '%update
        page = PyH("test")
        page<<div(style="background-color: #9999FF")
        page <<h3(a)
        page <<p(k)
        page <<p(h)
        page <<p(b)
        page <<p(c)
        page <<p(d)
        page <<p(e)
        page <<p(f)
        #page <<p(g)
        page.printOut('/usr/local/scripts/can/test.html')
if __name__=='__main__':
    RUN = run()
    RUN.weather()
    RUN.getday()
    body = open('/usr/local/scripts/can/test.html').read()
    print body
    receiver = ['邮箱地址，列表形式，以逗号隔开']
    title = '来自X先生的爱心提醒'
    RUN.sendmail(receiver,title,body)
    del RUN
