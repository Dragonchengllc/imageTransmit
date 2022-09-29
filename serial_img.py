# 树莓派数据发送端

import cv2
import numpy as np
import serial
import time
import datetime

src = cv2.imread("./serial_test.jpg")
h1,w1 = src.shape[0:2]
src = cv2.resize(src,(int(w1/10), int(h1/10)))
h,w = src.shape[0:2]
cv2.imwrite("./temp001.jpg",src)
print(src[0][0])
print(w,h)
print(len(src))
print(type(src[0][0]))
print(int(src[0][0][0]))

# 串口数据
ser2 = serial.Serial('/dev/ttyAMA1', 460800)  # windows change2

while True:
    count = ser2.inWaiting()
    # 发送开始
    if count != 0:
        
        receive = ser2.read(count)
        print("receive date:",receive)
        cur_time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
        if str(receive) == "b'start'":
            ser2.write("start".encode("gbk"))
            # ser2.write(str(w).encode("gbk"))
            # ser2.write(str(h).encode("gbk"))
            count1 = 0
            # for i in range(0,h):
            data = []

            for i in range(0,h):
                # temp = []
                for j in range(0, w):
                    # temp = [src[i][j][0], src[i][j][1], src[i][j][2]]
                    data.append(src[i][j][0])
                    data.append(src[i][j][1])
                    data.append(src[i][j][2])

                    # data.append(temp)
                # ser2.write(('row' + str(count1)).encode("gbk"))
                ser2.write(str(data).encode("gbk"))
                print("data:>>>>{}".format(count1))
                # print("data:>>>>{}-{}".format(count1, data))

                data = []
                count1 = count1 + 1

            # for j in range(0, h):
            #     print(src[0][j])
            #     temp = []
            #     temp.append(src[0][j][0])
            #     temp.append(src[0][j][1])
            #     temp.append(src[0][j][2])

            #    data.append(temp)
            ser2.write("end".encode("gbk"))

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        cur_time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

        print("{}: {}".format(cur_time1, cur_time2))
        break

    ser2.flushInput()
    time.sleep(0.3)
