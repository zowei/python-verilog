import socket


# 获取当前主机 IP
def GetHostIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    print("本机ip =", ip)
    return ip


# print(bin(0x04C11DB7))

#
# sock = socket.socket()
#
# # 查看默认发送接收缓冲区大小
# recv_buff = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
# send_buff = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
# #
# print(f'默认接收缓冲区大小：{recv_buff}。默认发送缓冲区大小：{send_buff}')

