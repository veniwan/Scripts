#!/usr/bin/env python2.7
#coding:utf-8

import os
import sys
import stat
import time
import shutil
import socket
import hashlib
import logging
import platform
try:
    import fcntl
except:
    with open(os.path.join(os.path.dirname('{0}'.format(sys.modules['daemonize']).split("'")[3]), 'fcntl.py'), 'w') as f:
        f.write("""#!/usr/bin/python
def fcntl(fd, op, arg=0):
    return 0

def ioctl(fd, op, arg=0, mutable_flag=True):
    if mutable_flag:
        return 0
    else:
        return ""

def flock(fd, op):
    return

def lockf(fd, operation, length=0, start=0, whence=0):
    return
""")

from daemonize import Daemonize

reload(sys)
sys.setdefaultencoding('utf-8')


#变量初始
#os.name
OPS = platform.system()
if OPS == 'Windows':
    BASEDIR = 'xx'
elif OPS == 'Darwin':
    BASEDIR = '/Users/veniwan/tmp/'
else:
    sys.exit('{0} 此系统暂未在考虑之内'.format(OPS))

#日志初始
pid = 'check_file.pid'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler('check_file.log', 'a')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)-8s %(filename)s %(levelname)s: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


class CheckFile(object):
    def __init__(self):
        self.srcdir = BASEDIR + 'A'
        self.tgtdir = BASEDIR + 'B'
        self.bakdir = BASEDIR + 'C'
        self.md5file = BASEDIR + 'md5.txt'
        self.address = '127.0.0.1' 
        self.port = 9090
        self.request = 'POST /login HTTP/1.1\r\nHost:127.0.0.1\r\n\r\n'

    def genMd5(self, filename, blocksize=2**20):
        with open(filename, 'rb') as f:
            md5obj = hashlib.md5()
            while True:
                data = f.read(blocksize)
                if not data:
                    break
                md5obj.update(data)
        return md5obj.hexdigest()

    def cmpFile(self, srcfiles, tgtfiles):
        def _sig(st):
            return (stat.S_IFMT(st.st_mode),
                    st.st_size,
                    st.st_mtime)

        for f1, f2 in zip(srcfiles, tgtfiles):
            s1 = _sig(os.stat(f1))
            s2 = _sig(os.stat(f2))
            if s1 != s2:
                return False
            else:
                continue
        else:
            return True

    def cmpMd5(self, srcfiles, md5Dict):
        for f in srcfiles:
            if self.genMd5(f) != md5Dict.get(f):
                return False
        else:
            return True

    def apiTrigger(self):
        try:
            s = socket.socket()
            s.connect((self.address, self.port))
            s.send(self.request)
            line = s.recv(100)
            status = line.split()[1]
        except Exception as e:
            logger.warning(str(e))
            return
        else:
            if status != '200':
                logger.warning('API触发更新失败')
            else:
                logger.info('API触发更新成功')
        finally:
            s.close()
            return True

    def do(self, srcfiles, md5Dict):
        if self.cmpMd5(srcfiles, md5Dict):
            shutil.rmtree(self.bakdir)
            shutil.move(self.tgtdir, self.bakdir)
            shutil.copytree(self.srcdir, self.tgtdir)
            for i in range(5): 
                if self.apiTrigger():
                    return        

    def checkAndSync(self):
        #查看MD5文件和调用的文件名要保持一致,有字符串比较
        md5Dict = dict()
        srcfiles = [ os.path.join(fp, f) for fp, fd, fs in os.walk(self.srcdir) for f in fs ]
        tgtfiles = [ os.path.join(fp, f) for fp, fd, fs in os.walk(self.tgtdir) for f in fs ]

        with open(self.md5file) as f:
            for line in f.readlines():
                line = line.strip().split()
                md5Dict.update({line[1]:line[0]})
      
        if len(srcfiles) == len(tgtfiles):
            if self.cmpFile(srcfiles, tgtfiles):
                return
            else:
                self.do(srcfiles, md5Dict)
                return 
        else:
            self.do(srcfiles, md5Dict)
            return

        return

    @staticmethod
    def main():
        logger.info('检查文件同步及触发更新')
        while True:
            check_file()
            time.sleep(5)

    __call__ = checkAndSync

if __name__ == '__main__':
    check_file = CheckFile()
    daemon = Daemonize(app='check_file', pid=pid, action=CheckFile.main, keep_fds=keep_fds)
    daemon.start()