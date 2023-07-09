# -*- codeing = utf-8 -*-
import queue
import socket
import threading
import cv2
import numpy as np

# 定义消息队列，用于存储生产者发送的数据和消费者接收的数据
msg_queue = queue.Queue()


class server(threading.Thread):
    def __init__(self, address):
        # 调用父类的初始化方法
        super().__init__()
        self.address = address

    def receive_save(self):
        # 建立 udp 连接
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(self.address)
        while True:
            data, addr = s.recvfrom(800000)
            # 存放数据到消息队列
            msg_queue.put((data, addr))

    def run(self):
        self.receive_save()


# 定义消费者类，继承自 threading.Thread
class consumer(threading.Thread):
    def __init__(self, name):
        # 调用父类的初始化方法
        super().__init__()
        # 设置线程名字
        self.name = name
        print(f"{self.name} 线程启动")

    def run(self):
        # 线程运行的方法，循环从消息队列中取出数据并处理
        # images = []
        v = cv2.VideoWriter('../video/cam-10.avi', cv2.VideoWriter_fourcc(*'XVID'), 10.0, (640, 480), True)
        while msg_queue.not_empty:
            # 从消息队列中消费数据, 返回一个元组(data, addr)
            data, addr = msg_queue.get()
            # print("data.length= ", len(data))
            # 处理数据
            np_arr = np.frombuffer(data, np.uint8)
            img_decode = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # 一帧一帧保存图片成视频
            i = cv2.resize(img_decode, (640, 480))
            v.write(i)

            # 视频展示
            cv2.startWindowThread()
            cv2.imshow('img_receive', img_decode)
            # 50ms 一张图片, 0.05s 一张图片; 5s一百张图片; 1s20张图;fps=20
            # 计算fps：fps = 1000 / x
            c = cv2.waitKey(20)
            if c == 27:  # 按了 esc 后可以退出
                exit(0)


if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    print("正在监听的ip: ", ip)
    address = ip, 20388
    # 开启 server 监听并接收数据线程
    server(address).start()
    # 消费数据
    consumer("consumer").start()
