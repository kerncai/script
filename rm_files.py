# -*- coding: utf-8 -*-

import os
import time
import datetime

path = "/home/kerncai/test/"


def filetime(filetimes):
    filetime1 = time.localtime(os.stat(filetimes).st_mtime)
    filetimenow = time.strftime("%Y-%m-%d",filetime1)
    return filetimenow

        
def getYesterday():  
    today=datetime.date.today()  
    oneday=datetime.timedelta(days=1)  
    yesterday=today-oneday   
    return yesterday


def getYesterday():  
    today=datetime.date.today()  
    twoday=datetime.timedelta(days=2)  
    bday=today-twoday   
    return bday


def endWith(s,*endstring):
    array = map(s.endswith,endstring)
    if True in array:
        return True
    else:
        return False

if __name__=='__main__':
    s = os.listdir(path)
    f_file = []
    for i in s:
        if endWith(i,'.dmp'):
            print filetime(i)
