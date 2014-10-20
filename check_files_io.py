#!/usr/bin/env python

import os
import random
import datetime
import threading
import logging
import signal

#import shutil
#
#shutil.rmtree
log_type = ["db","log"]
time_type = ["day","hour"]
choice_list = ["5","8"]
d1 = datetime.datetime.now()

def game_name(game,dirname):
    directory = "/home/kerncai/test/game%s/141020" %game
    if not os.path.exists(directory):
#os.makedirs(directory)
        print "mkdir %s" %directory
        for item in log_type:
            for line in time_type:
                file_directory = "%s/%s/%s" % (directory,item,line)
                for i in range(30):
                    chlist = random.choice(choice_list)
                    touch_cmd = "dd if=/dev/zero of=%s/log_%s/file_%s bs=1M count=%s" %(file_directory,dirname,i,chlist)
                    if os.path.exists(file_directory):
                        print touch_cmd
#                        os.system(touch_cmd)
                    else:
#                        os.makedirs(file_directory)
#                        os.system(touch_cmd)
                        print touch_cmd
    else:
        print "%s is exists,please rm -rfv it" % directory
class Mkdirfiles(threading.Thread):
    def __int__(self):
        threading.Thread.__int__(self)

    def run(self):
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='time.log',
                    filemode='w')
        for item in range(30):
            for i in range(18):
                game_name(item,i)
        d2 = datetime.datetime.now()
        diff = d2 - d1
        a = "The calculation is completed, consuming a total of %sS" %diff
        logging.info(a)
        for id in os.popen('ps -eo pid,comm,args|grep iostat|grep -v grep'):
            pid = id.split()[0]
            os.kill(int(pid),signal.SIGKILL)
        

class Iostatus(threading.Thread):
    def __int__(self):
        threading.Thread.__int__(self)

    def run(self):
        io_cmd = "iostat -d -k -x 1 > iostat_mkfiles.log"
        os.system(io_cmd)

if __name__ == "__main__":
    lock = threading.Lock()
    t = Mkdirfiles()
    t1 = Iostatus()
    t.start()
    t1.start()
    t.join()
#    t1.join()
