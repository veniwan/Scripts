#!/usr/bin/env python2.7
#coding:utf-8

import sys
import time
import socket
import logging
import subprocess
from StringIO import StringIO
from daemonize import Daemonize

reload(sys)
sys.setdefaultencoding('utf-8')


class CheckAdmin(object):
    def __init__(self):
        self.address = '127.0.0.1' 
        self.port = 9090
        self.request = 'GET /login HTTP/1.1\r\nHost:127.0.0.1\r\n\r\n'
        
    def check(self, logger):
        try:
            s = socket.socket()
            s.connect((self.address, self.port))
            s.send(self.request)
            line = s.recv(100)
            status =  line.split()[1]
        except Exception as e:
            logger.info(str(e))
            return
        else:
            if status != '200':
                logger.info('admin down {0:=<{1}} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))), 50))
                cmd = '''
                    cd /data/www/center-new/http/ ;
                    sh shutdown.sh ;
                    sh startup.sh
                '''
                logger.info(subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate())
        finally:
            s.close()
            return

    __call__ = check    

def main():
    logger.info('check admin up/down')
    while True:
        time.sleep(120)
        check_admin(logger)

pid = "/data/tmp/check_admin.pid"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("/data/tmp/check_admin.log", "w")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)-8s: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

check_admin = CheckAdmin()
daemon = Daemonize(app='check_admin', pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
