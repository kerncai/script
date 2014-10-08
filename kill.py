#!/usr/bin/env python
# -*- coding utf-8 -*-
# time :2014/10/8
# check the zombie and kill it
# kerncai
import os
import time
import datetime
import signal
import logging

nowtime = datetime.datetime.now()
process_name = ["DB","LOG"]
# log format
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='kill_pid.log',
                filemode='w')
def list():
    for i in process_name:
        check(i)

#check the DB or LOG processes
def check(sid):
    os.environ['sid']=str(sid)
    for line in os.popen("ps -eo user,comm,lstart,pid|grep -w $sid |grep -v grep"):
        a = ' '
        process = line.split()
        del process[0:3]
        process1 = process[0:4]
        pid = process[4]
        intpid = int(pid)
        gettime1 = a.join(process1)
        gettime = time.strptime(gettime1, '%b %d %X %Y')
        endtime = datetime.datetime(gettime[0],gettime[1],gettime[2],gettime[3],gettime[4],gettime[5],gettime[6])
        difftime = (nowtime - endtime).seconds
        strdiff = str(difftime)
        if difftime > 1080:
            os.kill(intpid,signal.SIGKILL)
            logging.warning('The process %s was killed' %pid)
            print 'The process %s was killed' %pid
        else:
            logging.info('The process %s has be running %s seconds' % (pid,strdiff))
            print 'The process %s has be running %s seconds' % (pid,strdiff)
if __name__ == "__main__":
    list()
