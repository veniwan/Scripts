#!py
#coding=utf-8
# 打包编译
#pyinstaller -F -c --icon=icon64.ico directory_size_sort.py

# 兼容win中文乱码
from __future__ import unicode_literals

import os
import sys
from collections import defaultdict
from prettytable import PrettyTable


file_size = {}
dir_size = defaultdict(list)

if len(sys.argv) == 1:
    dirname = '.'
    numbers = 10
elif len(sys.argv) == 2:
    dirname = sys.argv[1]
    numbers = 10
elif len(sys.argv) == 3:
    dirname = sys.argv[1]
    numbers = int(sys.argv[2])
else:
    print(u"用法：{0} 目录名 打印条数".format(__file__))
    print(u"===========任意键退出！============")
    raw_input()
    sys.exit(1)

if not os.path.isdir(dirname):
    print(u"目录:{0} 不存在".format(dirname))
    print(u"===========任意键退出！============")
    raw_input()
    sys.exit(1)

print(u"當前參數：目錄名{0}，顯示條數{1}".format(dirname, numbers))

for line in (os.path.join(fp, f) for fp, fd, fs in os.walk(dirname) for f in fs):
    d = os.path.dirname(line)
    f_s = os.path.getsize(line)
    file_size.update({line:f_s})
    dir_size[d].append(f_s)

for k in dir_size:
    dir_size[k] = sum(dir_size[k])

x = PrettyTable([u"文件名", u"文件大小/M"], encoding=sys.stdout.encoding)
x.align[u"文件名"] = "|"
x.padding_width = 1

y = PrettyTable([u"目录名", u"目录大小/M"], encoding=sys.stdout.encoding)
y.align[u"目录名"] = "|"
y.padding_width = 1

print(u"文件大小前{0}:".format(numbers))
for line in sorted(file_size.items(), key=lambda i:i[1], reverse=True)[0:numbers]:
    x.add_row([line[0], round(line[1]/1024.0/1024, 2)])
print(x)

print(u"目錄大小前{0}:".format(numbers))
for line in sorted(dir_size.items(), key=lambda i:i[1], reverse=True)[0:numbers]:
    y.add_row([line[0], round(line[1]/1024.0/1024, 2)])
print(y)

print(u"===========任意键退出！============")
# raw_input中文乱码
raw_input()
