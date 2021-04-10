# -------------------------------------------------
# -*- coding: utf-8 -*-
# File Name：  GPS4
# Description :gps接收数据处理输出
# @Time    : 2021/4/2 23:22
# @Author  : Reuben.Lu
# -------------------------------------------------
import serial
import pynmea2
import time

ser = serial.Serial("/dev/ttyS0", 9600)
data1 = []  # 存放一个坐标点
a = 0
while True:
    try:
        recv = ser.readline().decode()
        if recv.startswith('$'):
            record = pynmea2.parse(recv)
            if recv.startswith('$GPRMC') or recv.startswith('$GNRMC'):
                # print('Fix Status: ', record.status)
                print('1.Latitude: ', record.latitude)
                print('2.longitude: ', record.longitude)
            elif recv.startswith('$GPGGA') or recv.startswith('$GNGGA'):
                print('3.Number of Satellites availabe:', record.num_sats)
            elif recv.startswith('$GPGSA') or recv.startswith('$BDGSA') or recv.startswith('$GNGSA'):
                print('4.Fixed Satellites No.: ', record.sv_id01, record.sv_id02, record.sv_id03,
                      record.sv_id04,record.sv_id05, record.sv_id06,record.sv_id07, record.sv_id08,
                      record.sv_id09, record.sv_id10,record.sv_id11, record.sv_id12)
            elif recv.startswith('$GPGSV') or recv.startswith('$BDGSV') or recv.startswith('$GBGSV') or recv.startswith('$GLGSV'):
               if record.msg_num =='1':
                   print('5.Number of Satellites in View:', record.num_sv_in_view)
                   print("6.Satallites No.:  GROUP", record.msg_num+'    ','['+record.sv_prn_num_1+':'+record.snr_1+']',
                         '['+record.sv_prn_num_2+':'+record.snr_2+']', '['+record.sv_prn_num_3+':'+record.snr_3+']',
                         '['+record.sv_prn_num_4+':'+record.snr_4+']')
                   print("7.Satallites CN0: ", record.snr_1, record.snr_2, record.snr_3, record.snr_4)
            time.sleep(1)
    except (pynmea2.nmea.ParseError):
        print('NMEA wrong！')
    # a+=1
    # print(a)