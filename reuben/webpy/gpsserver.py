# -------------------------------------------------
# -*- coding: utf-8 -*-
# File Name：  server
# Description :
# @Time    : 2021/4/3 22:48
# @Author  : Reuben.Lu
# -------------------------------------------------

import web  # 它是Python的web框架，它非常简单但功能强大，同时它是开源程序。）创建一个简单的WEB服务器
import pynmea2
import time
import serial
urls = ('/', 'index')

def gpsdata():
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)
    x = 1
    data = []  # 存放单组坐标
    while x < 7:  # GPS输出信息每次有6行
        try:
            recv = ser.readline().decode('utf8', errors='ignore')
            time.sleep(0.5)
            if recv.startswith('$'):
                record = pynmea2.parse(recv)
                if recv.startswith('$GPRMC') or recv.startswith('$GNRMC'):
                    data.append(record.latitude)
                    data.append(record.longitude)
        except (pynmea2.nmea.ParseError):
            print('NMEA wrong！')
        x += 1
        # time.sleep(1)
    return data

database = []
class index:
    def GET(self):
        total = gpsdata()  # 执行GPS接收函数
        print(total)
        if not (total == [0.0, 0.0] or total == []):  # 判断gps数组是否为空，不为空则增加值database列表中
            database.append(total)
            print('database:', database)
            time.sleep(1)
        return database

if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)   # 理论上可以用半载UART，但是测试不稳定待分析。用USB 2 UART
    app = web.application(urls, globals())
    app.run()