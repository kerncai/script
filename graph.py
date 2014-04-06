# -*- coding: utf-8 -*-

import re
from pyzabbix import ZabbixAPI

def main():
    
    host = '10.20.2.1'

    zapi = ZabbixAPI('http://zabbix20.corp.test.com')
    zapi.login('root', 'root')

#    ptrn_target = re.compile('if(In|Out)Octets\[(Ten-)?GigabitEthernet([0-9]+/[0-9]+/[0-9]+/[0-9]+)\]')
#    ptrn_target = re.compile('if(In|Out)Octets\[ethernet([0-9]+/[0-9]+)\]')
    ptrn_target = re.compile('if(In|Out)Octets\[GigabitEthernet([0-9]+/[0-9]+/[0-9]+/[0-9]+)\]')
     

    items = zapi.item.get(host=host,
                 search={'key_': ['ifInOctets', 'ifOutOctets']},
                 startSearch=True,
                 output=['key_'])
        
    if_in = {}
    if_out = {}
    for item in items:
        mo_target = ptrn_target.match(item['key_'])
        if mo_target is None:
            continue
        if mo_target.group(1) == 'In':
            if_in[mo_target.group(2)] = item['itemid']
#            print item['itemid']
            
        elif mo_target.group(1) == 'Out':
            if_out[mo_target.group(2)] = item['itemid']
#            print item['itemid']
#    print if_in
    ptrn_source = re.compile('GE([0-9]+/[0-9]+/[0-9]+/[0-9]+)\s+(.*)')
#    ptrn_source = re.compile('Gi([0-9]+/[0-9]+/[0-9]+)\s+(.*)')
#    ptrn_source = re.compile('ethernet([0-9]+/[0-9]+)\s+(.*)')



    with open('IDC10-3750-1') as f:
        for l in f:
            mo_source = ptrn_source.match(l)
            if mo_source is None:
                continue

            port = mo_source.group(1)
            a = mo_source.group(0)
            b = mo_source.group(2)
        
        


            if port not in if_in or port not in if_out:
                print 'port %s not found' % port 
                continue
               
            title = '*%s (GE%s)' % (mo_source.group(2), port)


            print title

            graphs = zapi.graph.get(filter={'host': host,
                                            'name': title})

            if graphs:
                print 'graph %s exists' % title
                continue

            result =zapi.graph.create(name=title, width=900, height=200,
                        gitems=[{
                            'itemid': if_in[port],
                            'color': '00AA00',
                            'drawtype': 5,
                            'yaxisside': 0,
                            'sortorder': 0
                           },{
                            'itemid': if_out[port],
                            'color': '3333FF',
                            'drawtype': 5,
                            'yaxisside': 0,
                            'sortorder': 1
                           }])
            print 'create %s %s' % (result['graphids'][0], title)


if __name__ == '__main__':
    main()
