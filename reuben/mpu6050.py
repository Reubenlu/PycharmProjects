# -------------------------------------------------
# -*- coding: utf-8 -*-
# File Name：  GPS5
# Description :mpu6050各项数据处理输出
# @Time    : 2021/4/2 23:24
# @Author  : Reuben.Lu
# -------------------------------------------------
import smbus
import math
import time

# Power management registers
power_mgmt_1 = 0x6b  # 寄存器地址   RST  WAKEUP
power_mgmt_2 = 0x6c
time.sleep(0.5)
a = 0
def read_byte(adr):    # 带参定义函数
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)   # 读adr地址的数据赋值high
    low = bus.read_byte_data(address, adr+1)  # 读adr+1地址的数据赋值low    查阅MPU-6000-Register-Map1 4.19寄存器和数据关系得知
    val = (high << 8) + low  # val 16bit
    return val

def read_word_2c(adr):  # 下面的代码从一个给定的寄存器中读取 一个单字（16bits）并将其转换为二进制补码
    val = read_word(adr)
    if (val >= 0x8000):    #最高位为1说明是负数  补码
        #return -((65535 - val) + 1)    #补码转换
        return  (val-65536)
    else:
        return val

def dist(a,b):     # 现在我们得到了每个三维空间中重力对传感器施加的值，通过这个值我们可以计算出X轴和Y轴的旋转值。
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68        # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

# ------------输出显示陀螺仪的数据 ------------
# ------------解析陀螺仪的数据------------
# 通过类似的方法，我们可以从MPU6050传感器的陀螺仪上读取数据。此功能通过以下代码来完成：
# 首先读取寄存器0x43、0x45、0x47的值，
# 同样的我们可以从MPU6050的datasheet中看到，
# 这些寄存器保存着原始的陀螺仪的数据。
# 为了转化获取的原始数据，这里需要除以131，可以得到每秒的旋转度数。

while True:
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    print("--------------------------------------------")
    print("***陀螺仪:每秒的旋转度数gyro data***")
    # print("gyro_xout: ", gyro_xout)
    # print("gyro_yout: ", gyro_yout)
    # print("gyro_zout: ", gyro_zout)
    print("gyro_xout:scaled=%6.2f" % (gyro_xout / 131))  #注意语法格式化字符串%%中间没有逗号，而上面需要
    print("gyro_yout:scaled=%6.2f" % (gyro_yout / 131))
    print("gyro_zout:scaled=%6.2f" % (gyro_zout / 131))
    print("--------------------------------------------")


    # ------------输出显示加速度 ------------
    # ------------解析加速度计的数据------------
    # 这三行代码用于读取X，Y，Z的加速度计数值，
    # 每个参数调用的是存放在传感器寄存器中的数据。MPU6050传感器有许多寄存器，
    # 它们具有不同的功能，详见MPU6050的datasheet。
    # 用于加速数据的寄存器是0x3b、0x3d、0x3f，      这些寄存器以16bit二进制补码的格式保存原始数据。
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    # 一旦我们获取了原始数据，我们就需要对它进行转换，
    # 然后把它转换成类似于旋转角度的数据。
    # 从MPU6050的datasheet数据表中我们可以看到，我们需要应用到原始加速度计值的默认转换值是16384，
    # 所以我们用这个值除以原始数据值。
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    print("--------------------------------------------")
    print("***加速度数据accelerometer data***")
    # print("accel_xout: ", accel_xout)
    # print("accel_yout: ", accel_yout)
    # print("accel_zout: ", accel_zout)
    print("accel_xout:scaled=%6.2f" % accel_xout_scaled)
    print("accel_yout:scaled=%6.2f" % accel_yout_scaled)
    print("accel_zout:scaled=%6.2f" % accel_zout_scaled)

    print("***轴和Y轴的旋转角度***")
    print("x rotation=%6.2f" % get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print("y rotation=%6.2f" % get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print("----------------------------------------------")
    print(str(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))+"*"+str(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)))
    # print('Count', a)
    Sensor_temp_out = read_word_2c(0x41)
    Sensor_temp = Sensor_temp_out/340+36.53
    print("Temperature=%6.2f" % Sensor_temp)

    time.sleep(1)
    a += 1