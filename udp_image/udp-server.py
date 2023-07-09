# -*- coding: utf-8 -*-
import gzip
import socket
from io import BytesIO
import PIL.Image
from PIL import Image
import PIL
import numpy as np
import cv2


host, port = 'localhost', 10488


# 利用 socket 接受二进制数据
def receive_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    data_all = b""
    while True:
        # 2048 --- buffer_size 参数为接收的最大数据量
        data, address = s.recvfrom(2048)
        if data == b'bye':
            print("收到客户端发送的 bye, 断开连接")
            break
        data_all += data
        # print('receive from client:', data.decode())
        # s.sendto("ok".encode("utf-8"), address)
    s.close()
    return data_all


# 解码并组成图像
def decode_and_compos_image(data):
    # image1 = np.asarray(data, dtype="uint8")
    # print("image1=", image1)
    image = np.fromstring(data, dtype="uint8")
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
    # 接收数据
    data = receive_data()
    # print("data =", data)
    # 解包，组成图像
    decode_and_compos_image(data)
