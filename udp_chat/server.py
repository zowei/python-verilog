import socket

host, port = 'localhost', 10888


# 利用 socket 接受二进制数据
def receive_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    # data = True
    data_all = b""
    while True:
        # 2048 --- buffer_size 参数为接收的最大数据量
        data, address = s.recvfrom(2048)
        if data == b'bye':
            print("收到客户端发送的 bye, 断开连接")
            break
        data_all += data
        print('receive from client:', data.decode('utf-8'))
        s.sendto("ok".encode("utf-8"), address)
    s.close()
    return data_all


if __name__ == '__main__':
    data = receive_data()
    print("data =", data)
