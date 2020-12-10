#!/bin/bash
# Author:LHQ
# Create Time:Thu Dec 10 10:35:48 2020


# Apps Info
# 应用存放地址
# APP_HOME=/Users/shanglishuai/temp/tyronesoft/applications
# 应用名称
APP_NAME=api.main:app

# 使用说明，用来提示输入参数
usage() {
    echo "Usage: bash $0 [start|stop|restart|status|test]"
    exit 1
}

# 检查程序是否在运行
is_exist(){
    # 获取PID
    PID=$(ps -ef |grep ${APP_NAME} |grep -v grep |awk '{print $2}')
    # -z "${pid}"判断pid是否存在，如果不存在返回1，存在返回0
    if [ -z "${PID}" ]; then
        # 如果进程不存在返回1
        return 1
    else
        # 进程存在返回0
        return 0
    fi
}

# 启动程序函数
start(){
    is_exist
    if [ $? -eq "0" ]; then
        echo "${APP_NAME} is already running, PID=${PID}"
    else
        nohup uvicorn api.main:app  --host 0.0.0.0 --port 8001 --reload --reload-dir data  > /dev/null 2>&1 &
        PID=$(echo $!)
        echo "${APP_NAME} start success, PID=$!"
    fi
}

# 停止进程函数
stop(){
    is_exist
    if [ $? -eq "0" ]; then
        # uvicorn启动服务会同时产生一些子进程，单纯kill主进程
        # 并不能同时kill掉这些子进程，故这边单独kill这些子进程
        SUB_PIDS=$(ps -ef | awk '{if('$PID'==$3){print $2}}')
        for pid in $SUB_PIDS
            do
                kill -9 ${pid}    # kill子进程
            done
        kill -9 "${PID}"     # kill主(父)进程
        echo "${APP_NAME} process stop, PID=${PID}"
    else
        echo "There is not the process of ${APP_NAME}"
    fi
}

# 重启进程函数
restart(){
    stop
    start
}

# 查看进程状态
status(){
    is_exist
    if [ $? -eq "0" ]; then
        echo "${APP_NAME} is running, PID=${PID}"
    else
        echo "There is not the process of ${APP_NAME}"
    fi
}

# 测试api
txt=${2:-'全国第一'}
test(){
    cmd="curl -X POST \"http://localhost:8001/api/v1/sms-check\" -H  \"accept: application/json\" -H  \"Content-Type: application/json\" -d \"{\\\"text\\\":\\\"$txt\\\"}\""
    echo -e "[command]:\n $cmd"
    echo -e "\n[Response]:"
    eval $cmd
    echo -e "\r"
}


case $1 in
"start")
    start
    ;;
"stop")
    stop
    ;;
"restart")
    restart
    ;;
"status")
    status
    ;;
"test")
    test
    ;;
*)
    usage
    ;;
esac

exit 0
