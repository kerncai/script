#!/usr/bin/python
# -*- coding: utf-8 -*-

import cookielib
import urllib
import urllib2

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

data = {'action': 'login', 'login_username': 'admin', 'login_password': 'admin_ops'}
f = opener.open('http://cacti10.corp.com/index.php', urllib.urlencode(data))
f.close()


d = f = opener.open('http://cacti10.corp.com/graph_image.php?action=view&local_graph_id=2988&rra_id=2')

h = f = opener.open('http://cacti10.corp.com/graph_image.php?action=view&local_graph_id=4866&rra_id=2')

with open('/home/kern-cai/log/zabbix20.15e.com/网通出口流量.png','w') as w:
    w.write(d.read())
d.close()

with open('/home/kern-cai/log/zabbix20.15.com/电信出口流量.png', 'w') as w:
    w.write(h.read())
h.close()
