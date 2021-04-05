# -------------------------------------------------
# -*- coding: utf-8 -*-
# File Name：  server
# Description :
# @Time    : 2021/4/3 22:48
# @Author  : Reuben.Lu
# -------------------------------------------------
# import web
# urls = ('/', 'index')
# class index:
#     def GET(self):
#         return "Hello, world!"
#
# if __name__ == "__main__":
#     app = web.application(urls, globals())
#     app.run()



import web  # 它是Python的web框架，它非常简单但功能强大，同时它是开源程序。）创建一个简单的WEB服务器
import smbus
import math
urls = ('/', 'index')

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68        # This is the address value read via the i2cdetect command
def read_byte(adr):
    return bus.read_byte_data(address, adr)
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
class index:
    def GET(self):
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        x_r = get_x_rotation(accel_xout_scaled, accel_yout_scaled,accel_zout_scaled)
        y_r = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        return str(x_r)+"*"+str(y_r)


if __name__ == "__main__":
    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)
    app = web.application(urls, globals())
    app.run()