#!/bin/bash

src="zzVer"
verList="xxVer|yyVer|TXxxx"

function doRsync(){
    src=$1
    dst=$2
    read -p "同步${src}到${dst}？(输入y确认):" -a option
    if [ $option = 'y' ];then
        echo '=================================='
        echo "同步前备份${dst}中..."
        rsync -avP ${dst}/ /data/xx/${dst}/ > /dev/null 2>&1 
        echo '=================================='
        rsync -avP --exclude=".svn" ${src}/ ${dst}/ 
        bash /data/xx.sh $dst
    else
        echo '=================================='
        echo '操作已取消'
    fi
}

case $1 in 
    xxVer|yyVer|TXxxx)
        case $# in
            1)
                dst=$1
                [[ $dst =~ ^(TX[a-z]+)$ ]] && src="TXVer"
                doRsync $src $dst
            ;;
            2)
                src=$1
                dst=$2
                grep -wq $dst <<< $verList || exit 2
                doRsync $src $dst
            ;;
            *)
                echo "????????"
            ;;
        esac
    ;;
    *)
        echo "Usage: sh rsyncTo_Ver.sh [srcVer] dstVer" 
    ;;
esac
