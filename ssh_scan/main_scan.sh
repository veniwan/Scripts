#!/bin/bash
#cmdfiles.ini远程执行命令组，hosts.ini格式为：电信ip 密码 平台

>run.log

for i in `awk '{print $1}' hosts.ini`
do
    sed -i "/$i ssh-rsa/d"  /root/.ssh/known_hosts 

done

echo -e "\033[33m正在获取远程信息(ret.ini)\033[0m"

while read line
do
  server=`echo $line |awk '{print $1}'`
  passwd=`echo $line |awk '{print $2}'`
  cmdfile="cmdfiles.ini"
  if ncat $server 22 <<< "EOF"  &> /dev/null; then
    sed -ri "/^spawn/s/([^0-9]+)[0-9]+/\122/" expect-run.exp
  elif ncat $server 2222 <<< "EOF"  &> /dev/null; then
    sed -ri "/^spawn/s/([^0-9]+)[0-9]+/\12222/" expect-run.exp
  else
    echo -e "\033[33m$server ssh端口是啥，填入脚本此处下行，取消注释！\033[0m"
    #sed -ri "/^spawn/s/([^0-9]+)[0-9]+/\1${whatport}/" expect-run.exp
    exit 1
  fi
  
  ./expect-run.exp $server $passwd  $cmdfile 
#增加roles.csv文件
  (($?==0)) && echo $passwd >> run.log || exit
  plat=`echo $line |awk '{print $3}'`
  (($?==0)) && echo $plat >> run.log || exit
done < hosts.ini &> /dev/null

egrep -v  "root|logout|Connect|Last|Warning|exit"  run.log > ret.ini 
#脚本运行完后用于提取有用信息

#egrep   "^[1-9]"  run.log > ip.ini 
#脚本运行完后用于提取有用信息

echo -e "\033[32m生成资源导入列表(res.ini)\033[0m"
/usr/local/python27/bin/python printHostRes.py 
echo -e "\033[32m生成装服文件列表(roles.csv)\033[0m"
