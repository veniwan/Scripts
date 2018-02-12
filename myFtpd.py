#!/usr/bin/env python3.6
#coding=utf-8
#execute_program: /usr/local/python3.6/bin/pyinstaller  -F  myFtpd.py

import argparse
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def main(user, passwd, ftpdir, perms, anony, host, port, max_cons, max_cons_per_ip):
    authorizer = DummyAuthorizer()

    authorizer.add_user(user, passwd, ftpdir, perm=perms)

    if anony:
        authorizer.add_anonymous(ftpdir)

    handler = FTPHandler
    handler.authorizer = authorizer

    handler.banner = "Welcome to Ftpd"

    address = (host, port)
    server = FTPServer(address, handler)

    server.max_cons = max_cons
    server.max_cons_per_ip = max_cons_per_ip
    server.serve_forever()

def init():
    perms = {
        'r':'elr',
        'rw':'elradfmwMT'
    }

    parser = argparse.ArgumentParser(description='********FTP服务********')
    parser.add_argument('-u', dest="user", default='ftpuser', help="用户")
    parser.add_argument('-p', dest="passwd", default='ftppasswd', help="密码")
    parser.add_argument('-d', dest="ftpdir", default='.', help="目录")
    parser.add_argument('-perms', dest="perms", default=perms['rw'], choices=perms.keys(), help="权限")
    parser.add_argument('-anony', dest="anony", default=False, action="store_true", help="匿名")
    parser.add_argument('-host', dest="host", default='0.0.0.0', help="主机")
    parser.add_argument('-port', dest="port", type=int, default=2121, help="端口")
    parser.add_argument('-maxc', dest="max_cons", type=int, default=256, help="最大连接数")
    parser.add_argument('-maxcpi', dest="max_cons_per_ip", type=int, default=5,  help="同IP连接数")

    return parser


if __name__ == '__main__':
    opt = init().parse_args()
    main(opt.user, opt.passwd, opt.ftpdir, opt.perms, opt.anony, opt.host, opt.port, opt.max_cons, opt.max_cons_per_ip)
