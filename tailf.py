#coding=utf-8
#Description: function tailf be similar to Linux commands tail -fn nums filename

import sys
import time
import codecs
import os.path

reload(sys)
sys.setdefaultencoding('utf-8')


def tailf(nums=10, filename='test.txt'):

    # Normal can use argparse modules to judge and limit
    if not ( nums < 0 or os.path.isfile(filename)):
        sys.exit('params may has error!')

    # compatible chinese and so on
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        offset = int(-nums)  # negative number for next 2 end forward up reading
        while True:
            # postion the read place
            try:
                f.seek(offset, 2)  # 2 is end of file
            except:
                f.seek(0)  # if throw a Exception then may file rows less then nums
                sys.stdout.write("".join(f.readlines()))
                break

            # for some character not be split otherwise throw exception
            try:
                lines = f.readlines()
                if len(lines) > nums:
                    sys.stdout.write(''.join(lines[int(-nums):]))
                    break
            except:
                pass
            offset -= 1

        while True:
            lines = f.readlines()
            if lines:
                sys.stdout.write(''.join(lines))
            else:
                time.sleep(0.2)

if __name__ == '__main__':
    tailf(10, 'test.txt')
