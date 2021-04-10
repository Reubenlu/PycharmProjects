# -------------------------------------------------
# !/usr/bin/env python
# -*- coding:utf8 -*-
# FileName: 1
# Description :
# Date    : 2021/3/30 11:09
# Author  : {USER}/Reuben.Lu
# -------------------------------------------------

# subprocess 模块允许我们启动一个新进程，并连接到它们的输入/输出/错误管道，从而获取返回值。
# Popen 是 subprocess的核心，子进程的创建和管理都靠它处理。
import subprocess
import time
a = 0
p = subprocess.Popen('candump can0', shell=True, stdout=subprocess.PIPE)
for i in iter(p.stdout.readline, 'b'):
    if not i:
        break
    #print(i)
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    a += 1
    print(a)
    print(i.decode('gbk'))
    # print(time1)

    with open("candata.txt", "a+") as f0:
        # f0.write(str(a))
        f0.write(time1)
        f0.write(i.decode('UTF-8'))

