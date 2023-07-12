import socket
import struct
import time
from udp_image.util import compress_image

host = 'localhost'
port = 10888
# AF_INET: IPv4               AF_INET6: IPv6
# SOCK_STREAM: tcp数据流       SOCK_DGRAM: udp数据报
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = input('>>>: ').encode('utf-8')
    s.sendto(data, (host, port))
    if data == b'bye':
        print("客户端发送了 bye, 退出程序")
        break
    data, address = s.recvfrom(512)
    print('server:', data.decode('utf-8'))