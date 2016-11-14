#!/usr/bin/env python
#encoding=utf-8

import re
import os

cmd = ''' salt "*"   status.diskusage /data  --out=raw --output-file=diskUsage.ini '''
os.system(cmd)
capNum = re.compile(r".*?'available': (\d+).*?'total': (\d+).*")
with open('diskUsage.ini') as f:
    for line in f.readlines():
        try:
            avail = reduce(lambda x,y:round(int(x)/float(y),2),capNum.search(line).groups())
        except:
            pass
        else:
            if avail < 0.20: print "salt-key: %s, avail: %s"  % (line.split(":")[0].strip('{'), avail)
