#!/bin/bash
# auto add evil detect ip by ipset
# 简单探测：以php为特征，单日超过150次请求加入黑名单
# */10 * * * * sh /data/code/detect_evil_ip.sh &> /dev/null
# 日志轮询
# 1 0 * * * sh /data/code/detect_evil_ip.sh rotate &> /dev/null
# chmod +x  /etc/rc.d/rc.local 
# [ -f /etc/sysconfig/ipset ] && /usr/sbin/ipset -! restore < /etc/sysconfig/ipset
# /usr/sbin/service iptables restart

NOWDATE=`/usr/bin/date +%F`
LOGPATH=/data/xiaowanzi/logs/uwsgi.log

IPS=`/usr/bin/cat $LOGPATH | /bin/grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | /bin/sort | /usr/bin/uniq  -c | /usr/bin/awk '$1>150{print $2}'`

/bin/grep -q blacklist /etc/sysconfig/iptables || \
/usr/sbin/iptables -A INPUT -p tcp -m set --match-set blacklist src -j DROP
/usr/sbin/ipset create blacklist hash:ip
for ip in $IPS
do
   /bin/grep "$ip" $LOGPATH | /bin/grep -q 'php' && \
       /usr/sbin/ipset add blacklist $ip
done
/usr/sbin/ipset save > /etc/sysconfig/ipset
/usr/sbin/service iptables save

if [ "$1" = "rotate" ]; then
    /bin/cp -f $LOGPATH{,.$NOWDATE}
    > $LOGPATH
fi
