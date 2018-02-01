#coding=utf-8

import sys
import time
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')


def tailf(nums=10, filename='test.txt'):
    nums = abs(nums)
    with codecs.open(filename, 'r', encoding='UTF-8') as f:
        offset = int(-nums)
        while True:
            try:
                f.seek(offset, 2)
            except:
                f.seek(0)
                sys.stdout.write(''.join(f.readlines()))
                break

            lines = f.readlines()
            if len(lines) > nums:
                sys.stdout.write(''.join(lines[int(-nums):]))
                break

            offset -= 1

        while True:
            lines = f.readlines()
            if lines:
                sys.stdout.write(''.join(lines))
            else:
                time.sleep(0.2)

tailf(10, 'test.txt')
