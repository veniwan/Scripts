#!py2.7
#coding=utf-8
# 类似flume，只是输出到redis

import os
import sys
import time
import codecs
import shutil
import hashlib
import logging

import redis
from daemonize import Daemonize

reload(sys)
sys.setdefaultencoding('utf-8')

workdir = os.path.abspath(os.path.dirname(__file__))

#日志初始
pid = os.path.join(workdir, 'flume.pid')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(os.path.join(workdir, 'flume.log'), 'a')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)-8s %(filename)s %(levelname)s: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

# 日志存放位置
logs_dir = '/data/tmp/realtimelogs'
# 过期时间1h
expire = 1 * 60 * 60
# 读取间隔1s
readtime = 1


class Flume(object):
    def __init__(self):
        # flow-uuid:mtime
        self.log_files = {}
        self.log_files_for_read = {}
        self.rd = redis.Redis(host="127.0.0.1", port=6379, db=2, password="redispass")

    def check_delete(self):
        # 确定就一级目录
        now = time.time()
        for log_file in os.listdir(logs_dir):
            log_file_mtime = os.path.getmtime(log_file)
            if log_file in self.log_files:
                if now - self.log_files[log_file] > expire:
                    self.delete_file(log_file)
                    self.delete_key(log_file)
                    del self.log_files[log_file]
                    del self.log_files_for_read[log_file]
                else:
                    # 更新文件时间戳
                    if log_file_mtime != self.log_files_for_read[log_file][0]:
                        self.log_files_for_read[log_file][0] = log_file_mtime

            else:
                # 防止中断续接
                self.delete_key(log_file)
                self.log_files.update({log_file:log_file_mtime})
                self.log_files_for_read.update({log_file:[log_file_mtime, 0]})

    def delete_file(self, log_file):
        try:
            os.remove(log_file)
        except:
            logger.warning('{} has already deleted'.format(log_file))

    def delete_key(self, log_file):
        # 不给key设置过期时间，直接删除怼一块
        self.rd.delete(log_file)

    def read_file(self, log_file, file_pos):
        with codecs.open(log_file, 'r', encoding='utf-8') as f:            
            f.seek(file_pos)
            lines = f.readlines()
            if lines:
                self.rd.rpush(log_file, "".join(lines))
            return f.tell()

    def run(self):
        # 进入目录，否则glob啥的也可以，fork子进程必须在方法内，除__init__等初始外
        os.chdir(logs_dir)
        logger.info('run is begin')
        log_files_for_read_copy = {}

        while True:
            # 顶层捕获，防止异常退出
            try:
                self.check_delete()
                if self.log_files:
                    for log_file in self.log_files:
                        # 差异化方便初始取值
                        log_file_mtime_old, file_pos_old = log_files_for_read_copy.get(log_file, [None, 0])
                        log_file_mtime, file_pos = self.log_files_for_read[log_file]

                        if log_file_mtime != log_file_mtime_old:
                            file_pos_new = self.read_file(log_file, file_pos)
                            self.log_files_for_read.update({log_file:[log_file_mtime, file_pos_new]})
                            log_files_for_read_copy.update({log_file:[log_file_mtime, file_pos]})    

            except IOError as e:
                log_file = e.filename
                del self.log_files[log_file]
                del self.log_files_for_read[log_file]
                del log_files_for_read_copy[log_file]
                self.delete_key(log_file)

            except Exception as e:
                logger.error('run get exception: {}'.format(str(e)))

            finally:
                time.sleep(readtime)

        logger.info('run is done')


if __name__ == '__main__':
    flume = Flume()
    daemon = Daemonize(app='Flume', pid=pid, action=flume.run, keep_fds=keep_fds)
    daemon.start()
