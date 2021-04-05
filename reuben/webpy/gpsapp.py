# -------------------------------------------------
# -*- coding: utf-8 -*-
# File Name：  level
# Description :
# @Time    : 2021/4/3 23:18
# @Author  : Reuben.Lu
# -------------------------------------------------
import pynmea2
import folium
import time
import os
import urllib
import urllib.request
# urllib提供了一系列用于操作URL的功能。Get urllib的request模块可以非常方便地抓取URL内容，
# 也就是发送一个GET请求到指定的页面，然后返回HTTP的响应：
# 例如，对豆瓣的一个URLhttps://api.douban.com/v2/book/2129650进行抓取，并返回响应：


def draw_gps(locations, output_path, file_name):  # 绘制gps轨迹图
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
                        weight=5,  # 线的大小为3
                        color='green',  # 线的颜色为橙色
                        opacity=0.7  # 线的透明度
                    ).add_to(m)  # 将这条线添加到刚才的区域m内
    # 起始点，结束点
    folium.Marker(locations[0], popup='<b>Starting Point</b>').add_to(m)
    folium.Marker(locations[-1], popup='<b>End Point</b>').add_to(m)
    m.save(os.path.join(output_path, file_name))  # 将结果以HTML形式保存到指定路径

def read_gpsserver_values():
    link = "http://192.168.0.182:8080"  # Change this address to your settings
    f = urllib.request.urlopen(link)   # <http.client.HTTPResponse object at 0x7f7492a1b9e8>
    #urllib没有urlopen方法

    myfile = f.read().decode("utf8")   # <class 'bytes'>   b'8.734972998756431*28.949391118961653'
    # 用a=urllib.request.urlopen("...")打开一个网页 然后print（a） 前面总有一个b是怎么回事??????
    # 因为你用的python的版本是3.X,网页内容是二进制的，你需要进行decode,
    # 一般中文的网页编码是GBK或UTF8.这样就可以了a=urllib.request.urlopen("...").decode("utf8")或a=urllib.request.urlopen("...").decode("gbk")
    # myfile = str(myfile)  # <str>  b'8.734972998756431*28.949391118961653'
    # 调试时报错 用print打印每个阶段输出结果或者类型 方便分析
    return myfile

def run():
    count = 0
    while True:
        database = read_gpsserver_values()   #  <class 'str'>
        count += 1
        database = eval(database)      # 网页接收数据为str需要转为list，轨迹图数据标准以及元素个数统计  注意不同用data = list(data)
        print(len(database))       # 打印列表个元素个数
        # print(count)
        draw = draw_gps(database, "/home/reuben/PycharmProjects/reuben/webpy", 'gpschart.html')
        time.sleep(1)
        print("database:", database)





if __name__ == "__main__":
    run()