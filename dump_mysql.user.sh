#!/bin/bash
# 导出数据库权限表

MYSQL_DUMP_VER=$1
MYSQL_LOAD_VER=$2

###### 全局变量开始 ######
DUMP_FILE='/tmp/dump_mysql.user.sql'
MYSQL_CMD='mysql -uroot -p123456 -BNe '
MYSQL_EXCLUDE_USER="('root','mysql.session','mysql.sys')"
MYSQL_EXCLUDE_HOST="('')"

declare -a ver_pass
ver_pass=(
	['55']="password"
	['56']="password"
	['57']="authentication_string"
)

MYSQL_OLD_PASS_FIELD=${ver_pass[$MYSQL_DUMP_VER]}
MYSQL_NEW_PASS_FIELD=${ver_pass[$MYSQL_LOAD_VER]}
###### 全局变量结束 ######

function Check(){
    if [ -z "$1" -o -z "$2" ]; then
        echo 'Position args $1 or $2 error...'
        echo "Example: $0 dump_ver[55] load_ver[57]"
        exit 1
    fi
}

function Main(){
    user_host=`$MYSQL_CMD "select user,host from mysql.user where user not in $MYSQL_EXCLUDE_USER and host not in $MYSQL_EXCLUDE_HOST;" 2> /dev/null`

    while read user host
    do
        if [[ "$host" = "%" ]]; then
           # echo "Exit: host is %"
            continue
        fi
        # 兼容5.7版本导出grant无identified by导致5.7导入失败，虽然更建议alter user修改密码
        $MYSQL_CMD "create user $user@$host;" 2> /dev/null
        $MYSQL_CMD "show grants for $user@$host;" 2> /dev/null
        $MYSQL_CMD "select concat('update mysql.user set $MYSQL_NEW_PASS_FIELD=\'', $MYSQL_OLD_PASS_FIELD, '\' where user=\'$user\' and host=\'$host\';') from mysql.user where user='$user' and host='$host';" 2>/dev/null
    done <<< "$user_host"
}

# 执行开始
Check $1 $2
Check $MYSQL_OLD_PASS_FIELD $MYSQL_NEW_PASS_FIELD
Main > $DUMP_FILE
sed -ir 's/[^;]$/&;/' $DUMP_FILE
echo "$DUMP_FILE 已生成！"
