#########################################################################
# File Name: zabbix_sendEmail.sh
# Author: kerncai
# mail: kernkerncai@gmail.com
# Created Time: 2014年02月17日 星期一 13时47分15秒
#########################################################################
#!/bin/bash

HOST=`echo $2 |grep -oE "[a-zA-Z]+[0-9]{2}-[0-9]{3}"`
mail=`mysql -uroot -proot -hip ops_db -e"select '$HOST',email from user where id = (select user_id from item where label = '$HOST') union select '$HOST',email from user where id = (select owner_id from item where label = '$HOST')"|grep -vE 'label|email' |awk '{print$2 }'`

/usr/local/bin/sendEmail -f zabbix@idc10_`date +%d%H%M`.com  -t $mail,$1 -u $2 -m "$3\npost time `date |awk '{print$4}'`" -s 10.10.6.209


