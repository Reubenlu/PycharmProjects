# -*- coding: utf-8 -*-
import sys
import smbus
import time
i2c = smbus.SMBus(1)
addr=0x44           #i2c地址
i2c.write_byte_data(addr,0x23,0x34)
# 4.5 Measurement Commands for Periodic Data Acquisition Mode
# 0x23 MSB , 0X34 LSB
time.sleep(0.5)
a = 0
while 1:
    i2c.write_byte_data(addr,0xe0,0x0)


    data = i2c.read_i2c_block_data(addr,0x00,6)# SHT30 address, 0x44(68) IIC地址，寄存器地址
# Read data back from 0x00(00), 6 bytes
# Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
    rawT = ((data[0]) << 8) | (data[1])#//温度拼接16bit : data[0]data[1]温度高8位 温度低8位
    rawR = ((data[3]) << 8) | (data[4])


    #Convert the data,review sht30 datasheet：4.12 Conversion of Signal Output
    temp = -45 + rawT * 175 / 65535
    RH = 100 * rawR / 65535
    #print(str(temp) + "C")
    #print(str(RH) +"%")
    print ("Temperature="+ str(temp) + "C" "---"  "Humidity="+ str(RH)+"%", "***" ,a )
    print("Temperature=%5.5f" % temp)
    time.sleep(5)
    a+=1
