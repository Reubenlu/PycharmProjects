# -------------------------------------------------
# -*- coding: utf-8 -*-
# File Name：  GPS5
# Description :GPS经纬度接收，然后1.转化为轨迹输出  2.存档excel(修改中)
# @Time    : 2021/4/2 23:24
# @Author  : Reuben.Lu
# -------------------------------------------------
import pynmea2
import folium
import time
import os
import serial
import RPi.GPIO as GPIO
import pandas as pd

def gps_map(locations, output_path, file_name):  # 绘制gps轨迹图
    """
    绘制gps轨迹图
    :param locations: list, 需要绘制轨迹的经纬度信息，格式为[[lat1, lon1], [lat2, lon2], ...]
    :param output_path: str, 轨迹图保存路径
    :param file_name: str, 轨迹图保存文件名
    :return: None
    """
    m = folium.Map(locations[0], zoom_start=15, attr='default')  # 中心区域的确定
    # m = folium.Map(locations[0],  # 中心区域的确定
    #                zoom_start=15,
    #                tiles="http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}",  # 设置高德底图
    #                attr='default')
    folium.PolyLine(  # polyline方法为将坐标用线段形式连接起来
                        locations,  # 将坐标点连接起来
                        weight=3,  # 线的大小为3
                        color='green',  # 线的颜色为橙色
                        opacity=0.7  # 线的透明度
                    ).add_to(m)  # 将这条线添加到刚才的区域m内
    folium.Marker(locations[0], popup='<b>Starting Point</b>').add_to(m)  #  标记起始点，结束点
    folium.Marker(locations[-1], popup='<b>End Point</b>').add_to(m)
    m.save(os.path.join(output_path, file_name))  # 将结果以HTML形式保存到指定路径

def gps_info():
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)   # "/dev/ttyS0" 或者"/dev/ttyUSB0"
    data = []    # 存放单组坐标
    while True:  # GPS输出信息每次有6行
        try:
            time.sleep(1)
            recv = ser.readline().decode('utf8', errors='ignore')
            if recv.startswith('$'):
                record = pynmea2.parse(recv)
                if recv.startswith('$GPRMC') or recv.startswith('$GNRMC'):
                    data.append(record.latitude)
                    data.append(record.longitude)
                    print('1.Latitude:', record.latitude)
                    print('2.Longitude:', record.longitude)
                    break
                    # break和continue只能用于循环（for 、 while ）中, 不能是if
                    # 在嵌套循环中，只对最内层循环有效
                    # break：结束整个循环
                    # continue：结束本次循环，开始下一次循环
            #     elif recv.startswith('$GPGGA') or recv.startswith('$GNGGA'):
            #         print('3.Number of Satellites availabe:', record.num_sats)
            #     elif recv.startswith('$GPGSA') or recv.startswith('$BDGSA') or recv.startswith('$GNGSA'):
            #         print('4.Fixed Satellites No.: ', record.sv_id01, record.sv_id02, record.sv_id03,
            #               record.sv_id04, record.sv_id05, record.sv_id06, record.sv_id07, record.sv_id08,
            #               record.sv_id09, record.sv_id10, record.sv_id11, record.sv_id12)
            #     elif recv.startswith('$GPGSV') or recv.startswith('$BDGSV') or recv.startswith('$GBGSV') or recv.startswith(
            #             '$GLGSV'):
            #         if record.msg_num == '1':
            #             print('5.Number of Satellites in View:', record.num_sv_in_view)
            #             print("6.Satallites No.:  GROUP", record.msg_num + '    ',
            #                   '[' + record.sv_prn_num_1 + ':' + record.snr_1 + ']',
            #                   '[' + record.sv_prn_num_2 + ':' + record.snr_2 + ']',
            #                   '[' + record.sv_prn_num_3 + ':' + record.snr_3 + ']',
            #                   '[' + record.sv_prn_num_4 + ':' + record.snr_4 + ']')
            #             print("7.Satallites CN0: ", record.snr_1, record.snr_2, record.snr_3, record.snr_4)
        except (pynmea2.nmea.ParseError):
            print('NMEA wrong！')
        # time.sleep(1)
    return data

# def gps_save(data):
#     df = pd.DataFrame(data, columns=['Latitude', 'Longitude'])   # list转dataframe
#     df.to_excel("GPS_DATA.xlsx", index=False)      # 保存到本地excel

starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
GPIO.setmode(GPIO.BCM)
LED1 = 6
GPIO.cleanup()
GPIO.setup(LED1, GPIO.OUT)
GPIO.output(LED1, 0)
database = []  # 存储所有连续做点列表 需要绘制轨迹的经纬度信息，格式为[[lat1, lon1], [lat2, lon2], ...]
count = 1
if __name__ == "__main__":
    while True:
        print('---------------------------------------')
        total = gps_info()  # 执行GPS接收函数,单个坐标点[lat1, lon1]
        GPIO.output(LED1, 1)
        print('单组数据:', total)
        if not(total==[0.0, 0.0] or total==[]):   # 判断gps数组是否为空，不为空则增加值database列表中
            database.append(total)  # 多次添加[lat1, lon1] 变为 [[lat1, lon1], [lat2, lon2], ...]
            print("数据组数:{a},总列表:{b}".format(a=len(database), b=database))
            # gps_save(database)
            if not (database == [[0.0, 0.0]] or database == [] or database == [[0.0, 0.0, 0.0, 0.0]]):
                map = gps_map(database, "/home/pi/reuben/GPS_Chart", 'GPS_Chart.html')
                time.sleep(1)
        GPIO.output(LED1, 0)
        # time.sleep(0.5)
        count += 1

