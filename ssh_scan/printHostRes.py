#!/usr/bin/env python
#coding=utf-8
#desc:生成资源导入列表
import sys
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

res = dict()
pas = dict()
with open('cmdfiles.ini') as cmdfile:
    rowNum = len(cmdfile.readlines()) + 2 #+1是增加了roles.csv,+2是增加平台信息
with open('ret.ini') as resfile:
    content = resfile.readlines()
    conline = len(content)
    for i in range(1,conline/rowNum+1)[::-1]:
        line = content[conline-rowNum*i+1:conline-rowNum*(i-1)]
        line = "".join(j for j in line).splitlines()
        ip1, ip2, ip3 = line[0], line[1], line[2]
        ip3 = "0" if ip2 == ip3 else ip3
        cpu = "E"+line[3].split('-')[1]
        disk = line[4].split('-')[1].strip(' G')
        disk = "600G" if int(disk) > 500 else "300G" 
        mem = int(line[5].split(':')[1].strip())
        if mem < 40:
        	mem = "32G"
        elif 40 < mem < 55:
        	mem = "48G"
        elif 55 < mem < 70:
        	mem = "64G"
        else: 
            mem = "128G"
        url = "http://ip.taobao.com/service/getIpInfo.php?ip={ip}".format(ip=ip1)
        city = requests.get(url,timeout=60).json()['data']['city'].strip('市')
        city = "xx" if city == "xxx" else city
        city = "xx" if city == "xxx" else city
        pwd = line[7] #多一项是roles.csv的密码字段
        plat = line[8] #多一项是roles.csv的平台字段
        temp = " ".join(str(i) for i in [ip1,ip2,ip3,cpu,mem,disk,city])
        temp2 = ",".join(str(i) for i in [ip1,ip2,pwd,city,plat])
        res[ip1] = "mir " + plat + " 游戏服[预留] " + temp + " GMT+8"
        pas[ip1] = temp2
#资源中心列表
with open('res.ini','w') as rf1:
    for ret in res.values():
        rf1.write(ret+"\n")
#roles.csv    
with open('roles.csv','wb') as rf2:
    for ret2 in pas.values():
        rf2.write(ret2+"\n")
