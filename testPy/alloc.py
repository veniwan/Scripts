#coding=utf-8

Num = int(raw_input("需要后台数量："))
Max = 24
servers = locals()
#for i in xrange(1,121):
for n in xrange(1,Num+1):
    servers['server%s' % n] = []
for m in xrange(1,120):
    if len(servers['server%s' % (m%Num+1)]) > 24:
        continue
    servers['server%s' % (m%Num+1)].append(m)

for n in xrange(1,Num+1):
	print servers['server%s' % n]
	print "server%s的组数：" % n +str(len(servers['server%s' % n]))

