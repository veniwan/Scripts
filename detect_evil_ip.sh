#!/bin/bash
# auto add evil detect ip by ipset
# 简单探测：以php为特征，单日超过150次请求加入黑名单
# */10 * * * * sh /data/code/detect_evil_ip.sh &> /dev/null
# 1 0 * * * sh /data/code/detect_evil_ip.sh rotate &> /dev/null

NOWDATE=`date +%F`
LOGPATH=/data/xiaowanzi/logs/uwsgi.log

IPS=`cat $LOGPATH | /bin/grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | /bin/sort | /usr/bin/uniq  -c | awk '$1>150{print $2}'`

grep -q blacklist /etc/sysconfig/iptables || \
/usr/sbin/iptables -A INPUT -p tcp -m set --match-set blacklist src -j DROP
/usr/sbin/ipset create blacklist hash:ip
for ip in $IPS
do
   grep "$ip" $LOGPATH | grep -q 'php' && \
       /usr/sbin/ipset add blacklist $ip
done
/usr/sbin/ipset save > /etc/sysconfig/ipset
service iptables save

if [ "$1" = "rotate" ]; then
    /bin/cp -f $LOGPATH{,.$NOWDATE}
    > $LOGPATH
fi