# PC数据接收端

import serial
from time import sleep
import numpy as np
import cv2
import datetime


# 图像数据初始化
img = np.zeros((178, 35, 3), dtype='uint8')  # 设置图像数值的初始化参数
triger = False
ser = serial.Serial(port="COM7", baudrate=460800, timeout=0.5)
while True:
    # 判断当前写入区有没有串口数据
    if ser.in_waiting:
        cur_time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
        # msg = ser.read_all()  # 分条显示
        msg = ser.readall()
        # 写入数据到文件里
        # print(msg)
        str0 = str(msg)[5:]
        str0 = str0[2:-4]
        # print("str0[2:-4]", str0)
        list1 = str0.split(']')
        print("len(list1)", len(list1))
        row_col = 0
        for k in range(0, len(list1) - 1):  # 获得每行数据处理结果   len(list1)-1排除空格
            # list2 = []
            for i in range(0, len(list1[k])):  # 获得一行像素点的数据处理结果
                temp = list1[k].split(' ')
                # print("temp", temp)
                row_pixel_count = 0
                RGB_count = 0
                # print("len(temp)", len(temp))
                for j in range(0, len(temp)):  # 获得一行中单个像素点三通道的数据处理结果
                    # print("row_col={}  row_pixel_count={}  RGB_count={}  j={}".format(row_col, row_pixel_count,RGB_count, j))
                    if j == 0:
                        # print(temp[0][1:-1])
                        img[row_col][row_pixel_count][RGB_count] = int(temp[0][1:-1])
                    elif j < len(temp) - 1:
                        # print(temp[j][0:-1])
                        img[row_col][row_pixel_count][RGB_count] = int(temp[j][0:-1])
                    elif j == len(temp) - 1:
                        # print("temp[j]", temp[j])
                        img[row_col][row_pixel_count][RGB_count] = int(temp[j])

                    RGB_count = RGB_count + 1  # 像素点和通道数目总和+1
                    if RGB_count == 3:
                        RGB_count = 0
                        row_pixel_count = row_pixel_count + 1
            row_col = row_col + 1
        cur_time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
        print("{}: {}".format(cur_time1, cur_time2))
        if int(img[41][31][2]) > 0:
            cv2.imshow("test",img)
            cv2.waitKey(0)
            cv2.imwrite("C:\\Users\\dragon\\Desktop\\receive.jpg", img)
    else:
        # 当串口写入缓存区没数据，关闭串口和文件，结束读写操作
        if not triger:
            ser.write("start".encode("gbk"))
            triger = True

        # sleep(10)

ser.close()
