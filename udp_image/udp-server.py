# -*- coding: utf-8 -*-
import socket
import numpy as np
import cv2

host, port = 'localhost', 10488


# 利用 socket 接受二进制数据
def receive_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    data_all = []
    while True:
        # 2048 --- buffer_size 参数为接收的最大数据量
        data, address = s.recvfrom(2048)
        if data == b'bye':
            print("收到客户端发送的 bye, 断开连接")
            break
        data_all.append(data)
    s.close()
    return data_all


# 解码并组成图像
def decode_and_compos_image(data):
    image = np.array(data, np.uint8).tobytes()
    print("image=", image)
    try:
        decode_image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imshow('image_show', decode_image)
        print("showed the image to screen")
        cv2.imwrite("../image/receive_image/im-8.png", decode_image)
    except socket.error as e:
        print("非图像数据", e)
        exit(-1)
    cv2.waitKey(0)
    if 0xFF == ord('q'):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    print("server 已启动")
    # 接收数据
    data = receive_data()
    # print("data =", data)
    # 解包组成图像
    decode_and_compos_image(data)
