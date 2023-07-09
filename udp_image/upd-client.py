# -*- coding: utf-8 -*-
import socket
import time

from udp_image.util import compress_image

host = 'localhost'
port = 10488
# AF_INET: IPv4               AF_INET6: IPv6
# SOCK_STREAM: tcp数据流       SOCK_DGRAM: udp数据报
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 注意：发送的数据必须为bytes 类型，如果是其他数据类型，需要用 bytes()函数转换
# 将图像转为字节流
image_data = compress_image("../image/send_image/img_8.png")
print("image_data.length=", len(image_data))

# 分段传输
for i in range(0, len(image_data), 2048):
    s.sendto(image_data[i:i + 2048], (host, port))
    # data, address = s.recvfrom(256)
    # print('server:', data.decode('utf-8'))

# 非 2048 整数倍，传输剩余资源
if len(image_data) % 2048 != 0:
    # print(len(image_data)-len(image_data) % 2048)
    s.sendto(image_data[len(image_data)-len(image_data) % 2048:len(image_data)], (host, port))

time.sleep(2)
print("发送bye")
s.sendto("bye".encode(), (host, port))

s.close()
