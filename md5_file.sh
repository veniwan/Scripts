#!/bin/bash
# md5文件列表差别

function stVer(){
    if [[ -e /data/xx/$1 ]];then
        tgtFile="/data/xx/$1/server"
        if [[ $1 =~ ^xy[a-z]+$ ]]; then
            srcVer=xytest
        elif [[ $1 =~ ^138[a-z]+$ || $1 =~ ^TEw_[a-z]+$ ]]; then
            srcVer=mxx
        elif [[ ! -d /data/xx/$1 ]]; then
            printf "\033[31m版本$1不存在\033[0m\n"
            exit 1
        else
            srcVer=xx
        fi

    elif [[ $1 =~ ^[0-9]+$ ]];then
        if ! ls /data/xx/*_xx$1/ &> /dev/null; then
            printf "\033[31mxx$1不存在\033[0m\n"
            exit 2
        fi
        Platform=`grep -oP '(?<=PLATFORM=)\S+' /data/xx/*_xx$1/xxxxxxxxxxxxx.properties`
        tgtFile="/data/xx/${pp}_xx$1"
        if [[ "$Platform" = "tt" ]]; then
            srcVer=tt
        elif [[ "$Platform" = "zz" ]]; then
            srcVer=zzt
        else
            srcVer=xx
        fi

    else
        printf "\033[31mxx$1不存在\033[0m\n"
        exit 3
    fi
}

function main(){
    srcFile="/data/xx/${srcVer}/yy"
    while read line
    do
        srcmd5=`md5sum $srcFile/$line 2>/dev/null| awk 'NF=1'`
        tgtmd5=`md5sum $tgtFile/$line 2>/dev/null| awk 'NF=1'`
        if [[ -z $srcmd5 ]]; then
            whatError=$(find $srcFile -name `basename $srcFile/$line`)
            if [[ -z $whatError ]]; then
                 printf "\033[33m文件名有误,错文件名=>%s\033[0m\n" `basename $line`
            else
                 printf "\033[33m文件路径错,正确路径=>%s\033[0m\n" `sed -r "s#/data/xx/\w+/yy/##" <<<"$whatError"`
            fi
        else    
            if [[ $srcmd5 = $tgtmd5 ]]; then
                printf "\033[32m%s %s\t%s\t%s\033[0m\n" `md5sum {$srcFile,$tgtFile}/$line | while read line ; do haha=$(awk -F[.\ ] '$1=="Change:"{print $2,$3}' <<< "$(stat ${line#* })");echo $haha $line ; done`
            else
                printf "\033[31m%s %s\t%s\t%s\033[0m\n" `md5sum {$srcFile,$tgtFile}/$line | while read line ; do haha=$(awk -F[.\ ] '$1=="Change:"{print $2,$3}' <<< "$(stat ${line#* })");echo $haha $line ; done`
            fi
        fi
    done < /data/xx/files.txt
}

case $# in 
    1)
        stVer $1
    ;;
    2)
        stVer $2
        srcVer=$1
    ;;
    *)
        echo -e "\033[31m参数有误！sh md5_file.sh [srcVer] dstVer/serverId \033[0m"
        exit 4
    ;;
esac

main
